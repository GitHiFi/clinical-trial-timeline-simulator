import yaml
from typing import Dict, Any, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConfigError(Exception):
    """Custom exception for configuration issues."""
    pass

class AppConfig:
    """Singleton-like class for loading and accessing configuration."""
    _instance: Dict[str, Any] = None

    @classmethod
    def load(cls, config_path: str = 'config.yaml') -> Dict[str, Any]:
        if cls._instance is None:
            try:
                with open(config_path, 'r') as f:
                    cls._instance = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
            except FileNotFoundError:
                raise ConfigError(f"Config file not found: {config_path}")
            except yaml.YAMLError as e:
                raise ConfigError(f"Invalid YAML in config: {e}")
        return cls._instance

    @classmethod
    def get_delays(cls) -> Dict[str, Dict[str, float]]:
        return cls.load()['delays']

    @classmethod
    def get_gcp(cls) -> Dict[str, Any]:
        return cls.load()['gcp']

    @classmethod
    def get_visualization(cls) -> Dict[str, Any]:
        return cls.load()['visualization']

    @classmethod
    def get_flask(cls) -> Dict[str, bool]:
        return cls.load()['flask']