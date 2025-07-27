import tweepy
import praw
import feedparser
import requests
import json
from datetime import datetime
from typing import List
from .models import NewsItem, RaceResults, RaceResult


class TwitterSource:
    """Fetch F1 news from Twitter/X."""
    
    def __init__(self):
        # Twitter API credentials would be loaded from config
        self.api = None
        
    def fetch_news(self, limit: int = 10) -> List[NewsItem]:
        """Fetch F1 news from Twitter."""
        # For now, return mock data
        return [
            NewsItem(
                title="Mock Twitter F1 News",
                content="This is a mock Twitter post about F1.",
                url="https://twitter.com/mock",
                source="twitter",
                author="@f1",
                timestamp=datetime.now()
            )
        ]


class RedditSource:
    """Fetch F1 news from Reddit."""
    
    def __init__(self):
        # Reddit API credentials would be loaded from config
        self.reddit = None
        
    def fetch_news(self, limit: int = 10) -> List[NewsItem]:
        """Fetch F1 news from Reddit."""
        # For now, return mock data
        return [
            NewsItem(
                title="Mock Reddit F1 News",
                content="This is a mock Reddit post about Formula 1.",
                url="https://reddit.com/r/formula1/mock",
                source="reddit",
                author="u/f1fan",
                timestamp=datetime.now()
            )
        ]


class RSSSource:
    """Fetch F1 news from RSS feeds."""
    
    def __init__(self):
        self.rss_feeds = [
            "https://www.formula1.com/en/latest/headlines.xml",
            "https://www.autosport.com/rss/feed/f1",
        ]
        
    def fetch_news(self, limit: int = 10) -> List[NewsItem]:
        """Fetch F1 news from RSS feeds."""
        news_items = []
        
        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:limit]:
                    news_item = NewsItem(
                        title=entry.title,
                        content=getattr(entry, 'summary', ''),
                        url=entry.link,
                        source=f"rss_{feed.feed.title}" if hasattr(feed.feed, 'title') else "rss",
                        timestamp=datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else None
                    )
                    news_items.append(news_item)
            except Exception as e:
                print(f"Error fetching RSS feed {feed_url}: {e}")
        
        return news_items[:limit]


class RaceResultSource:
    """Fetch F1 race results from OpenF1 API."""
    
    def __init__(self):
        # Using OpenF1 API for F1 data (free and reliable)
        self.base_url = "https://api.openf1.org/v1"
        
    def fetch_latest_results(self) -> RaceResults:
        """Fetch the most recent session results (Race, Qualifying, Sprint, etc.)."""
        try:
            current_year = datetime.now().year
            
            # Session types to try in order of preference
            session_types = ['Race', 'Qualifying', 'Sprint', 'Practice']
            
            # Get all sessions for current year only
            sessions_response = requests.get(f"{self.base_url}/sessions?year={current_year}")
            sessions_response.raise_for_status()
            year_sessions = sessions_response.json()
            
            # Filter for completed sessions (sessions that have ended)
            now = datetime.utcnow()
            completed_sessions = [
                session for session in year_sessions 
                if datetime.fromisoformat(session['date_end'].replace('Z', '+00:00')).replace(tzinfo=None) < now
            ]
            
            latest_session = None
            if completed_sessions:
                # Try to find the most recent session of preferred types
                for session_type in session_types:
                    if session_type == 'Sprint':
                        # Sprint sessions have session_type="Race" but session_name="Sprint"
                        type_sessions = [s for s in completed_sessions 
                                       if s['session_type'] == 'Race' and s['session_name'] == 'Sprint']
                    else:
                        # Regular sessions match by session_type
                        type_sessions = [s for s in completed_sessions 
                                       if s['session_type'] == session_type and s['session_name'] != 'Sprint']
                    
                    if type_sessions:
                        latest_session = type_sessions[-1]  # Most recent of this type
                        break
            
            if not latest_session:
                raise Exception(f"No completed sessions found for {current_year}")
            
            session_key = latest_session['session_key']
            
            # Get final positions (latest timestamp for each driver)
            positions_response = requests.get(f"{self.base_url}/position?session_key={session_key}")
            positions_response.raise_for_status()
            positions_data = positions_response.json()
            
            # Get driver information
            drivers_response = requests.get(f"{self.base_url}/drivers?session_key={session_key}")
            drivers_response.raise_for_status()
            drivers_data = drivers_response.json()
            
            # Get lap data and calculate total race times
            race_times = {}
            try:
                laps_response = requests.get(f"{self.base_url}/laps?session_key={session_key}")
                laps_response.raise_for_status()
                laps_data = laps_response.json()
                
                # Calculate total race time for each driver
                for lap in laps_data:
                    driver_num = lap['driver_number']
                    if driver_num not in race_times:
                        race_times[driver_num] = 0
                    if lap.get('lap_duration'):
                        race_times[driver_num] += lap['lap_duration']
                
                # Find winner's time for gap calculations
                winner_time = min(race_times.values()) if race_times else 0
                
                # Calculate fastest lap for each driver
                driver_fastest_laps = {}
                for lap in laps_data:
                    driver_num = lap['driver_number']
                    lap_time = lap.get('lap_duration')
                    if lap_time:
                        if driver_num not in driver_fastest_laps or lap_time < driver_fastest_laps[driver_num]:
                            driver_fastest_laps[driver_num] = lap_time
                
            except Exception as e:
                print(f"Warning: Could not fetch lap data: {e}")
                race_times = {}
                winner_time = 0
                driver_fastest_laps = {}
            
            # Create driver lookup
            driver_lookup = {driver['driver_number']: driver for driver in drivers_data}
            
            # Get final positions (group by driver and get latest position)
            final_positions = {}
            for pos in positions_data:
                driver_num = pos['driver_number']
                date = pos['date']
                if driver_num not in final_positions or date > final_positions[driver_num]['date']:
                    final_positions[driver_num] = pos
            
            # Create results
            results = []
            points_table = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1] + [0] * 10  # F1 points system
            
            for driver_num, pos_data in final_positions.items():
                if driver_num in driver_lookup:
                    driver_info = driver_lookup[driver_num]
                    position = pos_data['position']
                    
                    # Calculate points
                    points = points_table[position - 1] if position <= len(points_table) else 0
                    
                    # Format race time display
                    time_display = f"P{position}"  # Default fallback
                    if driver_num in race_times and race_times[driver_num] > 0:
                        total_time = race_times[driver_num]
                        
                        if position == 1:
                            # Winner gets total race time
                            minutes = int(total_time // 60)
                            seconds = total_time % 60
                            time_display = f"{minutes}:{seconds:06.3f}"
                        else:
                            # Others get gap to winner
                            gap = total_time - winner_time
                            if gap >= 60:
                                gap_minutes = int(gap // 60)
                                gap_seconds = gap % 60
                                time_display = f"+{gap_minutes}:{gap_seconds:06.3f}"
                            else:
                                time_display = f"+{gap:.3f}"
                    
                    # Format fastest lap time
                    fastest_lap_display = ""
                    if driver_num in driver_fastest_laps:
                        fl_time = driver_fastest_laps[driver_num]
                        fl_minutes = int(fl_time // 60)
                        fl_seconds = fl_time % 60
                        fastest_lap_display = f"{fl_minutes}:{fl_seconds:06.3f}"
                    
                    race_result = RaceResult(
                        position=position,
                        driver=driver_info['full_name'],
                        team=driver_info['team_name'],
                        time=time_display,
                        points=points,
                        fastest_lap=fastest_lap_display
                    )
                    results.append(race_result)
            
            # Sort by position
            results.sort(key=lambda x: x.position)
            
            # Parse session info
            session_type = latest_session['session_type']
            session_name_api = latest_session['session_name']
            
            # Determine the actual session type (Sprint races have session_type="Race" but session_name="Sprint")
            if session_name_api == 'Sprint':
                session_name = f"{latest_session['country_name']} Sprint"
            elif session_type == 'Race':
                session_name = f"{latest_session['country_name']} Grand Prix"
            else:
                session_name = f"{latest_session['country_name']} {session_type}"
            
            date = datetime.fromisoformat(latest_session['date_start'].replace('Z', '+00:00'))
            circuit = latest_session['location']
            
            return RaceResults(
                race_name=session_name,
                date=date,
                circuit=circuit,
                results=results
            )
            
        except Exception as e:
            print(f"OpenF1 API Error: {e}")
            # Return mock data if API fails
            return RaceResults(
                race_name="Mock Grand Prix (API Error)",
                date=datetime.now(),
                circuit="Mock Circuit",
                results=[
                    RaceResult(1, "Max Verstappen", "Red Bull Racing", "1:32:28.851", 25, True),
                    RaceResult(2, "Sergio Pérez", "Red Bull Racing", "+22.896", 18, False),
                    RaceResult(3, "Charles Leclerc", "Ferrari", "+34.808", 15, False),
                    RaceResult(4, "Carlos Sainz", "Ferrari", "+47.036", 12, False),
                    RaceResult(5, "Lando Norris", "McLaren", "+1:13.715", 10, False),
                ]
            )