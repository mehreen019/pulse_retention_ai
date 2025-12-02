from sqlalchemy import Column, Integer, String, Float, JSON
from app.db.base_class import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    segment_id = Column(String, nullable=True)
    churn_score = Column(Float, nullable=True, default=0.0)
    custom_fields = Column(JSON, nullable=True, default={})
    organization_id = Column(Integer, nullable=False, index=True)
