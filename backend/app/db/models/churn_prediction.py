from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class ChurnPrediction(Base):
    __tablename__ = "churn_predictions"
    
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), primary_key=True, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    churn_probability = Column(Numeric(5, 4), nullable=False)  # 0.0000 to 1.0000
    risk_segment = Column(String, nullable=False)  # 'Low', 'Medium', 'High', 'Critical'
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="churn_prediction")
    organization = relationship("Organization", back_populates="churn_predictions")

