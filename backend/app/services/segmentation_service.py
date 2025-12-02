"""
Segmentation Service
Handles segment data and customer segmentation.
Currently uses mock data, designed for easy API integration with teammate's service.
"""
from typing import List, Dict, Any, Optional
from app.schemas.customer import SegmentResponse


class SegmentationService:
    """Service for managing customer segments"""
    
    @staticmethod
    def get_mock_segments() -> List[Dict[str, Any]]:
        """
        Returns mock segment data for demo purposes.
        
        TODO: Replace with teammate's segmentation API:
        - Endpoint: GET /api/segments?organization_id={org_id}
        - Response: List of segments with customer counts
        """
        return [
            {
                "id": "s1",
                "name": "High Value Customers",
                "description": "Customers with high purchase amounts and low churn risk",
                "customer_count": 3
            },
            {
                "id": "s2",
                "name": "At Risk Customers",
                "description": "Customers with high churn probability",
                "customer_count": 3
            },
            {
                "id": "s3",
                "name": "New Users",
                "description": "Recently onboarded customers",
                "customer_count": 4
            }
        ]
    
    @staticmethod
    async def get_segments(organization_id: int) -> List[SegmentResponse]:
        """
        Get all segments for an organization.
        
        Args:
            organization_id: The organization ID
            
        Returns:
            List of segments
            
        TODO: Replace with API call to teammate's service:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SEGMENTATION_API_URL}/api/segments",
                    params={"organization_id": organization_id}
                )
                data = response.json()
                return [SegmentResponse(**s) for s in data]
        """
        segments = SegmentationService.get_mock_segments()
        return [SegmentResponse(**s) for s in segments]
    
    @staticmethod
    async def get_segment_by_id(segment_id: str, organization_id: int) -> Optional[SegmentResponse]:
        """
        Get a specific segment by ID.
        
        Args:
            segment_id: Segment ID
            organization_id: Organization ID
            
        Returns:
            Segment or None
            
        TODO: Replace with API call:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SEGMENTATION_API_URL}/api/segments/{segment_id}",
                    params={"organization_id": organization_id}
                )
                return SegmentResponse(**response.json())
        """
        segments = SegmentationService.get_mock_segments()
        segment = next((s for s in segments if s["id"] == segment_id), None)
        if segment:
            return SegmentResponse(**segment)
        return None
    
    @staticmethod
    async def get_segment_customers(segment_id: str, organization_id: int) -> List[str]:
        """
        Get all customer IDs in a segment.
        
        Args:
            segment_id: Segment ID
            organization_id: Organization ID
            
        Returns:
            List of customer IDs
            
        TODO: Replace with API call:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SEGMENTATION_API_URL}/api/segments/{segment_id}/customers",
                    params={"organization_id": organization_id}
                )
                return response.json()["customer_ids"]
        """
        from app.services.customer_service import CustomerService
        
        # For now, use the CustomerService mock data
        customers = CustomerService.get_mock_customers()
        customer_ids = [c["id"] for c in customers if c.get("segment_id") == segment_id]
        return customer_ids
