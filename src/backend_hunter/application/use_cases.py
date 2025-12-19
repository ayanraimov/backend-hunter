from datetime import datetime
from ..domain.entities import Company
from .ports import IScraper, IAnalyzer

class ScanCompanyUseCase:
    """
    Caso de Uso: Escanear una empresa individual.
    Orquestra el flujo de obtención de datos y análisis.
    """
    def __init__(self, scraper: IScraper, analyzer: IAnalyzer):
        self.scraper = scraper
        self.analyzer = analyzer

    async def execute(self, url: str) -> Company:
        # 1. Crear la entidad
        company = Company(url=url)
        
        # 2. Obtener datos crudos (Infraestructura de Red)
        try:
            html_content = await self.scraper.fetch_page(url)
            headers = await self.scraper.get_headers(url)
        except Exception as e:
            # En un caso real, manejaríamos errores de red aquí
            print(f"Error scanning {url}: {e}")
            return company

        # 3. Analizar datos (Infraestructura de Análisis)
        # Pasamos la entidad para que sea enriquecida
        self.analyzer.analyze_stack(html_content, headers, company)
        self.analyzer.analyze_compliance(html_content, company)
        
        company.last_scanned_at = datetime.now()
        
        return company
