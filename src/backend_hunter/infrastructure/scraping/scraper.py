import httpx
from typing import Dict, Optional
from ...application.ports import IScraper

class AsyncWebScraper(IScraper):
    """
    Implementación concreta de IScraper usando httpx.
    Simula ser un navegador real.
    """
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        # Headers por defecto para parecer un navegador moderno
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        }

    async def fetch_page(self, url: str) -> str:
        async with httpx.AsyncClient(headers=self.default_headers, follow_redirects=True, timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text

    async def get_headers(self, url: str) -> Dict[str, str]:
        async with httpx.AsyncClient(headers=self.default_headers, follow_redirects=True, timeout=self.timeout) as client:
            response = await client.head(url)
            # A veces HEAD falla o no devuelve todo, hacemos un GET parcial o completo si es necesario.
            # Por simplicidad, aquí retornamos las headers del response.
            # Si HEAD falla, intentamos GET stream
            if response.status_code >= 400:
                 response = await client.get(url)
            
            return dict(response.headers)
