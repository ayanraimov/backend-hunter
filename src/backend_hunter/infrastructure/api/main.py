from fastapi import FastAPI, HTTPException
from ...application.use_cases import ScanCompanyUseCase
from ...infrastructure.scraping.scraper import AsyncWebScraper
from ...infrastructure.analysis.analyzer_service import AnalyzerService
from .schemas import ScanRequest, ScanResponse

app = FastAPI(
    title="The Backend Hunter Intelligence API",
    version="0.1.0",
    description="API para detectar Stack Tecnológico y conformidad fiscal de empresas."
)

@app.post("/scan", response_model=ScanResponse)
async def scan_company(request: ScanRequest):
    """
    Escanea una URL y devuelve la inteligencia detectada.
    """
    # Inyección de Dependencias
    scraper = AsyncWebScraper()
    analyzer = AnalyzerService()
    use_case = ScanCompanyUseCase(scraper, analyzer)
    
    try:
        company = await use_case.execute(request.url)
        
        # Mapeo manual simple de Entidad -> DTO (Schema)
        return ScanResponse(
            url=company.url,
            detected_stacks=[s.value for s in company.detected_stacks],
            detected_frameworks=[f.value for f in company.detected_frameworks],
            compliance_status=company.compliance_status.value,
            postal_code=company.postal_code,
            location_details=company.location_details
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
