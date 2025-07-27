import os
import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Handle configuration for F1 News CLI."""
    
    def __init__(self):
        self.config_dir = Path.home() / '.f1-news'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration."""
        default_config = {
            'twitter': {
                'api_key': os.getenv('TWITTER_API_KEY', ''),
                'api_secret': os.getenv('TWITTER_API_SECRET', ''),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN', ''),
                'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET', ''),
                'bearer_token': os.getenv('TWITTER_BEARER_TOKEN', '')
            },
            'reddit': {
                'client_id': os.getenv('REDDIT_CLIENT_ID', ''),
                'client_secret': os.getenv('REDDIT_CLIENT_SECRET', ''),
                'user_agent': 'F1NewsCLI/0.1.0'
            },
            'rss_feeds': [
                'https://www.formula1.com/en/latest/headlines.xml',
                'https://www.autosport.com/rss/feed/f1'
            ],
            'cache_duration': 300,  # 5 minutes
            'default_limit': 10
        }
        
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config(self._config)
    
    @property
    def twitter_config(self) -> Dict[str, str]:
        """Get Twitter configuration."""
        return self._config.get('twitter', {})
    
    @property
    def reddit_config(self) -> Dict[str, str]:
        """Get Reddit configuration."""
        return self._config.get('reddit', {})
    
    @property
    def rss_feeds(self) -> list:
        """Get RSS feed URLs."""
        return self._config.get('rss_feeds', [])