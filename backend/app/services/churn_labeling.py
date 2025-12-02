"""
Churn Labeling Service
Defines churn based on organization's threshold and creates training datasets.
"""
import pandas as pd
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.models.customer import Customer
from app.db.models.transaction import Transaction
from app.db.models.customer_feature import CustomerFeature
from app.db.models.organization import Organization


def label_churn(
    customer_id: UUID,
    churn_threshold_days: int,
    db: Session,
    current_date: Optional[datetime] = None
) -> int:
    """
    Label a customer as churned (1) or active (0).
    
    Args:
        customer_id: Customer UUID
        churn_threshold_days: Number of days of inactivity to consider churn
        db: Database session
        current_date: Current date (defaults to today)
        
    Returns:
        1 if churned, 0 if active
    """
    if current_date is None:
        current_date = datetime.now().date()
    
    # Get last transaction date
    last_transaction = db.query(func.max(Transaction.event_date)).filter(
        Transaction.customer_id == customer_id
    ).scalar()
    
    if last_transaction is None:
        # No transactions = churned
        return 1
    
    # Calculate days since last activity
    days_since_last = (current_date - last_transaction).days
    
    # Label as churned if inactive for more than threshold
    return 1 if days_since_last >= churn_threshold_days else 0


def create_training_dataset(
    organization_id: UUID,
    db: Session,
    churn_threshold: Optional[int] = None,
    current_date: Optional[datetime] = None
) -> pd.DataFrame:
    """
    Create training dataset with features and churn labels.
    
    Args:
        organization_id: Organization UUID
        db: Database session
        churn_threshold: Churn threshold in days (uses org default if None)
        current_date: Current date (defaults to today)
        
    Returns:
        DataFrame with features and churn labels
    """
    if current_date is None:
        current_date = datetime.now().date()
    
    # Get organization churn threshold
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise ValueError(f"Organization {organization_id} not found")
    
    if churn_threshold is None:
        churn_threshold = org.churn_threshold_days
    
    # Get all customers with features
    customers = db.query(Customer).filter(
        Customer.organization_id == organization_id
    ).all()
    
    data = []
    
    for customer in customers:
        # Get customer features
        feature = db.query(CustomerFeature).filter(
            CustomerFeature.customer_id == customer.id
        ).first()
        
        if not feature:
            # Skip customers without features
            continue
        
        # Label churn
        churn_label = label_churn(customer.id, churn_threshold, db, current_date)
        
        # Create feature vector
        data.append({
            "customer_id": str(customer.id),
            "recency_score": float(feature.recency_score or 0),
            "frequency_score": float(feature.frequency_score or 0),
            "monetary_score": float(feature.monetary_score or 0),
            "engagement_score": float(feature.engagement_score or 0),
            "tenure_days": int(feature.tenure_days or 0),
            "activity_trend": float(feature.activity_trend or 0),
            "avg_transaction_value": float(feature.avg_transaction_value or 0),
            "days_between_transactions": float(feature.days_between_transactions or 0),
            "churn_label": churn_label
        })
    
    df = pd.DataFrame(data)
    
    if len(df) == 0:
        raise ValueError("No training data available. Ensure features are calculated first.")
    
    return df


def split_train_test(
    df: pd.DataFrame,
    test_size: float = 0.2,
    time_based: bool = True,
    date_column: Optional[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split dataset into train and test sets.
    
    Args:
        df: DataFrame with features and labels
        test_size: Proportion of data for testing (0.0 to 1.0)
        time_based: If True, split by time (use last N% as test). If False, random split.
        date_column: Column name for date-based splitting (not used if time_based=False)
        
    Returns:
        Tuple of (train_df, test_df)
    """
    if time_based:
        # Time-based split: use last N% of data
        # Since we don't have explicit dates, we'll use a random split but
        # in production, you'd sort by a date column
        n_test = int(len(df) * test_size)
        train_df = df.iloc[:-n_test] if n_test > 0 else df
        test_df = df.iloc[-n_test:] if n_test > 0 else pd.DataFrame()
    else:
        # Random split
        test_df = df.sample(frac=test_size, random_state=42)
        train_df = df.drop(test_df.index)
    
    return train_df, test_df

