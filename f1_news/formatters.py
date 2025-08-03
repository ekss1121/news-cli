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
        """Display news items in a rich terminal format with detailed panels."""
        if not news_items:
            console.print("[yellow]No news items found.[/yellow]")
            return
        
        # Display header
        console.print(f"\n[bold blue]📰 F1 News ({len(news_items)} items)[/bold blue]\n")
        
        # Show detailed view for each news item
        for i, item in enumerate(news_items, 1):
            # Extract keywords for this item
            keywords = extract_keywords(item.content + " " + item.title, 5)
            
            # Format timestamp
            time_str = item.timestamp.strftime("%Y-%m-%d %H:%M") if item.timestamp else "Unknown time"
            
            # Format source
            source_str = f" • {item.source}" if item.source else ""
            
            # Clean content - remove HTML tags and truncate
            clean_content = re.sub(r'<[^>]+>', '', item.content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            # Show more content but still truncate if very long
            content_preview = clean_content[:400] + "..." if len(clean_content) > 400 else clean_content
            
            # Create the panel content
            panel_content = f"[bold]{item.title}[/bold]\n"
            panel_content += f"[dim]{time_str}{source_str}[/dim]\n"
            if keywords:
                panel_content += f"[cyan]Keywords: {', '.join(keywords)}[/cyan]\n"
            panel_content += f"\n{content_preview}\n"
            panel_content += f"\n[link={item.url}]🔗 Read full article[/link]"
            
            # Create panel with item number
            panel = Panel(
                panel_content,
                title=f"News Item #{i}",
                title_align="left",
                expand=False,
                border_style="blue"
            )
            console.print(panel)
            
            # Add spacing between items (except after the last one)
            if i < len(news_items):
                console.print("")


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
        
        # Results table with different columns for qualifying vs race/practice
        table = Table(title=f"{session_type} Results")
        table.add_column("Pos", style="bold white", width=4)
        table.add_column("Driver", style="magenta", width=20)
        table.add_column("Team", style="cyan", width=25)
        
        # Different columns for qualifying vs other sessions
        if session_type == "Qualifying":
            table.add_column("Best Time", style="yellow", width=15)
            table.add_column("Gap", style="red", width=12)
        else:
            table.add_column("Time", style="yellow", width=15)
            table.add_column("Points", style="green", width=8)
            table.add_column("Fastest Lap", style="red", width=12)
        
        if session_type == "Qualifying":
            # For qualifying, find the fastest overall time and calculate gaps
            fastest_overall_time = None
            fastest_time_seconds = float('inf')
            
            # Find the fastest qualifying time (position 1)
            if race_results.results:
                pole_result = race_results.results[0]  # Position 1 should be fastest
                if pole_result.fastest_lap:
                    try:
                        parts = pole_result.fastest_lap.split(':')
                        if len(parts) == 2:
                            minutes = int(parts[0])
                            seconds = float(parts[1])
                            fastest_time_seconds = minutes * 60 + seconds
                            fastest_overall_time = pole_result.fastest_lap
                    except:
                        pass
            
            for result in race_results.results:
                # For qualifying, use fastest_lap as the qualifying time
                best_time = result.fastest_lap if result.fastest_lap else "No time"
                
                # Calculate gap to pole position
                gap_display = ""
                if result.position == 1:
                    gap_display = "Pole"
                elif result.fastest_lap and fastest_time_seconds != float('inf'):
                    try:
                        parts = result.fastest_lap.split(':')
                        if len(parts) == 2:
                            minutes = int(parts[0])
                            seconds = float(parts[1])
                            driver_time_seconds = minutes * 60 + seconds
                            gap_seconds = driver_time_seconds - fastest_time_seconds
                            if gap_seconds >= 1:
                                gap_display = f"+{gap_seconds:.3f}s"
                            else:
                                gap_display = f"+{gap_seconds:.3f}s"
                    except:
                        gap_display = ""
                
                # Highlight pole position in purple
                if result.position == 1 and best_time:
                    best_time = f"[purple]{best_time}[/purple]"
                
                table.add_row(
                    str(result.position),
                    result.driver,
                    result.team,
                    best_time,
                    gap_display
                )
        else:
            # For race/practice sessions, find the overall fastest lap time
            fastest_overall = None
            fastest_time = float('inf')
            for result in race_results.results:
                if result.fastest_lap:  # If driver has a fastest lap time
                    # Parse time string to compare (format: "M:SS.sss")
                    try:
                        parts = result.fastest_lap.split(':')
                        if len(parts) == 2:
                            minutes = int(parts[0])
                            seconds = float(parts[1])
                            total_seconds = minutes * 60 + seconds
                            if total_seconds < fastest_time:
                                fastest_time = total_seconds
                                fastest_overall = result.fastest_lap
                    except:
                        pass
            
            for result in race_results.results:
                # Highlight the overall fastest lap in purple
                fastest_lap_display = result.fastest_lap
                if result.fastest_lap == fastest_overall:
                    fastest_lap_display = f"[purple]{result.fastest_lap}[/purple]"
                
                table.add_row(
                    str(result.position),
                    result.driver,
                    result.team,
                    result.time,
                    str(result.points),
                    fastest_lap_display
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