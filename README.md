# 🏎️ F1 News CLI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![F1](https://img.shields.io/badge/Formula%201-🏁-red.svg)](https://www.formula1.com/)

A powerful command-line tool to fetch the latest Formula 1 news, race results, and practice session data directly in your terminal with beautiful, detailed displays.

## ✨ Features

- **📰 Multi-Source F1 News**: Fetch real-time F1 news from multiple sources (Formula1.com, Autosport, Motorsport.com, ESPN)
- **🏁 Complete Session Results**: Race, qualifying, sprint, and **practice session** results
- **🎨 Rich Detailed Display**: Beautiful terminal panels with full news content (not just tables)
- **📊 Multiple Output Formats**: Terminal, JSON, or Markdown formats
- **🔍 Advanced Filtering**: Filter news by teams, drivers, or custom keywords
- **🎯 Source Selection**: Choose specific news sources or use all
- **⚡ Default Command**: No need to type "fetch" - just use `f1-news` directly
- **🏃‍♂️ Practice Sessions**: View detailed practice session results (FP1, FP2, FP3)
- **🚀 Fast & Lightweight**: Minimal dependencies, maximum performance

## 🛠️ Installation

### Option 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/f1-news-cli.git
cd f1-news-cli

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Option 2: Direct Installation

```bash
pip install click feedparser rich requests python-dateutil
```

## 🚀 Quick Start

Once installed, you can use the `f1-news` command anywhere in your terminal:

```bash
# Get help
f1-news --help

# Fetch latest F1 news (default command - no need for "fetch"!)
f1-news
f1-news --limit 5

# Get latest race results
f1-news result

# Get practice session results  
f1-news result --practice all

# Filter news by team
f1-news --team ferrari --limit 3

# Use specific news sources
f1-news --sources motorsport,autosport --limit 5
```

## 📖 User Guide

### 1. Fetching F1 News (Default Command)

The default behavior fetches the latest F1 news - no need to type "fetch":

```bash
# Basic usage - get 10 latest news items
f1-news

# Limit the number of articles  
f1-news --limit 5

# Filter by team, driver, or keyword
f1-news --team mclaren --limit 3
f1-news --driver verstappen
f1-news --keyword "championship"

# Choose specific news sources
f1-news --sources formula1_headlines,motorsport

# Change output format
f1-news --format json
f1-news --format markdown
f1-news --format terminal  # default

# Still works with explicit "fetch" command
f1-news fetch --limit 5
```

#### Example Output (New Detailed Format):
```
📰 F1 News (3 items)

╭─ News Item #1 ───────────────────────────────────────────────────────────────╮
│ Verstappen confused by tough start to F1 Hungarian GP weekend                │
│ 2025-08-01 17:54 • Autosport                                                 │
│ Keywords: verstappen, norris, haas, tsunoda, f1                              │
│                                                                              │
│ Max Verstappen has said "nothing really works" on his Red Bull Formula 1 car │
│ as he finished the Hungarian Grand Prix's Friday sessions adrift of the      │
│ frontrunners. Verstappen finished the afternoon's FP2 session in a lowly...  │
│                                                                              │
│ 🔗 Read full article                                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### 2. Multiple News Sources

The CLI now supports multiple news sources:

```bash
# List available sources
f1-news sources

# Use specific sources
f1-news --sources motorsport,autosport
f1-news --sources formula1_headlines

# Use all sources (default)
f1-news
```

#### Available Sources:
- **formula1_headlines** - Formula 1 Official (Headlines)
- **formula1_all** - Formula 1 Official (All Content) 
- **autosport** - Autosport
- **motorsport** - Motorsport.com
- **espn** - ESPN Motorsports

### 3. Advanced Filtering

```bash
# Filter by F1 team
f1-news --team ferrari
f1-news --team "red bull"

# Filter by driver  
f1-news --driver verstappen
f1-news --driver hamilton

# Filter by custom keyword
f1-news --keyword "championship"
f1-news --keyword "safety car"

# Combine filters
f1-news --team mclaren --driver norris

# Use dedicated filter command
f1-news filter --team ferrari --driver leclerc
```

### 4. Getting Session Results

The `result` command fetches race, qualifying, and **practice session** results:

```bash
# Get latest race/qualifying results (default)
f1-news result

# Get specific practice session
f1-news result --practice 1    # FP1 only
f1-news result --practice 2    # FP2 only  
f1-news result --practice 3    # FP3 only

# Get all practice sessions
f1-news result --practice all
f1-news result --session practice

# Session type selection
f1-news result --session race        # Default
f1-news result --session qualifying
f1-news result --session practice
```

#### Example Practice Results:
```
[PRACTICE] Hungary Practice 1
Location: Budapest
Date: August 01, 2025

                                Practice Results                                
┏━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━┓
┃  ┃ Driver           ┃ Team                  ┃ Time        ┃ Poi… ┃ Fastest   ┃
┃  ┃                  ┃                       ┃             ┃      ┃ Lap       ┃
┡━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━┩
│ 1│ Lando NORRIS     │ McLaren               │ 1:16.052    │ 0    │ 1:16.052  │
│ 2│ Oscar PIASTRI    │ McLaren               │ 1:16.071    │ 0    │ 1:16.071  │
│ 3│ Charles LECLERC  │ Ferrari               │ 1:16.269    │ 0    │ 1:16.269  │
└──┴──────────────────┴───────────────────────┴─────────────┴──────┴───────────┘

Top 3 Results
1st: Lando NORRIS (McLaren)
2nd: Oscar PIASTRI (McLaren) 
3rd: Charles LECLERC (Ferrari)
```

### 5. Output Formats

#### Terminal Format (Default)
Rich, detailed panels with full article content - perfect for interactive use.

#### JSON Format
```bash
f1-news --format json
```
```json
[
  {
    "title": "Verstappen confused by tough start to F1 Hungarian GP weekend",
    "content": "Max Verstappen has said \"nothing really works\"...",
    "url": "https://www.autosport.com/f1/news/...",
    "source": "Autosport",
    "timestamp": "2025-08-01T17:54:49",
    "keywords": ["verstappen", "norris", "haas", "tsunoda", "f1"]
  }
]
```

#### Markdown Format
```bash
f1-news --format markdown
```
Perfect for documentation or saving to files.

## 🔧 Configuration

### News Sources
The CLI fetches news from multiple RSS feeds:
- **Formula1.com** - Official F1 news (headlines and all content)
- **Autosport.com** - F1 journalism and analysis
- **Motorsport.com** - Comprehensive F1 coverage
- **ESPN** - Motorsports news

### Race & Practice Data
Live session results are fetched from the [OpenF1 API](https://openf1.org/) - a free, real-time F1 data service providing:
- Race results with timing data
- Qualifying session results  
- Practice session results (FP1, FP2, FP3)
- Fastest lap information
- Live timing data

## 🚀 Advanced Usage

### Combining Commands & Options
```bash
# Get McLaren news and save to file
f1-news --team mclaren --format markdown > mclaren_news.md

# Get practice results as JSON
f1-news result --practice all --format json

# Daily F1 update with news and results
f1-news --limit 5 && f1-news result

# Specific source with filtering
f1-news --sources motorsport --driver verstappen --limit 3
```

### Integration Examples

#### Use in Scripts
```bash
#!/bin/bash
echo "=== Daily F1 Update ==="
f1-news --limit 5
echo ""
echo "=== Latest Practice Results ==="
f1-news result --practice all
echo ""
echo "=== Latest Race Results ==="
f1-news result
```

#### Cron Job for Daily Updates
```bash
# Add to crontab for daily F1 updates
0 9 * * * /usr/local/bin/f1-news --limit 10 > ~/f1_daily.txt
0 18 * * FRI /usr/local/bin/f1-news result --practice all > ~/f1_practice.txt
```

## 🛠️ Development

### Project Structure
```
f1-news-cli/
├── f1_news/
│   ├── __init__.py
│   ├── cli.py          # Main CLI interface with default command
│   ├── models.py       # Data models (NewsItem, RaceResult)
│   ├── sources.py      # Multi-source news and race data
│   ├── formatters.py   # Enhanced output formatting
│   ├── filters.py      # Advanced news filtering logic
│   └── config.py       # Configuration (future)
├── requirements.txt    # Dependencies
├── setup.py           # Package configuration
└── README.md          # This file
```

### Running from Source
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/f1-news-cli.git
cd f1-news-cli
pip install -r requirements.txt

# Run directly (new default command)
python -m f1_news.cli --limit 5
python -m f1_news.cli result --practice 1

# Or explicit commands
python -m f1_news.cli fetch --team ferrari
python -m f1_news.cli filter --driver verstappen
```

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Run linting: `python -m pycodestyle f1_news/`
5. Submit a pull request

## 📊 Dependencies

- **click** - Command-line interface framework
- **rich** - Rich terminal formatting and panels
- **feedparser** - RSS feed parsing for news sources
- **requests** - HTTP requests for APIs (OpenF1)
- **python-dateutil** - Date/time parsing and formatting

## 🐛 Troubleshooting

### Common Issues

**Command not found after installation:**
```bash
# Make sure pip install location is in PATH
pip show f1-news-cli
# Or run directly
python -m f1_news.cli
```

**No practice results showing:**
- The CLI shows the most recent completed practice sessions
- Practice sessions are only available during F1 weekends
- Check your internet connection for OpenF1 API access

**No race results showing:**
- The CLI shows the most recent completed session
- If no recent sessions, it falls back to mock data
- Check your internet connection for API access

**RSS feeds not loading:**
- Some feeds occasionally have temporary outages
- The CLI will show available data from working feeds
- Try using specific sources: `f1-news --sources autosport,motorsport`

**Invalid source errors:**
```bash
# List available sources
f1-news sources
# Use correct source names
f1-news --sources formula1_headlines,autosport
```

### Debug Mode
```bash
# Run with Python for detailed error messages
python -m f1_news.cli --limit 5
python -m f1_news.cli result --practice all
```

## 🗺️ Roadmap

### Recently Added ✅
- **Multi-source news** - Formula1.com, Autosport, Motorsport.com, ESPN
- **Practice session results** - FP1, FP2, FP3 with detailed timing
- **Default command** - No need to type "fetch"
- **Enhanced filtering** - Team, driver, keyword filtering
- **Detailed news display** - Full content panels instead of tables
- **Source selection** - Choose specific news sources

### Coming Soon 🚧
- [ ] **Qualifying session results** - Dedicated qualifying results display
- [ ] **Live timing during sessions** - Real-time updates during F1 weekends
- [ ] **Driver standings** - Championship points and standings
- [ ] **Historical data access** - Past seasons and results
- [ ] **Configuration file** - Customize sources and preferences
- [ ] **Caching system** - Offline support and faster queries
- [ ] **Social media integration** - Twitter and Reddit sources

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenF1 API](https://openf1.org/) - Free, real-time F1 data for race and practice results
- [Formula1.com](https://formula1.com/) - Official F1 news RSS feeds
- [Autosport.com](https://autosport.com/) - Professional F1 journalism and analysis  
- [Motorsport.com](https://motorsport.com/) - Comprehensive motorsport coverage
- The amazing F1 community for inspiration and feedback

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/YOUR_USERNAME/f1-news-cli/issues) page
2. Create a new issue with detailed information
3. Tag with appropriate labels (bug, enhancement, question)

### Example Commands for Testing
```bash
# Test basic functionality
f1-news --limit 3

# Test filtering
f1-news --team mclaren --limit 2

# Test practice results
f1-news result --practice 1

# Test multiple sources
f1-news --sources motorsport,autosport --limit 2

# Test help
f1-news --help
f1-news result --help
```

---

**Happy racing! 🏁**

*Stay updated with the latest F1 news and practice session results right from your terminal.*