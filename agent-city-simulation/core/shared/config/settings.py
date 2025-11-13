"""
Central configuration management using Pydantic Settings.

Loads configuration from:
1. Environment variables
2. .env.local file (local development)
3. .env.gcp file (GCP production)
4. YAML configuration files
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main application settings."""

    # =============================================================================
    # ENVIRONMENT
    # =============================================================================
    environment: str = Field(default="local", description="Deployment environment")
    debug: bool = Field(default=True, description="Debug mode")

    # =============================================================================
    # DATABASE CONFIGURATION
    # =============================================================================
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="agent_city")
    postgres_user: str = Field(default="agent_user")
    postgres_password: str = Field(default="")

    # Redis
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_password: str = Field(default="")
    redis_db: int = Field(default=0)

    # =============================================================================
    # MESSAGE QUEUE
    # =============================================================================
    kafka_bootstrap_servers: str = Field(default="localhost:9092")
    kafka_consumer_group: str = Field(default="agent-city")

    # GCP Pub/Sub (optional)
    gcp_project_id: Optional[str] = Field(default=None)
    pubsub_emulator_host: Optional[str] = Field(default=None)

    # =============================================================================
    # AI/ML API KEYS
    # =============================================================================
    anthropic_api_key: Optional[str] = Field(default=None)
    openai_api_key: Optional[str] = Field(default=None)

    # =============================================================================
    # FINANCIAL TRADING APIs
    # =============================================================================
    alpaca_api_key: Optional[str] = Field(default=None)
    alpaca_secret_key: Optional[str] = Field(default=None)
    alpaca_base_url: str = Field(default="https://paper-api.alpaca.markets")

    polygon_api_key: Optional[str] = Field(default=None)
    alpha_vantage_api_key: Optional[str] = Field(default=None)
    yahoo_finance_enabled: bool = Field(default=True)

    # =============================================================================
    # NEWS AND SENTIMENT APIs
    # =============================================================================
    news_api_key: Optional[str] = Field(default=None)
    twitter_api_key: Optional[str] = Field(default=None)
    twitter_api_secret: Optional[str] = Field(default=None)
    twitter_bearer_token: Optional[str] = Field(default=None)
    reddit_client_id: Optional[str] = Field(default=None)
    reddit_client_secret: Optional[str] = Field(default=None)
    reddit_user_agent: str = Field(default="AgentCityBot/1.0")

    # =============================================================================
    # GEOGRAPHIC DATA
    # =============================================================================
    mapbox_api_key: Optional[str] = Field(default=None)
    osm_enabled: bool = Field(default=True)

    # =============================================================================
    # MONITORING AND LOGGING
    # =============================================================================
    sentry_dsn: Optional[str] = Field(default=None)
    log_level: str = Field(default="INFO")
    prometheus_enabled: bool = Field(default=True)
    prometheus_port: int = Field(default=9090)

    # =============================================================================
    # APPLICATION CONFIGURATION
    # =============================================================================
    api_gateway_host: str = Field(default="0.0.0.0")
    api_gateway_port: int = Field(default=8000)
    dashboard_host: str = Field(default="0.0.0.0")
    dashboard_port: int = Field(default=3000)

    # =============================================================================
    # SECURITY
    # =============================================================================
    jwt_secret: str = Field(default="change-me-in-production")
    dashboard_api_key: str = Field(default="change-me")
    require_auth: bool = Field(default=False)

    # =============================================================================
    # PERFORMANCE
    # =============================================================================
    worker_threads: int = Field(default=4)
    db_pool_size: int = Field(default=20)
    db_max_overflow: int = Field(default=10)
    cache_ttl: int = Field(default=300)

    # =============================================================================
    # FEATURE FLAGS
    # =============================================================================
    enable_experimental_features: bool = Field(default=False)
    enable_detailed_metrics: bool = Field(default=True)
    enable_agent_memory: bool = Field(default=True)

    # Model configuration
    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_url_sync(self) -> str:
        """Construct synchronous PostgreSQL database URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def kafka_servers(self) -> List[str]:
        """Get Kafka servers as a list."""
        return [s.strip() for s in self.kafka_bootstrap_servers.split(",")]

    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment in ["local", "development"]


class ConfigManager:
    """Manages YAML configuration files."""

    def __init__(self, config_dir: str = "config"):
        """Initialize configuration manager.

        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self._cache: Dict[str, Any] = {}

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file.

        Args:
            filename: Name of the YAML file (without path)

        Returns:
            Parsed YAML content as dictionary
        """
        if filename in self._cache:
            return self._cache[filename]

        file_path = self.config_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self._cache[filename] = config
        return config

    def get_core_config(self) -> Dict[str, Any]:
        """Load core foundation configuration."""
        return self.load_yaml("core.yaml")

    def get_modules_config(self) -> Dict[str, Any]:
        """Load modules configuration."""
        return self.load_yaml("modules.yaml")

    def get_departments_config(self) -> Dict[str, Any]:
        """Load departments configuration."""
        return self.load_yaml("departments.yaml")

    def is_module_enabled(self, module_name: str) -> bool:
        """Check if a module is enabled.

        Args:
            module_name: Name of the module to check

        Returns:
            True if module is enabled, False otherwise
        """
        modules_config = self.get_modules_config()
        module_config = modules_config.get("modules", {}).get(module_name, {})
        return module_config.get("enabled", False)

    def is_department_enabled(self, department_name: str) -> bool:
        """Check if a department is enabled.

        Args:
            department_name: Name of the department to check

        Returns:
            True if department is enabled, False otherwise
        """
        departments_config = self.get_departments_config()
        dept_config = departments_config.get("departments", {}).get(department_name, {})
        return dept_config.get("enabled", False)

    def get_module_config(self, module_name: str) -> Dict[str, Any]:
        """Get configuration for a specific module.

        Args:
            module_name: Name of the module

        Returns:
            Module configuration dictionary
        """
        modules_config = self.get_modules_config()
        return modules_config.get("modules", {}).get(module_name, {})

    def get_department_config(self, department_name: str) -> Dict[str, Any]:
        """Get configuration for a specific department.

        Args:
            department_name: Name of the department

        Returns:
            Department configuration dictionary
        """
        departments_config = self.get_departments_config()
        return departments_config.get("departments", {}).get(department_name, {})


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance (cached)
    """
    return Settings()


@lru_cache()
def get_config_manager() -> ConfigManager:
    """Get cached configuration manager instance.

    Returns:
        ConfigManager instance (cached)
    """
    return ConfigManager()
