import re
from typing import Optional, Tuple
from bs4 import BeautifulSoup
from ...domain.entities import Company

class LocationDetector:
    """
    Detector de conformidad legal (FCT) basado en ubicación.
    Busca códigos postales 07xxx y menciones a Baleares.
    """
    
    # Regex para CP de Baleares: 07 seguida de 3 dígitos
    BALEARES_CP_REGEX = re.compile(r'\b07\d{3}\b')
    
    KEYWORDS = ["illes balears", "baleares", "mallorca", "menorca", "ibiza", "eivissa", "palma"]

    def detect(self, html: str, company: Company):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Estrategia 1: Buscar en el footer o páginas de contacto (simplificado a todo el texto)
        # Convertimos a minúsculas para búsqueda case-insensitive
        text = soup.get_text(" ", strip=True).lower()
        
        cp_match = self.BALEARES_CP_REGEX.search(text)
        keyword_match = any(k in text for k in self.KEYWORDS)
        
        if cp_match:
            # Encontrado CP explícito
            cp_found = cp_match.group()
            details = f"Encontrado CP {cp_found} en el contenido."
            company.mark_compliant(postal_code=cp_found, details=details)
            
        elif keyword_match:
            # Heurística debil: Menciona Baleares pero no vemos CP
            # No marcamos compliant automáticamente, pero lo anotamos (o decidimos marcarlo)
            # Para este ejercicio, requerimos CP o mención explícita fuerte.
            # Vamos a asumir que si menciona Baleares es un candidato fuerte.
            pass 
            # Si queremos ser estrictos con el requisito "07xxx", solo el if anterior vale.
            # Si queremos ser flexibles, podríamos marcarlo aquí.
            # Dejaremos que '07xxx' sea la prueba definitiva de conformidad fiscal.
