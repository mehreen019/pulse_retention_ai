"""
ML Training Pipeline
Trains churn prediction models and evaluates performance.
"""
import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Any, Optional
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, classification_report

from app.db.models.organization import Organization
from app.db.models.model_metadata import ModelMetadata
from app.services.churn_labeling import create_training_dataset, split_train_test


# Feature columns for model training
FEATURE_COLUMNS = [
    "recency_score",
    "frequency_score",
    "monetary_score",
    "engagement_score",
    "tenure_days",
    "activity_trend",
    "avg_transaction_value",
    "days_between_transactions"
]


def train_churn_model(
    organization_id: UUID,
    db: Session,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[Any, Dict[str, float]]:
    """
    Train churn prediction model for an organization.
    
    Args:
        organization_id: Organization UUID
        db: Database session
        test_size: Proportion of data for testing
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (trained_model, metrics_dict)
    """
    # Create training dataset
    df = create_training_dataset(organization_id, db)
    
    if len(df) < 10:
        raise ValueError(f"Insufficient data for training. Need at least 10 samples, got {len(df)}")
    
    # Split into train and test
    train_df, test_df = split_train_test(df, test_size=test_size, time_based=False)
    
    if len(train_df) == 0:
        raise ValueError("No training data after split")
    
    if len(test_df) == 0:
        # If no test data, use all data for training
        train_df = df
        test_df = df
    
    # Prepare features and labels
    X_train = train_df[FEATURE_COLUMNS].values
    y_train = train_df["churn_label"].values
    
    X_test = test_df[FEATURE_COLUMNS].values
    y_test = test_df["churn_label"].values
    
    # Train Logistic Regression model
    model = LogisticRegression(
        random_state=random_state,
        max_iter=1000,
        class_weight='balanced'  # Handle imbalanced classes
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    
    return model, metrics


def evaluate_model(
    model: Any,
    X_test: np.ndarray,
    y_test: np.ndarray
) -> Dict[str, float]:
    """
    Evaluate model performance.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        
    Returns:
        Dictionary with evaluation metrics
    """
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probability of churn
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    
    # ROC-AUC (handle case where only one class present)
    try:
        roc_auc = roc_auc_score(y_test, y_pred_proba)
    except ValueError:
        roc_auc = 0.0
    
    # Feature importance (coefficients for Logistic Regression)
    feature_importance = {
        col: float(coef) for col, coef in zip(FEATURE_COLUMNS, model.coef_[0])
    }
    
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "roc_auc": round(roc_auc, 4),
        "feature_importance": feature_importance
    }


def save_model(
    organization_id: UUID,
    model: Any,
    metadata: Dict[str, Any],
    base_path: str = "models"
) -> str:
    """
    Save trained model to disk.
    
    Args:
        organization_id: Organization UUID
        model: Trained model object
        metadata: Model metadata (metrics, etc.)
        base_path: Base directory for model storage
        
    Returns:
        Path to saved model file
    """
    # Create directory structure
    model_dir = Path(base_path) / str(organization_id)
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Save model
    model_path = model_dir / "churn_model.pkl"
    joblib.dump(model, model_path)
    
    return str(model_path)


def load_model(
    organization_id: UUID,
    base_path: str = "models"
) -> Any:
    """
    Load trained model from disk.
    
    Args:
        organization_id: Organization UUID
        base_path: Base directory for model storage
        
    Returns:
        Loaded model object
    """
    model_path = Path(base_path) / str(organization_id) / "churn_model.pkl"
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found for organization {organization_id}")
    
    return joblib.load(model_path)


def store_model_metadata(
    db: Session,
    organization_id: UUID,
    model_path: str,
    metrics: Dict[str, Any]
) -> ModelMetadata:
    """
    Store model metadata in database.
    
    Args:
        db: Database session
        organization_id: Organization UUID
        model_path: Path to saved model file
        metrics: Model evaluation metrics
        
    Returns:
        ModelMetadata object
    """
    # Check if metadata exists
    existing = db.query(ModelMetadata).filter(
        ModelMetadata.organization_id == organization_id
    ).order_by(ModelMetadata.trained_at.desc()).first()
    
    if existing:
        # Update existing
        existing.model_path = model_path
        existing.accuracy = metrics.get("accuracy")
        existing.precision = metrics.get("precision")
        existing.recall = metrics.get("recall")
        existing.roc_auc = metrics.get("roc_auc")
        existing.feature_importance = metrics.get("feature_importance")
        existing.trained_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new
        metadata = ModelMetadata(
            organization_id=organization_id,
            model_path=model_path,
            accuracy=metrics.get("accuracy"),
            precision=metrics.get("precision"),
            recall=metrics.get("recall"),
            roc_auc=metrics.get("roc_auc"),
            feature_importance=metrics.get("feature_importance")
        )
        db.add(metadata)
        db.commit()
        db.refresh(metadata)
        return metadata

