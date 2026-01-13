# The Backend Hunter Intelligence

CLI tool and API for detecting Tech Stack and legal compliance (FCT) of companies.

## Architecture

The project follows **Clean Architecture / DDD**:
- `domain/` - Pure entities and business rules
- `application/` - Use cases and ports (interfaces)
- `infrastructure/` - Implementations (API, CLI, Scraping, Analysis)

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker (optional)

### Install Poetry (Windows)

```bash
pip install poetry
```

## Installation
```bash
poetry install
```
### Usage
CLI - Single scan
```bash
poetry run python -m backend_hunter.main scan https://example.com
```
Or using the installed command:

```bash
poetry run hunter scan https://example.com
```
### CLI - Bulk scanning from CSV
```bash
poetry run hunter bulk companies.csv --output report.csv
```
Available options:
```
-c, --column: Name of the column with URLs (default: url)

-o, --output: Output file (default: report.csv)

-f, --format: Output format: csv, json, excel (default: csv)

-n, --concurrency: Number of concurrent scans (default: 5)
```
### API - FastAPI Server
```bash
poetry run uvicorn backend_hunter.infrastructure.api.main:app --reload
```
Interactive documentation available at: http://127.0.0.1:8000/docs

### Docker
```bash
# Build and run API
docker compose up -d

# Bulk scanning with CLI
docker compose --profile cli run cli bulk /app/data/companies.csv -o /app/data/report.csv
```

### Detected Technologies
| Stack   | Detected Frameworks      |
| ------- | ------------------------ |
| Python  | Django, FastAPI, Flask   |
| Node.js | Express, NestJS, Next.js |
| .NET    | ASP.NET, .NET Core       |
| PHP     | Laravel, WordPress       |
| Java    | Spring                   |
| Ruby    | Rails                    |
| Go      | -                        |

### FCT Compliance (Balearic Islands)
Automatically detects 07xxx postal codes and mentions to Balearic Islands in contact and legal pages.

### Input CSV Format
```text
url
https://company1.com
https://company2.es
```

### Development
```bash
# Run tests
poetry run pytest

# Format code
poetry run black src/
poetry run isort src/

# Check types
poetry run mypy src/
```

## License

MIT License - feel free to use this project for learning or commercial purposes.

## Author

**Ayan Reyhanov Raimov**

- GitHub: [@ayanraimov](https://github.com/ayanraimov)
- LinkedIn: [ayanreyhanov](https://linkedin.com/in/ayanreyhanov)

---

⭐️ Star this repo if you find it useful!
