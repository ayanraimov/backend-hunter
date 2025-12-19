from enum import Enum, auto

class BackendStack(Enum):
    PYTHON = "Python"
    NODEJS = "Node.js"
    DOTNET = ".NET"
    JAVA = "Java"
    PHP = "PHP"
    GO = "Go"
    RUBY = "Ruby"
    UNKNOWN = "Unknown"

class Framework(Enum):
    # Python
    FASTAPI = "FastAPI"
    DJANGO = "Django"
    FLASK = "Flask"
    
    # Node
    EXPRESS = "Express"
    NESTJS = "NestJS"
    
    # .NET
    DOTNET_CORE = ".NET Core"
    ASP_NET = "ASP.NET"
    
    UNKNOWN = "Unknown"

class ComplianceStatus(Enum):
    COMPLIANT = "Compliant"       # Sede en Baleares
    NON_COMPLIANT = "Non-Compliant" # Sede fuera
    UNKNOWN = "Unknown"           # No se pudo determinar
