# 🏎️ F1 News CLI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![F1](https://img.shields.io/badge/Formula%201-🏁-red.svg)](https://www.formula1.com/)

A powerful command-line tool to fetch the latest Formula 1 news, race results, and insights directly in your terminal.

## ✨ Features

- **📰 Live F1 News**: Fetch real-time F1 news from official RSS feeds
- **🏁 Race Results**: Get the latest race, qualifying, and sprint session results
- **🎨 Rich Terminal Output**: Beautiful, colorful terminal displays
- **📊 Multiple Formats**: Output in terminal, JSON, or Markdown formats
- **🔍 Smart Filtering**: Filter news by teams, drivers, or custom keywords
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

# Fetch latest F1 news
f1-news fetch

# Get latest race results
f1-news result

# Filter news (coming soon)
f1-news filter --team ferrari
```

## 📖 User Guide

### 1. Fetching F1 News

The `fetch` command retrieves the latest F1 news from official sources:

```bash
# Basic usage - get 10 latest news items
f1-news fetch

# Limit the number of articles
f1-news fetch --limit 5

# Change output format
f1-news fetch --format json
f1-news fetch --format markdown
f1-news fetch --format terminal  # default
```

#### Example Output:
```
                                    F1 News                                    
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Title                      ┃ Keywords                    ┃ Time             ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Verstappen dominates in... │ verstappen, red bull, f1    │ 2025-07-26 18:31 │
│ Hamilton's strategy call   │ hamilton, ferrari, strategy │ 2025-07-26 17:28 │
│ McLaren's double podium    │ mclaren, norris, piastri    │ 2025-07-26 16:53 │
└────────────────────────────┴─────────────────────────────┴──────────────────┘
```

### 2. Getting Race Results

The `result` command fetches the most recent session results:

```bash
# Get latest race/qualifying/sprint results
f1-news result
```

#### Example Output:
```
[RACE] United Kingdom Grand Prix
Location: Silverstone
Date: July 06, 2025

                                 Race Results                                  
┏━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┳━━━┓
┃ Pos┃ Driver          ┃ Team                  ┃ Time         ┃ Points ┃FL ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━╇━━━┩
│ 1  │ Lando NORRIS    │ McLaren               │ WINNER       │ 25     │   │
│ 2  │ Oscar PIASTRI   │ McLaren               │ +6.812       │ 18     │   │
│ 3  │ Max VERSTAPPEN  │ Red Bull Racing       │ +15.924      │ 15     │ * │
└────┴─────────────────┴───────────────────────┴──────────────┴────────┴───┘

Podium Finishers
1st: Lando NORRIS (McLaren)
2nd: Oscar PIASTRI (McLaren)  
3rd: Max VERSTAPPEN (Red Bull Racing)
```

### 3. Filtering News (Coming Soon)

```bash
# Filter by F1 team
f1-news filter --team ferrari
f1-news filter --team "red bull"

# Filter by driver
f1-news filter --driver verstappen
f1-news filter --driver hamilton

# Filter by custom keyword
f1-news filter --keyword "championship"
f1-news filter --keyword "safety car"
```

### 4. Output Formats

#### Terminal Format (Default)
Rich, colorful output with tables and panels - perfect for interactive use.

#### JSON Format
```bash
f1-news fetch --format json
```
```json
[
  {
    "title": "Verstappen wins Belgian GP",
    "content": "Max Verstappen secured victory...",
    "url": "https://formula1.com/...",
    "source": "rss_Formula1.com",
    "timestamp": "2025-07-26T18:31:44",
    "keywords": ["verstappen", "belgian", "gp", "victory"]
  }
]
```

#### Markdown Format
```bash
f1-news fetch --format markdown
```
Perfect for documentation or saving to files.

## 🔧 Configuration

### News Sources
The CLI fetches news from these RSS feeds:
- Formula1.com Official News
- Autosport.com F1 Section

### Race Data
Live race results are fetched from the [OpenF1 API](https://openf1.org/) - a free, real-time F1 data service.

## 🚀 Advanced Usage

### Combining Commands
```bash
# Get news and save to file
f1-news fetch --format markdown > f1_news.md

# Get race results as JSON for processing
f1-news result --format json | jq '.results[0:3]'

# Chain multiple commands
f1-news fetch --limit 3 && f1-news result
```

### Integration Examples

#### Use in Scripts
```bash
#!/bin/bash
echo "=== Daily F1 Update ==="
f1-news fetch --limit 5
echo ""
f1-news result
```

#### Cron Job for Daily Updates
```bash
# Add to crontab for daily F1 updates
0 9 * * * /usr/local/bin/f1-news fetch --limit 10 > ~/f1_daily.txt
```

## 🛠️ Development

### Project Structure
```
f1-news-cli/
├── f1_news/
│   ├── __init__.py
│   ├── cli.py          # Main CLI interface
│   ├── models.py       # Data models
│   ├── sources.py      # News and race data sources
│   ├── formatters.py   # Output formatting
│   ├── filters.py      # News filtering logic
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

# Run directly
python -m f1_news.cli fetch
python -m f1_news.cli result
```

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📊 Dependencies

- **click** - Command-line interface framework
- **rich** - Rich terminal formatting
- **feedparser** - RSS feed parsing
- **requests** - HTTP requests for APIs
- **python-dateutil** - Date/time parsing

## 🐛 Troubleshooting

### Common Issues

**Command not found after installation:**
```bash
# Make sure pip install location is in PATH
pip show f1-news-cli
# Or run directly
python -m f1_news.cli
```

**No race results showing:**
- The CLI shows the most recent completed session
- If no recent sessions, it falls back to mock data
- Check your internet connection for API access

**RSS feeds not loading:**
- Feeds occasionally have temporary outages
- The CLI will show available data from working feeds
- Check your internet connection

### Debug Mode
```bash
# Run with Python for detailed error messages
python -m f1_news.cli fetch --limit 5
```

## 🗺️ Roadmap

- [ ] **Social Media Integration**: Twitter and Reddit news sources
- [ ] **Advanced Filtering**: Real-time filtering implementation
- [ ] **Configuration File**: Customize news sources and preferences
- [ ] **Caching**: Offline support and faster repeated queries
- [ ] **Live Timing**: Real-time race updates during sessions
- [ ] **Driver Standings**: Championship points and standings
- [ ] **Historical Data**: Access past seasons and results

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenF1 API](https://openf1.org/) - Free, real-time F1 data
- [Formula1.com](https://formula1.com/) - Official F1 news RSS feeds
- [Autosport.com](https://autosport.com/) - F1 journalism and analysis
- The amazing F1 community for inspiration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/YOUR_USERNAME/f1-news-cli/issues) page
2. Create a new issue with detailed information
3. Tag with appropriate labels (bug, enhancement, question)

---

**Happy racing! 🏁**

*Stay updated with the latest F1 news and results right from your terminal.*