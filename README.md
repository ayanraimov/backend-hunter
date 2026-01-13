# The Backend Hunter Intelligence

Herramienta CLI y API para detectar Stack Tecnológico y conformidad legal (FCT) de empresas.

## Arquitectura

El proyecto sigue **Clean Architecture / DDD**:
- `domain/` - Entidades y reglas de negocio puras
- `application/` - Casos de uso y puertos (interfaces)
- `infrastructure/` - Implementaciones (API, CLI, Scraping, Análisis)

## Prerrequisitos

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker (opcional)

### Instalar Poetry (Windows)

```bash
pip install poetry
```

## Instalación

```bash
poetry install
```

## Uso

### CLI - Escaneo individual

```bash
poetry run python -m backend_hunter.main scan https://ejemplo.com
```

O usando el comando instalado:

```bash
poetry run hunter scan https://ejemplo.com
```

### CLI - Escaneo masivo desde CSV

```bash
poetry run hunter bulk empresas.csv --output reporte.csv
```

Opciones disponibles:
- `-c, --column`: Nombre de la columna con URLs (default: `url`)
- `-o, --output`: Archivo de salida (default: `report.csv`)
- `-f, --format`: Formato de salida: `csv`, `json`, `excel` (default: `csv`)
- `-n, --concurrency`: Número de escaneos simultáneos (default: `5`)

### API - Servidor FastAPI

```bash
poetry run uvicorn backend_hunter.infrastructure.api.main:app --reload
```

Documentación interactiva disponible en: http://127.0.0.1:8000/docs

### Docker

```bash
# Construir y ejecutar API
docker compose up -d

# Escaneo masivo con CLI
docker compose --profile cli run cli bulk /app/data/empresas.csv -o /app/data/reporte.csv
```

## Tecnologías Detectadas

| Stack    | Frameworks detectados           |
|----------|--------------------------------|
| Python   | Django, FastAPI, Flask         |
| Node.js  | Express, NestJS, Next.js       |
| .NET     | ASP.NET, .NET Core             |
| PHP      | Laravel, WordPress             |
| Java     | Spring                         |
| Ruby     | Rails                          |
| Go       | -                              |

## Conformidad FCT (Baleares)

Detecta automáticamente códigos postales `07xxx` y menciones a Islas Baleares en páginas de contacto y legales.

## Formato CSV de entrada

```csv
url
https://empresa1.com
https://empresa2.es
```

## Desarrollo

```bash
# Ejecutar tests
poetry run pytest

# Formatear código
poetry run black src/
poetry run isort src/

# Verificar tipos
poetry run mypy src/
```
