from typing import Dict
from ...application.ports import IAnalyzer
from ...domain.entities import Company
from .tech_detector import TechDetector
from .location_detector import LocationDetector

class AnalyzerService(IAnalyzer):
    """
    Implementación concreta de IAnalyzer.
    Coordina los detectores especializados.
    """
    def __init__(self):
        self.tech_detector = TechDetector()
        self.location_detector = LocationDetector()

    def analyze_stack(self, html_content: str, headers: Dict[str, str], company: Company) -> Company:
        self.tech_detector.detect(html_content, headers, company)
        return company

    def analyze_compliance(self, html_content: str, company: Company) -> Company:
        self.location_detector.detect(html_content, company)
        return company
