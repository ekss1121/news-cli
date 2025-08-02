import click
from rich.console import Console
from rich.table import Table
from .sources import RSSSource, RaceResultSource
from .models import NewsItem
from .filters import NewsFilter
from .formatters import TerminalFormatter, JSONFormatter, MarkdownFormatter, ResultFormatter

console = Console()


def fetch_news_logic(source, sources, output_format, limit, team, driver, keyword):
    """Core logic for fetching F1 news."""
    rss = RSSSource()
    
    # Parse sources parameter
    selected_sources = None
    if sources:
        selected_sources = [s.strip() for s in sources.split(',')]
        available_sources = rss.get_available_sources()
        invalid_sources = [s for s in selected_sources if s not in rss.rss_feeds]
        if invalid_sources:
            console.print(f"[red]Invalid sources: {', '.join(invalid_sources)}[/red]")
            console.print(f"[yellow]Available sources: {', '.join(rss.rss_feeds.keys())}[/yellow]")
            return
        source_names = [available_sources[s] for s in selected_sources]
        console.print(f"[bold blue]Fetching F1 news from: {', '.join(source_names)}[/bold blue]")
    else:
        console.print("[bold blue]Fetching F1 news from all sources...[/bold blue]")
    
    news_items = []
    fetch_limit = limit * 3 if any([team, driver, keyword]) else limit
    news_items.extend(rss.fetch_news(limit=fetch_limit, sources=selected_sources))
    
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
@click.option('--source', type=click.Choice(['rss']),
              default='rss', help='Source to fetch news from')
@click.option('--sources', 
              help='Comma-separated list of specific news sources (formula1_headlines,autosport,motorsport,espn)')
@click.option('--format', 'output_format', type=click.Choice(['terminal', 'json', 'markdown']),
              default='terminal', help='Output format')
@click.option('--limit', default=10, help='Maximum number of news items to fetch')
@click.option('--team', help='Filter by F1 team')
@click.option('--driver', help='Filter by F1 driver')
@click.option('--keyword', help='Filter by custom keyword')
@click.version_option()
@click.pass_context
def main(ctx, source, sources, output_format, limit, team, driver, keyword):
    """F1 News CLI - Fetch the latest F1 news from social media."""
    if ctx.invoked_subcommand is None:
        # No subcommand provided, so run fetch by default
        fetch_news_logic(source, sources, output_format, limit, team, driver, keyword)


@main.command()
@click.option('--source', type=click.Choice(['rss']),
              default='rss', help='Source to fetch news from')
@click.option('--sources', 
              help='Comma-separated list of specific news sources (formula1_headlines,autosport,motorsport,espn)')
@click.option('--format', 'output_format', type=click.Choice(['terminal', 'json', 'markdown']),
              default='terminal', help='Output format')
@click.option('--limit', default=10, help='Maximum number of news items to fetch')
@click.option('--team', help='Filter by F1 team')
@click.option('--driver', help='Filter by F1 driver')
@click.option('--keyword', help='Filter by custom keyword')
def fetch(source, sources, output_format, limit, team, driver, keyword):
    """Fetch the latest F1 news."""
    fetch_news_logic(source, sources, output_format, limit, team, driver, keyword)


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
@click.option('--practice', type=click.Choice(['1', '2', '3', 'all']),
              help='Show practice session results (1, 2, 3, or all)')
@click.option('--session', type=click.Choice(['race', 'qualifying', 'practice']),
              default='race', help='Type of session to show results for')
def result(practice, session):
    """Show the most recent F1 session results."""
    
    try:
        source = RaceResultSource()
        formatter = ResultFormatter()
        
        if practice or session == 'practice':
            # Handle practice sessions
            if practice == 'all':
                console.print("[bold blue]Fetching all practice session results...[/bold blue]")
                practice_results = source.fetch_practice_results()
            elif practice:
                practice_num = int(practice)
                console.print(f"[bold blue]Fetching Practice {practice_num} results...[/bold blue]")
                practice_results = source.fetch_practice_results(practice_num)
            else:
                console.print("[bold blue]Fetching all practice session results...[/bold blue]")
                practice_results = source.fetch_practice_results()
            
            if not practice_results:
                console.print("[yellow]No practice session results found.[/yellow]")
                return
            
            # Display each practice session
            for practice_result in practice_results:
                formatter.format_results(practice_result)
                console.print()  # Add spacing between sessions
        else:
            # Handle race/qualifying sessions (existing behavior)
            console.print("[bold blue]Fetching latest F1 race results...[/bold blue]")
            race_results = source.fetch_latest_results()
            formatter.format_results(race_results)
        
    except Exception as e:
        console.print(f"[red]Error fetching session results: {e}[/red]")


if __name__ == '__main__':
    main()