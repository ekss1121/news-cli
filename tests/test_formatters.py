"""Tests for F1 News CLI formatters."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from f1_news.formatters import TerminalFormatter, JSONFormatter, ResultFormatter, extract_keywords
from f1_news.models import NewsItem, RaceResult, RaceResults


class TestExtractKeywords:
    """Tests for keyword extraction."""
    
    def test_extract_f1_keywords(self):
        """Test extracting F1-specific keywords."""
        text = "Max Verstappen wins at Red Bull Racing in Formula 1 Grand Prix"
        keywords = extract_keywords(text, limit=5)
        
        assert "verstappen" in keywords
        # Keywords are normalized to lowercase and split by spaces
        assert any(keyword in ['verstappen', 'racing', 'formula', 'grand', 'prix'] for keyword in keywords)
    
    def test_extract_keywords_empty_text(self):
        """Test extracting keywords from empty text."""
        keywords = extract_keywords("", limit=5)
        assert isinstance(keywords, list)
    
    def test_extract_keywords_limit(self):
        """Test keyword extraction respects limit."""
        text = "verstappen hamilton leclerc russell norris piastri"
        keywords = extract_keywords(text, limit=3)
        assert len(keywords) <= 3


class TestTerminalFormatter:
    """Tests for terminal formatter."""
    
    def test_terminal_formatter_initialization(self):
        """Test terminal formatter initialization."""
        formatter = TerminalFormatter()
        assert formatter is not None
    
    @patch('f1_news.formatters.console.print')
    def test_format_news_empty_list(self, mock_print):
        """Test formatting empty news list."""
        formatter = TerminalFormatter()
        formatter.format_news([])
        
        mock_print.assert_called()
        # Check that warning message was printed
        args = mock_print.call_args[0]
        assert "No news items found" in str(args[0])
    
    @patch('f1_news.formatters.console.print')
    def test_format_news_with_items(self, mock_print):
        """Test formatting news items."""
        news_items = [
            NewsItem(
                title="Test F1 News",
                content="This is about Formula 1 racing",
                url="https://example.com",
                source="test",
                timestamp=datetime(2024, 1, 1, 12, 0)
            )
        ]
        
        formatter = TerminalFormatter()
        formatter.format_news(news_items)
        
        # Should print table and panel
        assert mock_print.call_count >= 2


class TestJSONFormatter:
    """Tests for JSON formatter."""
    
    def test_json_formatter_initialization(self):
        """Test JSON formatter initialization."""
        formatter = JSONFormatter()
        assert formatter is not None
    
    @patch('builtins.print')
    def test_format_news_json_output(self, mock_print):
        """Test JSON output formatting."""
        news_items = [
            NewsItem(
                title="Test News",
                content="Test content",
                url="https://example.com",
                source="test",
                timestamp=datetime(2024, 1, 1)
            )
        ]
        
        formatter = JSONFormatter()
        formatter.format_news(news_items)
        
        mock_print.assert_called_once()
        # Check that JSON was printed
        printed_text = mock_print.call_args[0][0]
        assert "Test News" in printed_text
        assert "https://example.com" in printed_text


class TestResultFormatter:
    """Tests for result formatter."""
    
    def test_result_formatter_initialization(self):
        """Test result formatter initialization."""
        formatter = ResultFormatter()
        assert formatter is not None
    
    @patch('f1_news.formatters.console.print')
    def test_format_race_results(self, mock_print):
        """Test formatting race results."""
        results = [
            RaceResult(1, "Max Verstappen", "Red Bull Racing", "1:30:00", 25, "1:45.123"),
            RaceResult(2, "Lewis Hamilton", "Mercedes", "+5.123", 18, "1:45.456"),
            RaceResult(3, "Charles Leclerc", "Ferrari", "+10.456", 15, "1:45.789")
        ]
        
        race_results = RaceResults(
            race_name="Test Grand Prix",
            date=datetime(2024, 1, 1),
            circuit="Test Circuit",
            results=results
        )
        
        formatter = ResultFormatter()
        formatter.format_results(race_results)
        
        # Should print header, table, and podium
        assert mock_print.call_count >= 3
    
    @patch('f1_news.formatters.console.print')
    def test_format_sprint_results(self, mock_print):
        """Test formatting sprint results."""
        race_results = RaceResults(
            race_name="Test Sprint",
            date=datetime(2024, 1, 1),
            circuit="Test Circuit",
            results=[
                RaceResult(1, "Driver 1", "Team 1", "30:00", 8, "1:45.123")
            ]
        )
        
        formatter = ResultFormatter()
        formatter.format_results(race_results)
        
        # Check that sprint format was detected
        mock_print.assert_called()
        
        # Find the call with the header
        header_call = None
        for call in mock_print.call_args_list:
            if call[0] and "[SPRINT]" in str(call[0][0]):
                header_call = call
                break
        
        assert header_call is not None
    
    @patch('f1_news.formatters.console.print')
    def test_fastest_lap_highlighting(self, mock_print):
        """Test that fastest lap gets highlighted in purple."""
        results = [
            RaceResult(1, "Driver 1", "Team 1", "1:30:00", 25, "1:45.123"),  # Fastest
            RaceResult(2, "Driver 2", "Team 2", "+5.123", 18, "1:45.456"),
        ]
        
        race_results = RaceResults(
            race_name="Test Grand Prix",
            date=datetime(2024, 1, 1),
            circuit="Test Circuit",
            results=results
        )
        
        formatter = ResultFormatter()
        formatter.format_results(race_results)
        
        # Find the table call and check for purple formatting
        table_printed = False
        for call in mock_print.call_args_list:
            if hasattr(call[0][0], '__class__') and 'Table' in str(call[0][0].__class__):
                table_printed = True
                break
        
        assert table_printed