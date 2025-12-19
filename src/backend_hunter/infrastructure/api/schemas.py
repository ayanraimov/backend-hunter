from pydantic import BaseModel
from typing import List, Optional
from ...domain.enums import BackendStack, Framework, ComplianceStatus

class ScanRequest(BaseModel):
    url: str

class ScanResponse(BaseModel):
    url: str
    detected_stacks: List[str]
    detected_frameworks: List[str]
    compliance_status: str
    postal_code: Optional[str]
    location_details: str

    class Config:
        from_attributes = True
