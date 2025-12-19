import asyncio
import pandas as pd
from datetime import datetime
from typing import List
from pathlib import Path
from ..domain.entities import Company
from .use_cases import ScanCompanyUseCase
from .ports import IScraper, IAnalyzer

class BulkScanUseCase:
    """
    Caso de Uso: Escanear múltiples empresas desde un archivo CSV.
    Genera un reporte en Pandas DataFrame.
    """
    def __init__(self, scraper: IScraper, analyzer: IAnalyzer, concurrency: int = 5):
        self.scraper = scraper
        self.analyzer = analyzer
        self.concurrency = concurrency
        self.scan_use_case = ScanCompanyUseCase(scraper, analyzer)

    async def execute(self, urls: List[str]) -> pd.DataFrame:
        """
        Escanea una lista de URLs y retorna un DataFrame con los resultados.
        """
        semaphore = asyncio.Semaphore(self.concurrency)
        
        async def scan_with_limit(url: str) -> Company:
            async with semaphore:
                return await self.scan_use_case.execute(url)
        
        tasks = [scan_with_limit(url) for url in urls]
        companies = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convertir resultados a DataFrame
        return self._to_dataframe(companies, urls)
    
    async def execute_from_csv(self, csv_path: str, url_column: str = 'url') -> pd.DataFrame:
        """
        Lee URLs desde un archivo CSV y ejecuta el escaneo.
        """
        df = pd.read_csv(csv_path)
        if url_column not in df.columns:
            raise ValueError(f"Column '{url_column}' not found in CSV. Available: {list(df.columns)}")
        
        urls = df[url_column].dropna().tolist()
        return await self.execute(urls)
    
    def _to_dataframe(self, companies: List, original_urls: List[str]) -> pd.DataFrame:
        rows = []
        for i, result in enumerate(companies):
            if isinstance(result, Exception):
                rows.append({
                    'url': original_urls[i],
                    'status': 'error',
                    'error': str(result),
                    'tech_stacks': '',
                    'frameworks': '',
                    'compliance': 'Unknown',
                    'postal_code': '',
                    'scanned_at': datetime.now().isoformat()
                })
            else:
                company = result
                rows.append({
                    'url': company.url,
                    'status': 'success',
                    'error': '',
                    'tech_stacks': ', '.join([s.value for s in company.detected_stacks]),
                    'frameworks': ', '.join([f.value for f in company.detected_frameworks]),
                    'compliance': company.compliance_status.value,
                    'postal_code': company.postal_code or '',
                    'scanned_at': company.last_scanned_at.isoformat() if company.last_scanned_at else ''
                })
        
        return pd.DataFrame(rows)

def export_report(df: pd.DataFrame, output_path: str, format: str = 'csv'):
    """
    Exporta el DataFrame a un archivo.
    """
    path = Path(output_path)
    if format == 'csv':
        df.to_csv(path, index=False)
    elif format == 'json':
        df.to_json(path, orient='records', indent=2)
    elif format == 'excel':
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"Unsupported format: {format}")
