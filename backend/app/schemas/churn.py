"""
Pydantic schemas for churn prediction API.
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


class UploadStatusResponse(BaseModel):
    status: str
    records_processed: int
    errors: Optional[List[str]] = None
    updated_at: datetime


class TrainingStatusResponse(BaseModel):
    status: str
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    roc_auc: Optional[float] = None
    trained_at: Optional[datetime] = None


class ChurnPredictionResponse(BaseModel):
    customer_id: UUID
    external_customer_id: str
    churn_probability: float
    risk_segment: str


class BatchScoreResponse(BaseModel):
    success: bool
    predictions_stored: int
    errors: Optional[List[str]] = None

