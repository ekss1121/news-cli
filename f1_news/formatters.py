import json
import re
from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .models import NewsItem, RaceResults

console = Console()


def extract_keywords(text: str, limit: int = 5) -> List[str]:
    """Extract keywords from text content."""
    # F1-specific keywords
    f1_keywords = {
        'verstappen', 'hamilton', 'leclerc', 'russell', 'norris', 'piastri', 'sainz', 'perez',
        'alonso', 'stroll', 'ocon', 'gasly', 'albon', 'sargeant', 'bottas', 'zhou',
        'hulkenberg', 'magnussen', 'tsunoda', 'ricciardo',
        'red bull', 'mercedes', 'ferrari', 'mclaren', 'aston martin', 'alpine', 'williams',
        'haas', 'alphatauri', 'alfa romeo', 'racing', 'formula 1', 'f1', 'grand prix',
        'qualifying', 'practice', 'sprint', 'championship', 'points', 'podium', 'pole position',
        'fastest lap', 'drs', 'safety car', 'virtual safety car', 'pit stop', 'tyres', 'tires'
    }
    
    # Clean and normalize text
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    
    # Find F1 keywords in text
    found_keywords = []
    for word in words:
        if word in f1_keywords and word not in found_keywords:
            found_keywords.append(word)
            if len(found_keywords) >= limit:
                break
    
    # If we don't have enough F1 keywords, add common important words
    if len(found_keywords) < limit:
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'was', 'are', 'were', 'will', 'would', 'could', 'should'}
        for word in words:
            if (len(word) > 3 and word not in common_words and 
                word not in found_keywords and word.isalpha()):
                found_keywords.append(word)
                if len(found_keywords) >= limit:
                    break
    
    return found_keywords[:limit]


class TerminalFormatter:
    """Format news items for terminal display."""
    
    def format_news(self, news_items: List[NewsItem]):
        """Display news items in a rich terminal format."""
        if not news_items:
            console.print("[yellow]No news items found.[/yellow]")
            return
            
        table = Table(title="F1 News")
        table.add_column("Title", style="magenta")
        table.add_column("Keywords", style="cyan")
        table.add_column("Time", style="yellow")
        
        for item in news_items:
            keywords = extract_keywords(item.content + " " + item.title, 4)
            title_text = item.title[:60] + "..." if len(item.title) > 60 else item.title
            table.add_row(
                f"[link={item.url}]{title_text}[/link]",
                ", ".join(keywords) if keywords else "N/A",
                item.timestamp.strftime("%Y-%m-%d %H:%M") if item.timestamp else "Unknown"
            )
        
        console.print(table)
        
        # Show detailed view for first item
        if news_items:
            first_item = news_items[0]
            panel = Panel(
                f"[bold]{first_item.title}[/bold]\n\n{first_item.content[:200]}...\n\n[link={first_item.url}]Read more[/link]",
                title="Latest News Detail",
                expand=False
            )
            console.print(panel)


class JSONFormatter:
    """Format news items as JSON."""
    
    def format_news(self, news_items: List[NewsItem]):
        """Output news items as JSON."""
        json_data = []
        for item in news_items:
            keywords = extract_keywords(item.content + " " + item.title, 5)
            json_data.append({
                "title": item.title,
                "content": item.content,
                "url": item.url,
                "source": item.source,
                "author": item.author,
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
                "tags": item.tags,
                "keywords": keywords
            })
        
        print(json.dumps(json_data, indent=2))


class ResultFormatter:
    """Format race results for terminal display."""
    
    def format_results(self, race_results: RaceResults):
        """Display session results in a rich terminal format."""
        # Determine session type and emoji (Windows-safe)
        session_type = "Race"
        emoji = "[RACE]"
        if "Sprint" in race_results.race_name:
            session_type = "Sprint"
            emoji = "[SPRINT]"
        elif "Qualifying" in race_results.race_name:
            session_type = "Qualifying"
            emoji = "[QUALIFY]"
        elif "Practice" in race_results.race_name:
            session_type = "Practice"
            emoji = "[PRACTICE]"
        
        # Session header
        console.print(f"\n[bold blue]{emoji} {race_results.race_name}[/bold blue]")
        console.print(f"[yellow]Location: {race_results.circuit}[/yellow]")
        console.print(f"[green]Date: {race_results.date.strftime('%B %d, %Y')}[/green]\n")
        
        # Results table
        table = Table(title=f"{session_type} Results")
        table.add_column("Pos", style="bold white", width=4)
        table.add_column("Driver", style="magenta", width=20)
        table.add_column("Team", style="cyan", width=25)
        table.add_column("Time", style="yellow", width=15)
        table.add_column("Points", style="green", width=8)
        table.add_column("FL", style="red", width=3)  # Fastest Lap
        
        for result in race_results.results:
            fastest_lap_indicator = "*" if result.fastest_lap else ""
            table.add_row(
                str(result.position),
                result.driver,
                result.team,
                result.time,
                str(result.points),
                fastest_lap_indicator
            )
        
        console.print(table)
        
        # Show top finishers
        if len(race_results.results) >= 3:
            top_three = race_results.results[:3]
            if session_type == "Race":
                console.print(f"\n[bold yellow]Podium Finishers[/bold yellow]")
            elif session_type == "Qualifying":
                console.print(f"\n[bold yellow]Top Qualifiers[/bold yellow]")
            elif session_type == "Sprint":
                console.print(f"\n[bold yellow]Sprint Podium[/bold yellow]")
            else:
                console.print(f"\n[bold yellow]Top 3 Results[/bold yellow]")
            
            console.print(f"1st: {top_three[0].driver} ({top_three[0].team})")
            console.print(f"2nd: {top_three[1].driver} ({top_three[1].team})")
            console.print(f"3rd: {top_three[2].driver} ({top_three[2].team})")


class MarkdownFormatter:
    """Format news items as Markdown."""
    
    def format_news(self, news_items: List[NewsItem]):
        """Output news items as Markdown."""
        if not news_items:
            print("No news items found.")
            return
            
        print("# F1 News\n")
        
        for i, item in enumerate(news_items, 1):
            keywords = extract_keywords(item.content + " " + item.title, 5)
            print(f"## {i}. [{item.title}]({item.url})")
            print(f"**Keywords:** {', '.join(keywords) if keywords else 'N/A'}")
            if item.timestamp:
                print(f"**Time:** {item.timestamp.strftime('%Y-%m-%d %H:%M')}")
            print(f"\n{item.content}\n")
            print("---\n")