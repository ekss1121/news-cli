"""Tests for F1 News CLI models."""

import pytest
from datetime import datetime
from f1_news.models import NewsItem, RaceResult, RaceResults


class TestNewsItem:
    """Tests for NewsItem model."""
    
    def test_news_item_creation(self):
        """Test creating a NewsItem."""
        item = NewsItem(
            title="Test F1 News",
            content="This is test content",
            url="https://example.com",
            source="test"
        )
        
        assert item.title == "Test F1 News"
        assert item.content == "This is test content"
        assert item.url == "https://example.com"
        assert item.source == "test"
        assert item.tags == []
    
    def test_news_item_with_optional_fields(self):
        """Test NewsItem with optional fields."""
        timestamp = datetime.now()
        item = NewsItem(
            title="Test News",
            content="Content",
            url="https://example.com",
            source="test",
            author="Test Author",
            timestamp=timestamp,
            tags=["F1", "Racing"]
        )
        
        assert item.author == "Test Author"
        assert item.timestamp == timestamp
        assert item.tags == ["F1", "Racing"]


class TestRaceResult:
    """Tests for RaceResult model."""
    
    def test_race_result_creation(self):
        """Test creating a RaceResult."""
        result = RaceResult(
            position=1,
            driver="Max Verstappen",
            team="Red Bull Racing",
            time="1:32:28.851",
            points=25,
            fastest_lap="1:45.123"
        )
        
        assert result.position == 1
        assert result.driver == "Max Verstappen"
        assert result.team == "Red Bull Racing"
        assert result.time == "1:32:28.851"
        assert result.points == 25
        assert result.fastest_lap == "1:45.123"
    
    def test_race_result_defaults(self):
        """Test RaceResult with default values."""
        result = RaceResult(
            position=10,
            driver="Test Driver",
            team="Test Team",
            time="+1:23.456",
            points=0
        )
        
        assert result.fastest_lap == ""


class TestRaceResults:
    """Tests for RaceResults model."""
    
    def test_race_results_creation(self):
        """Test creating RaceResults."""
        date = datetime.now()
        results = [
            RaceResult(1, "Driver 1", "Team 1", "1:30:00", 25),
            RaceResult(2, "Driver 2", "Team 2", "+5.123", 18)
        ]
        
        race_results = RaceResults(
            race_name="Test Grand Prix",
            date=date,
            circuit="Test Circuit",
            results=results
        )
        
        assert race_results.race_name == "Test Grand Prix"
        assert race_results.date == date
        assert race_results.circuit == "Test Circuit"
        assert len(race_results.results) == 2
        assert race_results.results[0].position == 1
        assert race_results.results[1].position == 2