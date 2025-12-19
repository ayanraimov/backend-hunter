import re
from typing import Dict, Set, List
from bs4 import BeautifulSoup
from ...domain.enums import BackendStack, Framework
from ...domain.entities import Company

class TechDetector:
    """
    Motor de heurística para detectar tecnologías basado en huellas digitales.
    """
    
    # Patrones de cookies conocidos
    COOKIE_PATTERNS = {
        'csrftoken': (BackendStack.PYTHON, Framework.DJANGO),
        'sessionid': (BackendStack.PYTHON, Framework.DJANGO),
        'laravel_session': (BackendStack.PHP, None),
        'PHPSESSID': (BackendStack.PHP, None),
        '_rails_session': (BackendStack.RUBY, None),
        'connect.sid': (BackendStack.NODEJS, Framework.EXPRESS),
        'JSESSIONID': (BackendStack.JAVA, None),
        '.AspNetCore.': (BackendStack.DOTNET, Framework.DOTNET_CORE),
        'ASP.NET_SessionId': (BackendStack.DOTNET, Framework.ASP_NET),
    }
    
    # Patrones de URL/API conocidos
    URL_PATTERNS = [
        (r'/api/v\d+/', None, None),  # Generic API versioning
        (r'\.php($|\?)', BackendStack.PHP, None),
        (r'/wp-content/', BackendStack.PHP, None),  # WordPress
        (r'/wp-admin/', BackendStack.PHP, None),
        (r'/rails/', BackendStack.RUBY, None),
        (r'/spring/', BackendStack.JAVA, None),
    ]
    
    def detect(self, html: str, headers: Dict[str, str], company: Company):
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Análisis de Headers HTTP
        self._analyze_headers(headers, company)
        
        # 2. Análisis de Cookies
        self._analyze_cookies(headers, company)
        
        # 3. Análisis de Estructura HTML / Scripts
        self._analyze_html(soup, company)
        
        # 4. Análisis de URLs en el HTML
        self._analyze_urls(html, company)

    def _analyze_headers(self, headers: Dict[str, str], company: Company):
        server = headers.get('server', '').lower()
        x_powered = headers.get('x-powered-by', '').lower()
        via = headers.get('via', '').lower()
        
        # Python
        if any(s in server for s in ['gunicorn', 'uvicorn', 'werkzeug', 'hypercorn', 'daphne']):
            company.add_stack(BackendStack.PYTHON)
        
        # Node
        if 'express' in x_powered or 'express' in server:
            company.add_stack(BackendStack.NODEJS)
            company.add_framework(Framework.EXPRESS)
        if 'next' in x_powered or 'next.js' in x_powered:
            company.add_stack(BackendStack.NODEJS)
        if 'nestjs' in x_powered or 'nest' in x_powered:
            company.add_stack(BackendStack.NODEJS)
            company.add_framework(Framework.NESTJS)
            
        # .NET
        if 'kestrel' in server or 'asp.net' in x_powered or 'iis' in server:
            company.add_stack(BackendStack.DOTNET)
            if 'core' in x_powered:
                company.add_framework(Framework.DOTNET_CORE)
            else:
                company.add_framework(Framework.ASP_NET)
        
        # PHP
        if 'php' in x_powered or 'apache' in server:
            if 'php' in x_powered:
                company.add_stack(BackendStack.PHP)
        
        # Java
        if 'tomcat' in server or 'jetty' in server or 'wildfly' in server:
            company.add_stack(BackendStack.JAVA)
            
        # Go
        if 'go' in server or 'gin' in x_powered:
            company.add_stack(BackendStack.GO)
            
        # Specific Framework Patterns
        if 'uvicorn' in server:
            company.add_framework(Framework.FASTAPI)
        if 'werkzeug' in server:
            company.add_framework(Framework.FLASK)

    def _analyze_cookies(self, headers: Dict[str, str], company: Company):
        set_cookie = headers.get('set-cookie', '')
        
        for pattern, (stack, framework) in self.COOKIE_PATTERNS.items():
            if pattern.lower() in set_cookie.lower():
                company.add_stack(stack)
                if framework:
                    company.add_framework(framework)

    def _analyze_html(self, soup: BeautifulSoup, company: Company):
        # Django CSRF
        if soup.find('input', {'name': 'csrfmiddlewaretoken'}):
            company.add_stack(BackendStack.PYTHON)
            company.add_framework(Framework.DJANGO)
        
        # Django Admin
        if soup.find('link', href=re.compile(r'/static/admin/')):
            company.add_stack(BackendStack.PYTHON)
            company.add_framework(Framework.DJANGO)
            
        # Next.js (Node)
        if soup.find('script', {'id': '__NEXT_DATA__'}):
            company.add_stack(BackendStack.NODEJS)
        
        # Nuxt.js (Node/Vue)
        if soup.find('script', {'id': '__NUXT__'}):
            company.add_stack(BackendStack.NODEJS)
        
        # ASP.NET ViewState
        if soup.find('input', {'name': '__VIEWSTATE'}):
            company.add_stack(BackendStack.DOTNET)
            company.add_framework(Framework.ASP_NET)
            
        # ASP.NET MVC
        if soup.find('input', {'name': '__RequestVerificationToken'}):
            company.add_stack(BackendStack.DOTNET)
        
        # Laravel (PHP)
        if soup.find('meta', {'name': 'csrf-token'}):
            # Could be Laravel or other frameworks
            pass
            
        # Ruby on Rails
        if soup.find('meta', {'name': 'csrf-param', 'content': 'authenticity_token'}):
            company.add_stack(BackendStack.RUBY)
            
        # WordPress
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'WordPress')}):
            company.add_stack(BackendStack.PHP)
            
        # Spring (Java)
        if soup.find('input', {'name': '_csrf'}):
            company.add_stack(BackendStack.JAVA)

    def _analyze_urls(self, html: str, company: Company):
        for pattern, stack, framework in self.URL_PATTERNS:
            if re.search(pattern, html, re.IGNORECASE):
                if stack:
                    company.add_stack(stack)
                if framework:
                    company.add_framework(framework)
