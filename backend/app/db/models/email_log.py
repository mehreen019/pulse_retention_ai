from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
from app.db.base_class import Base


class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, nullable=False, index=True)
    recipient_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    html_body = Column(Text, nullable=False)
    text_body = Column(Text, nullable=True)
    segment_id = Column(String, nullable=True)
    status = Column(String, default="sent")  # sent, failed, pending
    sent_at = Column(DateTime, default=datetime.utcnow)
    organization_id = Column(Integer, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
