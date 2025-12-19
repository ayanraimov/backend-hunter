from abc import ABC, abstractmethod
from typing import Optional, Dict
from ..domain.entities import Company

class IScraper(ABC):
    """
    Puerto (Interface) para el servicio de Scraping.
    La capa de infraestructura implementará esto usando httpx, selenium, etc.
    """
    @abstractmethod
    async def fetch_page(self, url: str) -> str:
        """Descarga el HTML crudo o contenido de la página."""
        pass

    @abstractmethod
    async def get_headers(self, url: str) -> Dict[str, str]:
        """Obtiene las cabeceras HTTP."""
        pass

class IAnalyzer(ABC):
    """
    Puerto para el servicio de Análisis de contenido.
    """
    @abstractmethod
    def analyze_stack(self, html_content: str, headers: Dict[str, str], company: Company) -> Company:
        """Analiza el contenido para detectar tecnologías."""
        pass

    @abstractmethod
    def analyze_compliance(self, html_content: str, company: Company) -> Company:
        """Analiza el contenido para verificar conformidad fiscal (FCT)."""
        pass
