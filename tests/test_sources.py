"""Tests for F1 News CLI sources."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from f1_news.sources import RSSSource, RaceResultSource
from f1_news.models import NewsItem, RaceResults


class TestRSSSource:
    """Tests for RSS source."""
    
    def test_rss_source_initialization(self):
        """Test RSS source initialization."""
        source = RSSSource()
        assert len(source.rss_feeds) > 0
        assert "formula1.com" in source.rss_feeds[0]
    
    @patch('f1_news.sources.feedparser.parse')
    def test_fetch_news_success(self, mock_parse):
        """Test successful RSS news fetching."""
        # Mock feedparser response
        mock_entry = Mock()
        mock_entry.title = "Test F1 News"
        mock_entry.summary = "Test summary"
        mock_entry.link = "https://example.com"
        mock_entry.published_parsed = (2024, 1, 1, 12, 0, 0, 0, 1, 0)
        
        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_feed.feed.title = "Test Feed"
        
        mock_parse.return_value = mock_feed
        
        source = RSSSource()
        news_items = source.fetch_news(limit=1)
        
        # Should return at least one item from each RSS feed that works
        assert len(news_items) >= 1
        assert news_items[0].title == "Test F1 News"
        assert news_items[0].content == "Test summary"
        assert news_items[0].url == "https://example.com"
    
    @patch('f1_news.sources.feedparser.parse')
    def test_fetch_news_with_error(self, mock_parse):
        """Test RSS fetching with error handling."""
        mock_parse.side_effect = Exception("Network error")
        
        source = RSSSource()
        news_items = source.fetch_news(limit=5)
        
        # Should return empty list when all feeds fail
        assert isinstance(news_items, list)


class TestRaceResultSource:
    """Tests for race result source."""
    
    def test_race_result_source_initialization(self):
        """Test race result source initialization."""
        source = RaceResultSource()
        assert source.base_url == "https://api.openf1.org/v1"
    
    @patch('f1_news.sources.requests.get')
    def test_fetch_latest_results_success(self, mock_get):
        """Test successful race results fetching."""
        # Mock API responses
        sessions_response = Mock()
        sessions_response.json.return_value = [
            {
                'session_key': 123,
                'session_type': 'Race',
                'session_name': 'Race',
                'country_name': 'Test',
                'location': 'Test Circuit',
                'date_start': '2024-01-01T13:00:00+00:00',
                'date_end': '2024-01-01T15:00:00+00:00'
            }
        ]
        sessions_response.raise_for_status.return_value = None
        
        positions_response = Mock()
        positions_response.json.return_value = [
            {
                'driver_number': 1,
                'position': 1,
                'date': '2024-01-01T15:00:00+00:00'
            }
        ]
        positions_response.raise_for_status.return_value = None
        
        drivers_response = Mock()
        drivers_response.json.return_value = [
            {
                'driver_number': 1,
                'full_name': 'Test Driver',
                'team_name': 'Test Team'
            }
        ]
        drivers_response.raise_for_status.return_value = None
        
        laps_response = Mock()
        laps_response.json.return_value = [
            {
                'driver_number': 1,
                'lap_duration': 90.123
            }
        ]
        laps_response.raise_for_status.return_value = None
        
        # Configure mock to return different responses based on URL
        def mock_get_side_effect(url):
            if '/sessions' in url:
                return sessions_response
            elif '/position' in url:
                return positions_response
            elif '/drivers' in url:
                return drivers_response
            elif '/laps' in url:
                return laps_response
            return Mock()
        
        mock_get.side_effect = mock_get_side_effect
        
        source = RaceResultSource()
        with patch('f1_news.sources.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 2)  # After race
            mock_datetime.utcnow.return_value = datetime(2024, 1, 2)
            mock_datetime.fromisoformat = datetime.fromisoformat
            
            results = source.fetch_latest_results()
        
        assert isinstance(results, RaceResults)
        assert "Test" in results.race_name
        assert results.circuit == "Test Circuit"
        assert len(results.results) > 0
    
    @patch('f1_news.sources.requests.get')
    def test_fetch_latest_results_api_error(self, mock_get):
        """Test race results fetching with API error."""
        mock_get.side_effect = Exception("API Error")
        
        source = RaceResultSource()
        results = source.fetch_latest_results()
        
        # Should return mock data when API fails
        assert isinstance(results, RaceResults)
        assert "Mock Grand Prix" in results.race_name
        assert len(results.results) > 0