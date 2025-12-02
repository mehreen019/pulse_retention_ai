from sqlalchemy import Column, Numeric, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class CustomerFeature(Base):
    __tablename__ = "customer_features"
    
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), primary_key=True, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    recency_score = Column(Numeric(5, 2), nullable=True)  # 0-100 scale
    frequency_score = Column(Numeric(5, 2), nullable=True)  # 0-100 scale
    monetary_score = Column(Numeric(5, 2), nullable=True)  # 0-100 scale
    engagement_score = Column(Numeric(5, 2), nullable=True)  # 0-100 scale
    tenure_days = Column(Integer, nullable=True)
    activity_trend = Column(Numeric(5, 2), nullable=True)  # Slope of activity
    avg_transaction_value = Column(Numeric(10, 2), nullable=True)
    days_between_transactions = Column(Numeric(5, 2), nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="customer_feature")
    organization = relationship("Organization", back_populates="customer_features")

