import json
import time
from pathlib import Path
from typing import Any, Optional


class Cache:
    """Simple file-based cache for API responses."""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path.home() / '.f1-news' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for a key."""
        return self.cache_dir / f"{key}.json"
    
    def get(self, key: str, max_age: int = 300) -> Optional[Any]:
        """Get value from cache if not expired."""
        cache_file = self._get_cache_file(key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is expired
            if time.time() - cache_data['timestamp'] > max_age:
                cache_file.unlink()  # Delete expired cache
                return None
            
            return cache_data['data']
            
        except (json.JSONDecodeError, KeyError, OSError):
            # Invalid cache file, remove it
            if cache_file.exists():
                cache_file.unlink()
            return None
    
    def set(self, key: str, value: Any):
        """Set value in cache."""
        cache_file = self._get_cache_file(key)
        
        cache_data = {
            'timestamp': time.time(),
            'data': value
        }
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, default=str)  # default=str for datetime serialization
        except OSError:
            pass  # Silently fail if can't write cache
    
    def clear(self):
        """Clear all cache files."""
        for cache_file in self.cache_dir.glob('*.json'):
            try:
                cache_file.unlink()
            except OSError:
                pass