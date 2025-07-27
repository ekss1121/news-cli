import click
from rich.console import Console
from rich.table import Table
from .sources import RSSSource, RaceResultSource
from .models import NewsItem
from .filters import NewsFilter
from .formatters import TerminalFormatter, JSONFormatter, MarkdownFormatter, ResultFormatter

console = Console()


@click.group()
@click.version_option()
def main():
    """F1 News CLI - Fetch the latest F1 news from social media."""
    pass


@main.command()
@click.option('--source', type=click.Choice(['rss']), 
              default='rss', help='Source to fetch news from')
@click.option('--format', 'output_format', type=click.Choice(['terminal', 'json', 'markdown']), 
              default='terminal', help='Output format')
@click.option('--limit', default=10, help='Maximum number of news items to fetch')
def fetch(source, output_format, limit):
    """Fetch the latest F1 news."""
    console.print(f"[bold blue]Fetching F1 news from {source}...[/bold blue]")
    
    news_items = []
    
    rss = RSSSource()
    news_items.extend(rss.fetch_news(limit=limit))
    
    # Format and display results
    if output_format == 'terminal':
        formatter = TerminalFormatter()
    elif output_format == 'json':
        formatter = JSONFormatter()
    else:
        formatter = MarkdownFormatter()
    
    formatter.format_news(news_items[:limit])


@main.command()
@click.option('--team', help='Filter by F1 team')
@click.option('--driver', help='Filter by F1 driver')
@click.option('--keyword', help='Filter by custom keyword')
@click.option('--format', 'output_format', type=click.Choice(['terminal', 'json', 'markdown']), 
              default='terminal', help='Output format')
def filter(team, driver, keyword, output_format):
    """Filter F1 news by team, driver, or keyword."""
    console.print("[bold blue]Filtering F1 news...[/bold blue]")
    
    # This would integrate with the fetch functionality
    console.print("[yellow]Filter functionality coming soon![/yellow]")


@main.command()
def result():
    """Show the most recent F1 race results."""
    console.print("[bold blue]Fetching latest F1 race results...[/bold blue]")
    
    try:
        source = RaceResultSource()
        race_results = source.fetch_latest_results()
        
        formatter = ResultFormatter()
        formatter.format_results(race_results)
        
    except Exception as e:
        console.print(f"[red]Error fetching race results: {e}[/red]")


if __name__ == '__main__':
    main()