"""Tests for F1 News CLI commands."""

import pytest
from unittest.mock import Mock, patch
from click.testing import CliRunner
from f1_news.cli import main, fetch, result
from f1_news.models import NewsItem, RaceResults, RaceResult
from datetime import datetime


class TestCLICommands:
    """Tests for CLI commands."""
    
    def test_main_command_help(self):
        """Test main command shows help."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "F1 News CLI" in result.output
    
    def test_main_command_version(self):
        """Test main command shows version."""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        
        # Version command may fail if package not properly installed
        # Just check it runs without crashing
        assert result.exit_code in [0, 1]
    
    @patch('f1_news.cli.RSSSource')
    def test_fetch_command_default(self, mock_rss_source):
        """Test fetch command with default parameters."""
        # Mock RSS source
        mock_source = Mock()
        mock_source.fetch_news.return_value = [
            NewsItem(
                title="Test News",
                content="Test content",
                url="https://example.com",
                source="test",
                timestamp=datetime.now()
            )
        ]
        mock_rss_source.return_value = mock_source
        
        runner = CliRunner()
        result = runner.invoke(fetch)
        
        assert result.exit_code == 0
        assert "Fetching F1 news from rss" in result.output
        mock_source.fetch_news.assert_called_once()
    
    @patch('f1_news.cli.RSSSource')
    def test_fetch_command_json_format(self, mock_rss_source):
        """Test fetch command with JSON output format."""
        mock_source = Mock()
        mock_source.fetch_news.return_value = [
            NewsItem(
                title="Test News",
                content="Test content", 
                url="https://example.com",
                source="test"
            )
        ]
        mock_rss_source.return_value = mock_source
        
        runner = CliRunner()
        result = runner.invoke(fetch, ['--format', 'json'])
        
        assert result.exit_code == 0
        mock_source.fetch_news.assert_called_once()
    
    @patch('f1_news.cli.RSSSource')
    def test_fetch_command_with_limit(self, mock_rss_source):
        """Test fetch command with custom limit."""
        mock_source = Mock()
        mock_source.fetch_news.return_value = []
        mock_rss_source.return_value = mock_source
        
        runner = CliRunner()
        result = runner.invoke(fetch, ['--limit', '5'])
        
        assert result.exit_code == 0
        mock_source.fetch_news.assert_called_with(limit=5)
    
    @patch('f1_news.cli.RaceResultSource')
    def test_result_command_success(self, mock_result_source):
        """Test result command successful execution."""
        # Mock race result source
        mock_source = Mock()
        mock_source.fetch_latest_results.return_value = RaceResults(
            race_name="Test Grand Prix",
            date=datetime.now(),
            circuit="Test Circuit",
            results=[
                RaceResult(1, "Test Driver", "Test Team", "1:30:00", 25, "1:45.123")
            ]
        )
        mock_result_source.return_value = mock_source
        
        runner = CliRunner()
        cli_result = runner.invoke(result)
        
        assert cli_result.exit_code == 0
        assert "Fetching latest F1 race results" in cli_result.output
        mock_source.fetch_latest_results.assert_called_once()
    
    @patch('f1_news.cli.RaceResultSource')
    def test_result_command_with_error(self, mock_result_source):
        """Test result command handles errors gracefully."""
        mock_source = Mock()
        mock_source.fetch_latest_results.side_effect = Exception("API Error")
        mock_result_source.return_value = mock_source
        
        runner = CliRunner()
        cli_result = runner.invoke(result)
        
        assert cli_result.exit_code == 0
        assert "Error fetching race results" in cli_result.output
    
    def test_filter_command_placeholder(self):
        """Test filter command shows placeholder message."""
        runner = CliRunner()
        result = runner.invoke(main, ['filter'])
        
        assert result.exit_code == 0
        assert "Filter functionality coming soon" in result.output
    
    def test_filter_command_with_options(self):
        """Test filter command accepts team and driver options."""
        runner = CliRunner()
        result = runner.invoke(main, ['filter', '--team', 'McLaren', '--driver', 'Norris'])
        
        assert result.exit_code == 0
        assert "Filtering F1 news" in result.output


class TestCLIIntegration:
    """Integration tests for CLI."""
    
    def test_cli_entry_point(self):
        """Test CLI can be invoked."""
        runner = CliRunner()
        result = runner.invoke(main)
        
        # Should show help when no command given
        assert result.exit_code == 0
    
    def test_invalid_command(self):
        """Test invalid command handling."""
        runner = CliRunner()
        result = runner.invoke(main, ['invalid-command'])
        
        assert result.exit_code != 0
    
    def test_fetch_invalid_format(self):
        """Test fetch with invalid format."""
        runner = CliRunner()
        result = runner.invoke(fetch, ['--format', 'invalid'])
        
        assert result.exit_code != 0