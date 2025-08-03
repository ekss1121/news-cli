import click
from rich.console import Console
from rich.table import Table
from .sources import RSSSource, RaceResultSource
from .models import NewsItem
from .filters import NewsFilter
from .formatters import TerminalFormatter, JSONFormatter, MarkdownFormatter, ResultFormatter

console = Console()


def fetch_news_logic(output_format, limit, team, driver, keyword):
    """Core logic for fetching F1 news."""
    rss = RSSSource()
    
    console.print("[bold blue]Fetching F1 news from all sources...[/bold blue]")
    news_items = []
    fetch_limit = limit * 3 if any([team, driver, keyword]) else limit
    news_items.extend(rss.fetch_news(limit=fetch_limit))
    
    # Apply filters if specified
    if any([team, driver, keyword]):
        news_filter = NewsFilter()
        
        if team:
            console.print(f"[dim]Filtering by team: {team}[/dim]")
            news_items = news_filter.filter_by_team(news_items, team)
        
        if driver:
            console.print(f"[dim]Filtering by driver: {driver}[/dim]")
            news_items = news_filter.filter_by_driver(news_items, driver)
        
        if keyword:
            console.print(f"[dim]Filtering by keyword: {keyword}[/dim]")
            news_items = news_filter.filter_by_keyword(news_items, keyword)
        
        # Deduplicate results
        news_items = news_filter.deduplicate(news_items)
        
        if not news_items:
            console.print("[yellow]No news items found matching your filters.[/yellow]")
            return
        
        console.print(f"[green]Found {len(news_items)} matching news items[/green]")
    
    # Format and display results
    if output_format == 'terminal':
        formatter = TerminalFormatter()
    elif output_format == 'json':
        formatter = JSONFormatter()
    else:
        formatter = MarkdownFormatter()
    
    formatter.format_news(news_items[:limit])


@click.group(invoke_without_command=True)
@click.option('--format', 'output_format', type=click.Choice(['terminal', 'json', 'markdown']),
              default='terminal', help='Output format')
@click.option('--limit', default=10, help='Maximum number of news items to fetch')
@click.option('--team', help='Filter by F1 team')
@click.option('--driver', help='Filter by F1 driver')
@click.option('--keyword', help='Filter by custom keyword')
@click.version_option()
@click.pass_context
def main(ctx, output_format, limit, team, driver, keyword):
    """F1 News CLI - Fetch the latest F1 news from social media."""
    if ctx.invoked_subcommand is None:
        # No subcommand provided, so run fetch by default
        fetch_news_logic(output_format, limit, team, driver, keyword)


@main.command()
@click.option('--format', 'output_format', type=click.Choice(['terminal', 'json', 'markdown']),
              default='terminal', help='Output format')
@click.option('--limit', default=10, help='Maximum number of news items to fetch')
@click.option('--team', help='Filter by F1 team')
@click.option('--driver', help='Filter by F1 driver')
@click.option('--keyword', help='Filter by custom keyword')
def fetch(output_format, limit, team, driver, keyword):
    """Fetch the latest F1 news."""
    fetch_news_logic(output_format, limit, team, driver, keyword)


@main.command()
@click.option('--team', help='Filter by F1 team')
@click.option('--driver', help='Filter by F1 driver')
@click.option('--keyword', help='Filter by custom keyword')
@click.option('--format', 'output_format', type=click.Choice(['terminal', 'json', 'markdown']),
              default='terminal', help='Output format')
@click.option('--limit', default=10, help='Maximum number of news items to fetch')
def filter(team, driver, keyword, output_format, limit):
    """Filter F1 news by team, driver, or keyword."""
    if not any([team, driver, keyword]):
        console.print("[red]Error: Please specify at least one filter (--team, --driver, or --keyword)[/red]")
        return
    
    console.print("[bold blue]Fetching and filtering F1 news...[/bold blue]")
    
    # Fetch news from RSS sources
    rss = RSSSource()
    news_items = rss.fetch_news(limit=limit * 3)  # Fetch more to account for filtering
    
    # Apply filters
    news_filter = NewsFilter()
    filtered_items = news_items
    
    if team:
        console.print(f"[dim]Filtering by team: {team}[/dim]")
        filtered_items = news_filter.filter_by_team(filtered_items, team)
    
    if driver:
        console.print(f"[dim]Filtering by driver: {driver}[/dim]")
        filtered_items = news_filter.filter_by_driver(filtered_items, driver)
    
    if keyword:
        console.print(f"[dim]Filtering by keyword: {keyword}[/dim]")
        filtered_items = news_filter.filter_by_keyword(filtered_items, keyword)
    
    # Deduplicate results
    filtered_items = news_filter.deduplicate(filtered_items)
    
    # Limit results
    filtered_items = filtered_items[:limit]
    
    if not filtered_items:
        console.print("[yellow]No news items found matching your filters.[/yellow]")
        return
    
    console.print(f"[green]Found {len(filtered_items)} matching news items[/green]")
    
    # Format and display results
    if output_format == 'terminal':
        formatter = TerminalFormatter()
    elif output_format == 'json':
        formatter = JSONFormatter()
    else:
        formatter = MarkdownFormatter()
    
    formatter.format_news(filtered_items)


@main.command()
def sources():
    """List available news sources."""
    rss = RSSSource()
    available_sources = rss.get_available_sources()
    
    console.print("[bold blue]📰 Available News Sources[/bold blue]\n")
    
    table = Table(title="F1 News Sources")
    table.add_column("Source Key", style="magenta")
    table.add_column("Source Name", style="cyan")
    table.add_column("URL", style="yellow")
    
    for key, name in available_sources.items():
        url = rss.rss_feeds[key]
        table.add_row(key, name, url)
    
    console.print(table)
    console.print("\n[dim]Usage: f1-news fetch --sources formula1_headlines,autosport[/dim]")


@main.command()
@click.option('--session', type=click.Choice(['race', 'qualifying', 'practice']),
              default='race', help='Type of session to show results for')
def result(session):
    """Show the most recent F1 session results."""
    
    try:
        source = RaceResultSource()
        formatter = ResultFormatter()
        
        if session == 'practice':
            # Handle practice sessions
            console.print("[bold blue]Fetching all practice session results...[/bold blue]")
            results = source.fetch_latest_results(session_type='practice')
        elif session == 'qualifying':
            console.print("[bold blue]Fetching latest F1 qualifying results...[/bold blue]")
            results = source.fetch_latest_results(session_type='qualifying')
        else:
            console.print("[bold blue]Fetching latest F1 race results...[/bold blue]")
            results = source.fetch_latest_results(session_type='race')
        formatter.format_results(results)

    except Exception as e:
        console.print(f"[red]Error fetching session results: {e}[/red]")


if __name__ == '__main__':
    main()