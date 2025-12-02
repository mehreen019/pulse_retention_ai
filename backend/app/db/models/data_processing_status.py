from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base_class import Base


class DataProcessingStatus(Base):
    __tablename__ = "data_processing_status"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    status = Column(String, nullable=False)  # 'uploaded', 'processing', 'features_calculated', 'ready', 'error'
    records_processed = Column(Integer, default=0, nullable=False)
    errors = Column(JSONB, nullable=True)  # List of error messages
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="data_processing_status")

