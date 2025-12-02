from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base_class import Base


class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    churn_threshold_days = Column(Integer, default=30, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    customers = relationship("Customer", back_populates="organization", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="organization", cascade="all, delete-orphan")
    customer_features = relationship("CustomerFeature", back_populates="organization", cascade="all, delete-orphan")
    churn_predictions = relationship("ChurnPrediction", back_populates="organization", cascade="all, delete-orphan")
    model_metadata = relationship("ModelMetadata", back_populates="organization", cascade="all, delete-orphan")
    data_processing_status = relationship("DataProcessingStatus", back_populates="organization", cascade="all, delete-orphan")

