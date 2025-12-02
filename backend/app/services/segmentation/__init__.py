"""
Customer Segmentation Service
Provides RFM-based customer segmentation with churn risk integration
"""
from .segment_engine import segment_customer, batch_segment_customers, get_segment_distribution, get_customer_segment, batch_segment_customers_optimized, batch_segment_customers_from_db
from .rules import SEGMENT_DEFINITIONS, assign_segment
from .utils import categorize_rfm_score, categorize_churn_probability

__all__ = [
    'segment_customer',
    'batch_segment_customers',
    'get_segment_distribution',
    'get_customer_segment',
    'batch_segment_customers_optimized',
    'batch_segment_customers_from_db',
    'SEGMENT_DEFINITIONS',
    'assign_segment',
    'categorize_rfm_score',
    'categorize_churn_probability'
]
