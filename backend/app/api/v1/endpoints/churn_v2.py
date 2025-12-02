"""
Churn Prediction API Endpoints - V2
New simplified flow using Supabase storage without database transactions.
"""
import uuid
import pandas as pd
import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db
from app.db.models.organization import Organization
from app.db.models.dataset import Dataset
from app.db.models.model_metadata import ModelMetadata
from app.services.storage import (
    upload_to_supabase,
    upload_dataframe_to_supabase,
    download_from_supabase
)
from app.services.feature_engineering_csv import (
    engineer_features_from_csv,
    create_training_dataset_from_csv
)
from app.services.ml_training import (
    train_churn_model_from_dataframe,
    save_model_to_disk,
    load_model_from_disk,
    predict_from_features
)

router = APIRouter()


def get_organization(org_id: uuid.UUID, db: Session) -> Organization:
    """Helper to get organization or raise 404."""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization {org_id} not found"
        )
    return org


@router.post("/organizations/{org_id}/upload-dataset")
async def upload_dataset(
    org_id: uuid.UUID,
    file: UploadFile = File(...),
    has_churn_label: bool = False,
    db: Session = Depends(get_db)
):
    """
    Step 1: Upload customer transaction CSV to Supabase storage.

    CSV must have these columns:
        - customer_id (required): Customer identifier
        - event_date (required): Transaction date (YYYY-MM-DD)
        - amount (optional): Transaction value
        - event_type (optional): Type of event
        - churn_label (optional): 0 or 1 if has_churn_label=True

    The CSV is uploaded to Supabase bucket 'datasets' and the URL is stored in the database.

    Args:
        org_id: Organization UUID
        file: CSV file
        has_churn_label: Whether the CSV includes churn labels (default: False)
        db: Database session

    Returns:
        dataset_id, file_url, status
    """
    org = get_organization(org_id, db)

    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV"
        )

    try:
        # Upload to Supabase
        upload_result = await upload_to_supabase(
            file=file,
            bucket_name="datasets",
            folder=f"org_{org_id}/raw",
            custom_filename=None  # Auto-generate unique filename
        )

        # Read CSV to get row count
        file.file.seek(0)
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        row_count = len(df)

        # Create dataset record
        dataset = Dataset(
            id=uuid.uuid4(),
            organization_id=org_id,
            dataset_type="raw",
            file_url=upload_result["file_url"],
            bucket_name=upload_result["bucket_name"],
            file_path=upload_result["file_path"],
            filename=upload_result["filename"],
            file_size=upload_result["size"],
            row_count=row_count,
            has_churn_label=str(has_churn_label),
            status="uploaded"
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return {
            "success": True,
            "dataset_id": str(dataset.id),
            "file_url": dataset.file_url,
            "row_count": row_count,
            "status": "uploaded",
            "message": "Dataset uploaded successfully to Supabase storage"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading dataset: {str(e)}"
        )


async def process_features_background(
    org_id: uuid.UUID,
    dataset_id: uuid.UUID,
    db_session: Session
):
    """
    Background task: Download CSV, engineer features, upload features CSV to Supabase.
    """
    try:
        # Get dataset
        dataset = db_session.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            return

        # Update status
        dataset.status = "processing"
        db_session.commit()

        # Download CSV from Supabase
        csv_bytes = download_from_supabase(dataset.bucket_name, dataset.file_path)
        df = pd.read_csv(io.BytesIO(csv_bytes))

        # Engineer features
        has_churn = dataset.has_churn_label == "True"
        features_df = engineer_features_from_csv(df, has_churn_label=has_churn)

        # Convert to CSV bytes
        features_csv = features_df.to_csv(index=False).encode('utf-8')

        # Upload features CSV to Supabase
        features_result = await upload_dataframe_to_supabase(
            df_csv_bytes=features_csv,
            bucket_name="utils",
            folder=f"org_{org_id}/features",
            filename=f"features_{dataset_id}.csv"
        )

        # Store features dataset record
        features_dataset = Dataset(
            id=uuid.uuid4(),
            organization_id=org_id,
            dataset_type="features",
            file_url=features_result["file_url"],
            bucket_name=features_result["bucket_name"],
            file_path=features_result["file_path"],
            filename=features_result["filename"],
            file_size=features_result["size"],
            row_count=len(features_df),
            has_churn_label=dataset.has_churn_label,
            status="ready"
        )
        db_session.add(features_dataset)

        # Update raw dataset status
        dataset.status = "features_ready"
        db_session.commit()

    except Exception as e:
        dataset.status = "error"
        db_session.commit()
        print(f"Error processing features: {str(e)}")


@router.post("/organizations/{org_id}/datasets/{dataset_id}/process-features")
async def process_features(
    org_id: uuid.UUID,
    dataset_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Step 2: Download CSV, engineer features, and upload features CSV to Supabase 'utils' bucket.

    This is a background task. The features will be calculated from the raw CSV and
    a new features CSV will be uploaded to Supabase.

    Args:
        org_id: Organization UUID
        dataset_id: Dataset UUID from Step 1
        background_tasks: FastAPI background tasks
        db: Database session

    Returns:
        Status message
    """
    org = get_organization(org_id, db)

    # Get dataset
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.organization_id == org_id,
        Dataset.dataset_type == "raw"
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset {dataset_id} not found"
        )

    # Add background task
    background_tasks.add_task(process_features_background, org_id, dataset_id, db)

    return {
        "success": True,
        "message": "Feature engineering started in background",
        "dataset_id": str(dataset_id)
    }


async def train_model_background(
    org_id: uuid.UUID,
    model_type: str,
    churn_threshold_days: int,
    db_session: Session
):
    """
    Background task: Train churn prediction model.
    """
    try:
        # Create model metadata record
        model_metadata = ModelMetadata(
            id=uuid.uuid4(),
            organization_id=org_id,
            model_path="",  # Will update after training
            model_type=model_type,
            status="training"
        )
        db_session.add(model_metadata)
        db_session.commit()
        db_session.refresh(model_metadata)

        # Get latest features dataset
        features_dataset = db_session.query(Dataset).filter(
            Dataset.organization_id == org_id,
            Dataset.dataset_type == "features",
            Dataset.status == "ready"
        ).order_by(Dataset.uploaded_at.desc()).first()

        if not features_dataset:
            model_metadata.status = "failed"
            model_metadata.error_message = "No features dataset found"
            db_session.commit()
            return

        # Download features CSV
        features_bytes = download_from_supabase(
            features_dataset.bucket_name,
            features_dataset.file_path
        )
        features_df = pd.read_csv(io.BytesIO(features_bytes))

        # If no churn label, get raw dataset and generate labels
        if features_dataset.has_churn_label != "True":
            # Get raw dataset
            raw_dataset = db_session.query(Dataset).filter(
                Dataset.organization_id == org_id,
                Dataset.dataset_type == "raw",
                Dataset.status.in_(["uploaded", "features_ready"])
            ).order_by(Dataset.uploaded_at.desc()).first()

            if not raw_dataset:
                model_metadata.status = "failed"
                model_metadata.error_message = "No raw dataset found for labeling"
                db_session.commit()
                return

            # Download raw CSV
            raw_bytes = download_from_supabase(raw_dataset.bucket_name, raw_dataset.file_path)
            raw_df = pd.read_csv(io.BytesIO(raw_bytes))

            # Generate training dataset with labels
            from app.services.feature_engineering_csv import create_training_dataset_from_csv
            training_df = create_training_dataset_from_csv(raw_df, churn_threshold_days)

        else:
            training_df = features_df

        # Train model
        model, metrics = train_churn_model_from_dataframe(
            training_df=training_df,
            model_type=model_type
        )

        # Save model
        model_path = save_model_to_disk(model, str(org_id), metrics)

        # Update metadata
        model_metadata.model_path = model_path
        model_metadata.status = "completed"
        model_metadata.accuracy = metrics.get("accuracy")
        model_metadata.precision = metrics.get("precision")
        model_metadata.recall = metrics.get("recall")
        model_metadata.f1_score = metrics.get("f1_score")
        model_metadata.roc_auc = metrics.get("roc_auc")
        model_metadata.feature_importance = metrics.get("feature_importance")
        model_metadata.training_samples = metrics.get("total_samples")
        model_metadata.churn_rate = metrics.get("churn_rate")
        db_session.commit()

    except Exception as e:
        model_metadata.status = "failed"
        model_metadata.error_message = str(e)
        db_session.commit()
        print(f"Error training model: {str(e)}")


@router.post("/organizations/{org_id}/train")
async def train_model(
    org_id: uuid.UUID,
    model_type: str = "logistic_regression",
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Step 3: Train churn prediction model (background task).

    Downloads the latest features dataset, trains a model, and saves it locally.
    If the dataset doesn't have churn labels, it will auto-generate them based on
    the organization's churn threshold.

    Args:
        org_id: Organization UUID
        model_type: Model type ('logistic_regression', 'random_forest', 'gradient_boosting')
        background_tasks: FastAPI background tasks
        db: Database session

    Returns:
        Training job status
    """
    org = get_organization(org_id, db)

    # Validate model type
    valid_models = ["logistic_regression", "random_forest", "gradient_boosting"]
    if model_type not in valid_models:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid model_type. Must be one of: {', '.join(valid_models)}"
        )

    # Add background task
    background_tasks.add_task(
        train_model_background,
        org_id,
        model_type,
        org.churn_threshold_days,
        db
    )

    return {
        "success": True,
        "message": "Model training started in background",
        "model_type": model_type
    }


@router.get("/organizations/{org_id}/training-status")
async def get_training_status(
    org_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Get training status and metrics.

    Returns the latest model training status for the organization.
    """
    org = get_organization(org_id, db)

    metadata = db.query(ModelMetadata).filter(
        ModelMetadata.organization_id == org_id
    ).order_by(ModelMetadata.trained_at.desc()).first()

    if not metadata:
        return {
            "status": "not_started",
            "message": "No training job found"
        }

    return {
        "status": metadata.status,
        "model_type": metadata.model_type,
        "accuracy": float(metadata.accuracy) if metadata.accuracy else None,
        "precision": float(metadata.precision) if metadata.precision else None,
        "recall": float(metadata.recall) if metadata.recall else None,
        "f1_score": float(metadata.f1_score) if metadata.f1_score else None,
        "roc_auc": float(metadata.roc_auc) if metadata.roc_auc else None,
        "training_samples": metadata.training_samples,
        "churn_rate": float(metadata.churn_rate) if metadata.churn_rate else None,
        "trained_at": metadata.trained_at,
        "error_message": metadata.error_message
    }


@router.post("/organizations/{org_id}/predict")
async def predict_churn(
    org_id: uuid.UUID,
    customer_data: dict,
    db: Session = Depends(get_db)
):
    """
    Step 4: Get churn prediction for a customer.

    Provide customer transaction data and get back churn probability.

    Expected input format:
    {
        "customer_id": "CUST-001",
        "transactions": [
            {"event_date": "2024-01-15", "amount": 150.50, "event_type": "purchase"},
            {"event_date": "2024-01-20", "amount": 200.00, "event_type": "purchase"}
        ]
    }

    Returns:
        {
            "customer_id": "CUST-001",
            "churn_probability": 0.23,
            "risk_segment": "Low"
        }
    """
    org = get_organization(org_id, db)

    try:
        # Load model
        model = load_model_from_disk(str(org_id))

        # Convert input to DataFrame
        customer_id = customer_data.get("customer_id")
        transactions = customer_data.get("transactions", [])

        if not customer_id or not transactions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide customer_id and transactions"
            )

        # Build transactions DataFrame
        trans_df = pd.DataFrame(transactions)
        trans_df["customer_id"] = customer_id

        # Engineer features
        features_df = engineer_features_from_csv(trans_df, has_churn_label=False)

        # Predict
        predictions = predict_from_features(model, features_df)

        return predictions.to_dict(orient="records")[0]

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No trained model found for organization {org_id}. Please train a model first."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting churn: {str(e)}"
        )
