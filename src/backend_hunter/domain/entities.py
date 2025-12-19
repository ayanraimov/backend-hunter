from dataclasses import dataclass, field
from typing import List, Optional, Set
from datetime import datetime
from .enums import BackendStack, Framework, ComplianceStatus

@dataclass
class Company:
    """
    Entidad principal de Dominio.
    Representa una empresa analizada.
    """
    url: str
    name: Optional[str] = None
    
    # Análisis Tecnológico
    detected_stacks: Set[BackendStack] = field(default_factory=set)
    detected_frameworks: Set[Framework] = field(default_factory=set)
    
    # Análisis Legal/Fiscal (FCT)
    compliance_status: ComplianceStatus = ComplianceStatus.UNKNOWN
    postal_code: Optional[str] = None
    location_details: str = ""
    
    last_scanned_at: Optional[datetime] = None

    def add_stack(self, stack: BackendStack):
        self.detected_stacks.add(stack)

    def add_framework(self, framework: Framework):
        self.detected_frameworks.add(framework)
    
    def mark_compliant(self, postal_code: str, details: str):
        self.compliance_status = ComplianceStatus.COMPLIANT
        self.postal_code = postal_code
        self.location_details = details

    @property
    def is_python_shop(self) -> bool:
        return BackendStack.PYTHON in self.detected_stacks
