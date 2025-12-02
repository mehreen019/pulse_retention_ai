from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base_class import Base


class ModelMetadata(Base):
    __tablename__ = "model_metadata"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    model_path = Column(String, nullable=False)  # Path to saved model file
    accuracy = Column(Numeric(5, 4), nullable=True)
    precision = Column(Numeric(5, 4), nullable=True)
    recall = Column(Numeric(5, 4), nullable=True)
    roc_auc = Column(Numeric(5, 4), nullable=True)
    feature_importance = Column(JSONB, nullable=True)  # Dictionary of feature names and importance scores
    trained_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="model_metadata")

