"""
Email History Endpoints
Track and retrieve email sending history
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api import deps
from app.db.models.email_log import EmailLog

router = APIRouter()


@router.get("/history")
async def get_email_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status: sent, failed, pending"),
    segment_id: Optional[str] = Query(None, description="Filter by segment"),
    customer_email: Optional[str] = Query(None, description="Filter by customer email"),
    db: Session = Depends(deps.get_db),
):
    """
    Get email sending history with filters and pagination
    """
    query = db.query(EmailLog)
    
    # Apply filters
    if status:
        query = query.filter(EmailLog.status == status)
    if segment_id:
        query = query.filter(EmailLog.segment_id == segment_id)
    if customer_email:
        query = query.filter(EmailLog.recipient_email.ilike(f"%{customer_email}%"))
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    logs = query.order_by(EmailLog.sent_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [
            {
                "id": log.id,
                "customer_id": log.customer_id,
                "recipient_email": log.recipient_email,
                "subject": log.subject,
                "segment_id": log.segment_id,
                "status": log.status,
                "sent_at": log.sent_at.isoformat() if log.sent_at else None,
                "error_message": log.error_message,
            }
            for log in logs
        ]
    }


@router.get("/stats")
async def get_email_stats(
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    db: Session = Depends(deps.get_db),
):
    """
    Get email statistics for the specified time period
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Total emails sent
    total_sent = db.query(EmailLog).filter(
        EmailLog.sent_at >= cutoff_date,
        EmailLog.status == "sent"
    ).count()
    
    # Failed emails
    total_failed = db.query(EmailLog).filter(
        EmailLog.sent_at >= cutoff_date,
        EmailLog.status == "failed"
    ).count()
    
    # Emails by segment
    segment_stats = {}
    segments = db.query(EmailLog.segment_id).filter(
        EmailLog.sent_at >= cutoff_date
    ).distinct().all()
    
    for (segment,) in segments:
        if segment:
            count = db.query(EmailLog).filter(
                EmailLog.sent_at >= cutoff_date,
                EmailLog.segment_id == segment
            ).count()
            segment_stats[segment] = count
    
    # Top recipients (customers who received most emails)
    top_recipients = db.query(
        EmailLog.recipient_email,
        EmailLog.customer_id,
    ).filter(
        EmailLog.sent_at >= cutoff_date
    ).all()
    
    # Count emails per recipient
    recipient_counts = {}
    for email, customer_id in top_recipients:
        if email not in recipient_counts:
            recipient_counts[email] = {"email": email, "customer_id": customer_id, "count": 0}
        recipient_counts[email]["count"] += 1
    
    # Sort by count and get top 10
    top_10_recipients = sorted(
        recipient_counts.values(),
        key=lambda x: x["count"],
        reverse=True
    )[:10]
    
    return {
        "period_days": days,
        "total_sent": total_sent,
        "total_failed": total_failed,
        "success_rate": round((total_sent / (total_sent + total_failed) * 100) if (total_sent + total_failed) > 0 else 0, 2),
        "emails_by_segment": segment_stats,
        "top_recipients": top_10_recipients,
    }


@router.get("/customer/{customer_id}")
async def get_customer_email_history(
    customer_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(deps.get_db),
):
    """
    Get email history for a specific customer
    """
    query = db.query(EmailLog).filter(EmailLog.customer_id == customer_id)
    
    total = query.count()
    logs = query.order_by(EmailLog.sent_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "customer_id": customer_id,
        "total_emails": total,
        "items": [
            {
                "id": log.id,
                "subject": log.subject,
                "status": log.status,
                "sent_at": log.sent_at.isoformat() if log.sent_at else None,
                "segment_id": log.segment_id,
                "error_message": log.error_message,
            }
            for log in logs
        ]
    }
