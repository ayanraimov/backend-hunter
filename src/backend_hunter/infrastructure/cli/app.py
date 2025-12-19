import typer
import asyncio
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from ...application.use_cases import ScanCompanyUseCase
from ...application.bulk_scan import BulkScanUseCase, export_report
from ...infrastructure.scraping.scraper import AsyncWebScraper
from ...infrastructure.analysis.analyzer_service import AnalyzerService
from ...domain.entities import Company
from ...domain.enums import ComplianceStatus

app = typer.Typer(help="The Backend Hunter Intelligence CLI")
console = Console()

def print_company_report(company: Company):
    table = Table(title=f"Reporte: {company.url}")
    
    table.add_column("Aspecto", style="cyan", no_wrap=True)
    table.add_column("Resultado", style="magenta")

    # Tecnologías
    stacks = ", ".join([s.value for s in company.detected_stacks]) or "No detectado"
    frameworks = ", ".join([f.value for f in company.detected_frameworks]) or "No detectado"
    
    table.add_row("Tech Stack", stacks)
    table.add_row("Frameworks", frameworks)
    
    # Conformidad
    compliant_style = "green" if company.compliance_status == ComplianceStatus.COMPLIANT else "red"
    compliance_text = company.compliance_status.value
    if company.postal_code:
        compliance_text += f" (CP: {company.postal_code})"
            
    table.add_row("Conformidad FCT (Baleares)", f"[{compliant_style}]{compliance_text}[/{compliant_style}]")
    if company.location_details:
        table.add_row("Detalles Ubicación", company.location_details)

    console.print(table)

@app.command()
def scan(url: str):
    """
    Escanea una URL individual en busca de stack tecnológico y conformidad fiscal.
    """
    async def _run():
        console.print(f"[bold blue]Escaneando:[/bold blue] {url} ...")
        
        scraper = AsyncWebScraper()
        analyzer = AnalyzerService()
        use_case = ScanCompanyUseCase(scraper, analyzer)
        
        company = await use_case.execute(url)
        print_company_report(company)

    asyncio.run(_run())

@app.command()
def bulk(
    csv_file: str = typer.Argument(..., help="Ruta al archivo CSV con las URLs"),
    url_column: str = typer.Option("url", "--column", "-c", help="Nombre de la columna con las URLs"),
    output: str = typer.Option("report.csv", "--output", "-o", help="Archivo de salida"),
    format: str = typer.Option("csv", "--format", "-f", help="Formato de salida: csv, json, excel"),
    concurrency: int = typer.Option(5, "--concurrency", "-n", help="Número de escaneos simultáneos")
):
    """
    Escanea múltiples URLs desde un archivo CSV y genera un reporte.
    """
    async def _run():
        scraper = AsyncWebScraper()
        analyzer = AnalyzerService()
        use_case = BulkScanUseCase(scraper, analyzer, concurrency=concurrency)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task(description=f"Escaneando URLs desde {csv_file}...", total=None)
            df = await use_case.execute_from_csv(csv_file, url_column)
        
        # Mostrar resumen
        console.print(f"\n[bold green]✓ Escaneo completado:[/bold green] {len(df)} empresas")
        
        # Estadísticas
        success_count = len(df[df['status'] == 'success'])
        error_count = len(df[df['status'] == 'error'])
        console.print(f"  ├─ Exitosos: {success_count}")
        console.print(f"  └─ Errores: {error_count}")
        
        # Tech Stack breakdown
        if success_count > 0:
            console.print("\n[bold]Tecnologías detectadas:[/bold]")
            tech_counts = df['tech_stacks'].value_counts()
            for tech, count in tech_counts.head(5).items():
                if tech:
                    console.print(f"  • {tech}: {count}")
        
        # Exportar
        export_report(df, output, format)
        console.print(f"\n[bold blue]Reporte guardado:[/bold blue] {output}")

    asyncio.run(_run())

if __name__ == "__main__":
    app()
