from typing import List
from .models import NewsItem


class NewsFilter:
    """Filter F1 news items based on various criteria."""
    
    F1_TEAMS = [
        'red bull', 'ferrari', 'mercedes', 'mclaren', 'aston martin',
        'alpine', 'williams', 'alphatauri', 'alfa romeo', 'haas'
    ]
    
    F1_DRIVERS = [
        'verstappen', 'perez', 'leclerc', 'sainz', 'hamilton', 'russell',
        'norris', 'piastri', 'alonso', 'stroll', 'gasly', 'ocon',
        'albon', 'sargeant', 'tsunoda', 'ricciardo', 'bottas', 'zhou',
        'magnussen', 'hulkenberg'
    ]
    
    def filter_by_team(self, news_items: List[NewsItem], team: str) -> List[NewsItem]:
        """Filter news items by F1 team."""
        team_lower = team.lower()
        filtered_items = []
        
        for item in news_items:
            if (team_lower in item.title.lower() or 
                team_lower in item.content.lower()):
                filtered_items.append(item)
        
        return filtered_items
    
    def filter_by_driver(self, news_items: List[NewsItem], driver: str) -> List[NewsItem]:
        """Filter news items by F1 driver."""
        driver_lower = driver.lower()
        filtered_items = []
        
        for item in news_items:
            if (driver_lower in item.title.lower() or 
                driver_lower in item.content.lower()):
                filtered_items.append(item)
        
        return filtered_items
    
    def filter_by_keyword(self, news_items: List[NewsItem], keyword: str) -> List[NewsItem]:
        """Filter news items by custom keyword."""
        keyword_lower = keyword.lower()
        filtered_items = []
        
        for item in news_items:
            if (keyword_lower in item.title.lower() or 
                keyword_lower in item.content.lower()):
                filtered_items.append(item)
        
        return filtered_items
    
    def deduplicate(self, news_items: List[NewsItem]) -> List[NewsItem]:
        """Remove duplicate news items based on title similarity."""
        seen_titles = set()
        unique_items = []
        
        for item in news_items:
            # Simple deduplication based on title
            title_key = item.title.lower().strip()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_items.append(item)
        
        return unique_items