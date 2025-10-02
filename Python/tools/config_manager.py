"""
Configuration Manager for Unreal MCP.

This module provides comprehensive configuration management for the Unreal MCP server.
Supports multiple configuration formats (YAML, JSON, TOML) and provides validation,
environment variable overrides, and configuration merging capabilities.

Features:
- Multiple configuration file formats (YAML, JSON, TOML)
- Environment variable overrides
- Configuration validation with Pydantic models
- Configuration merging and inheritance
- Hot-reloading support
- Configuration templates and defaults
- Project-specific and global configurations
"""

import os
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, validator
from enum import Enum

# Get logger
logger = logging.getLogger("UnrealMCP.Config")

class LogLevel(str, Enum):
    """Supported log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ConfigFormat(str, Enum):
    """Supported configuration file formats."""
    YAML = "yaml"
    JSON = "json"
    TOML = "toml"

class ConnectionConfig(BaseModel):
    """Configuration for Unreal Engine connection."""
    host: str = Field(default="127.0.0.1", description="Unreal Engine host address")
    port: int = Field(default=55557, description="Unreal Engine port")
    timeout: int = Field(default=5, description="Connection timeout in seconds")
    buffer_size: int = Field(default=65536, description="Socket buffer size")
    auto_reconnect: bool = Field(default=True, description="Enable automatic reconnection")
    max_retries: int = Field(default=3, description="Maximum connection retry attempts")
    retry_delay: float = Field(default=1.0, description="Delay between retry attempts in seconds")
    
    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
    
    @validator('timeout')
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError('Timeout must be positive')
        return v

class LoggingConfig(BaseModel):
    """Configuration for logging system."""
    level: LogLevel = Field(default=LogLevel.INFO, description="Default log level")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s", 
                       description="Log message format")
    file_enabled: bool = Field(default=True, description="Enable file logging")
    file_path: str = Field(default="unreal_mcp.log", description="Log file path")
    file_max_size: int = Field(default=10485760, description="Maximum log file size in bytes (10MB)")
    file_backup_count: int = Field(default=5, description="Number of backup log files")
    console_enabled: bool = Field(default=False, description="Enable console logging")
    console_level: LogLevel = Field(default=LogLevel.WARNING, description="Console log level")
    
    @validator('file_max_size')
    def validate_file_size(cls, v):
        if v <= 0:
            raise ValueError('File max size must be positive')
        return v

class ProjectConfig(BaseModel):
    """Configuration for Unreal Engine project."""
    project_name: str = Field(default="", description="Unreal project name")
    engine_version: str = Field(default="5.6", description="Unreal Engine version")
    project_path: str = Field(default="", description="Path to .uproject file")
    content_path: str = Field(default="/Game", description="Content browser root path")
    plugins_enabled: List[str] = Field(default_factory=list, description="List of enabled plugins")
    plugins_disabled: List[str] = Field(default_factory=list, description="List of disabled plugins")
    build_configuration: str = Field(default="Development", description="Build configuration")
    target_platform: str = Field(default="Windows", description="Target platform")

class ToolConfig(BaseModel):
    """Configuration for individual MCP tools."""
    enabled: bool = Field(default=True, description="Whether the tool is enabled")
    timeout: int = Field(default=30, description="Tool execution timeout in seconds")
    retry_count: int = Field(default=2, description="Number of retry attempts")
    custom_settings: Dict[str, Any] = Field(default_factory=dict, description="Tool-specific settings")
    
    @validator('timeout')
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError('Timeout must be positive')
        return v

class SecurityConfig(BaseModel):
    """Configuration for security settings."""
    allowed_hosts: List[str] = Field(default=["127.0.0.1", "localhost"], description="Allowed connection hosts")
    max_connections: int = Field(default=10, description="Maximum concurrent connections")
    enable_ssl: bool = Field(default=False, description="Enable SSL/TLS encryption")
    ssl_cert_path: Optional[str] = Field(default=None, description="Path to SSL certificate")
    ssl_key_path: Optional[str] = Field(default=None, description="Path to SSL private key")
    api_key_required: bool = Field(default=False, description="Require API key for authentication")
    api_key: Optional[str] = Field(default=None, description="API key for authentication")
    
    @validator('max_connections')
    def validate_max_connections(cls, v):
        if v <= 0:
            raise ValueError('Max connections must be positive')
        return v

class UnrealMCPConfig(BaseModel):
    """Main configuration model for Unreal MCP server."""
    version: str = Field(default="0.2.0", description="Configuration version")
    environment: str = Field(default="development", description="Environment (development, staging, production)")
    
    # Sub-configurations
    connection: ConnectionConfig = Field(default_factory=ConnectionConfig, description="Connection settings")
    logging: LoggingConfig = Field(default_factory=LoggingConfig, description="Logging settings")
    project: ProjectConfig = Field(default_factory=ProjectConfig, description="Project settings")
    security: SecurityConfig = Field(default_factory=SecurityConfig, description="Security settings")
    tools: Dict[str, ToolConfig] = Field(default_factory=dict, description="Tool-specific configurations")
    
    # Global settings
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    hot_reload: bool = Field(default=True, description="Enable configuration hot-reloading")
    config_watch_interval: float = Field(default=1.0, description="Configuration file watch interval in seconds")
    
    @validator('environment')
    def validate_environment(cls, v):
        allowed = ['development', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f'Environment must be one of: {allowed}')
        return v

class ConfigManager:
    """
    Configuration manager for Unreal MCP server.
    
    Provides comprehensive configuration management with support for:
    - Multiple file formats (YAML, JSON, TOML)
    - Environment variable overrides
    - Configuration validation
    - Hot-reloading
    - Configuration inheritance
    """
    
    def __init__(self, config_dir: Optional[Union[str, Path]] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_dir: Directory containing configuration files (defaults to ./config)
        """
        self.config_dir = Path(config_dir) if config_dir else Path.cwd() / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        self._config: Optional[UnrealMCPConfig] = None
        self._config_file_path: Optional[Path] = None
        self._last_modified: Optional[float] = None
        
        # Configuration file search order
        self.config_files = [
            "unreal_mcp.yaml",
            "unreal_mcp.yml", 
            "unreal_mcp.json",
            "unreal_mcp.toml",
            "config.yaml",
            "config.yml",
            "config.json",
            "config.toml"
        ]
    
    def find_config_file(self) -> Optional[Path]:
        """
        Find the configuration file to use.
        
        Returns:
            Path to configuration file or None if not found
        """
        # Search in config directory first
        for filename in self.config_files:
            config_path = self.config_dir / filename
            if config_path.exists():
                logger.info(f"Found configuration file: {config_path}")
                return config_path
        
        # Search in current directory
        for filename in self.config_files:
            config_path = Path.cwd() / filename
            if config_path.exists():
                logger.info(f"Found configuration file: {config_path}")
                return config_path
        
        logger.warning("No configuration file found, using defaults")
        return None
    
    def detect_config_format(self, file_path: Path) -> ConfigFormat:
        """
        Detect the format of a configuration file.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Detected configuration format
        """
        suffix = file_path.suffix.lower()
        if suffix in ['.yaml', '.yml']:
            return ConfigFormat.YAML
        elif suffix == '.json':
            return ConfigFormat.JSON
        elif suffix == '.toml':
            return ConfigFormat.TOML
        else:
            raise ValueError(f"Unsupported configuration file format: {suffix}")
    
    def load_config_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Load configuration from a file.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Configuration dictionary
        """
        config_format = self.detect_config_format(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if config_format == ConfigFormat.YAML:
                    return yaml.safe_load(f) or {}
                elif config_format == ConfigFormat.JSON:
                    return json.load(f)
                elif config_format == ConfigFormat.TOML:
                    try:
                        import tomllib
                    except ImportError:
                        try:
                            import tomli as tomllib
                        except ImportError:
                            raise ImportError("TOML support requires tomllib (Python 3.11+) or tomli package")
                    return tomllib.load(f)
        except Exception as e:
            logger.error(f"Error loading configuration file {file_path}: {e}")
            raise
    
    def apply_environment_overrides(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply environment variable overrides to configuration.
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            Configuration dictionary with environment overrides applied
        """
        env_mappings = {
            'UNREAL_MCP_HOST': ('connection.host', str),
            'UNREAL_MCP_PORT': ('connection.port', int),
            'UNREAL_MCP_TIMEOUT': ('connection.timeout', int),
            'UNREAL_MCP_LOG_LEVEL': ('logging.level', str),
            'UNREAL_MCP_LOG_FILE': ('logging.file_path', str),
            'UNREAL_MCP_PROJECT_PATH': ('project.project_path', str),
            'UNREAL_MCP_ENGINE_VERSION': ('project.engine_version', str),
            'UNREAL_MCP_DEBUG': ('debug_mode', lambda x: x.lower() in ['true', '1', 'yes']),
            'UNREAL_MCP_ENVIRONMENT': ('environment', str),
        }
        
        for env_var, (config_path, converter) in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                try:
                    value = converter(env_value)
                    self._set_nested_value(config_dict, config_path, value)
                    logger.debug(f"Applied environment override: {env_var} -> {config_path} = {value}")
                except Exception as e:
                    logger.warning(f"Failed to apply environment override {env_var}: {e}")
        
        return config_dict
    
    def _set_nested_value(self, config_dict: Dict[str, Any], path: str, value: Any) -> None:
        """
        Set a nested value in a configuration dictionary.
        
        Args:
            config_dict: Configuration dictionary
            path: Dot-separated path (e.g., 'connection.host')
            value: Value to set
        """
        keys = path.split('.')
        current = config_dict
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def load_config(self, config_file: Optional[Union[str, Path]] = None) -> UnrealMCPConfig:
        """
        Load configuration from file or use defaults.
        
        Args:
            config_file: Optional path to configuration file
            
        Returns:
            Loaded and validated configuration
        """
        config_dict = {}
        
        # Determine config file to use
        if config_file:
            self._config_file_path = Path(config_file)
            if not self._config_file_path.exists():
                logger.warning(f"Specified config file not found: {config_file}")
                self._config_file_path = None
        else:
            self._config_file_path = self.find_config_file()
        
        # Load configuration from file if found
        if self._config_file_path:
            config_dict = self.load_config_file(self._config_file_path)
            self._last_modified = self._config_file_path.stat().st_mtime
        
        # Apply environment overrides
        config_dict = self.apply_environment_overrides(config_dict)
        
        # Validate and create configuration object
        try:
            self._config = UnrealMCPConfig(**config_dict)
            logger.info("Configuration loaded successfully")
            return self._config
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            logger.info("Using default configuration")
            self._config = UnrealMCPConfig()
            return self._config
    
    def get_config(self) -> UnrealMCPConfig:
        """
        Get the current configuration.
        
        Returns:
            Current configuration object
        """
        if self._config is None:
            return self.load_config()
        return self._config
    
    def reload_config(self) -> UnrealMCPConfig:
        """
        Reload configuration from file.
        
        Returns:
            Reloaded configuration
        """
        logger.info("Reloading configuration")
        return self.load_config(self._config_file_path)
    
    def has_config_changed(self) -> bool:
        """
        Check if the configuration file has changed since last load.
        
        Returns:
            True if configuration has changed
        """
        if not self._config_file_path or not self._config_file_path.exists():
            return False
        
        current_mtime = self._config_file_path.stat().st_mtime
        return current_mtime != self._last_modified
    
    def save_config(self, config: UnrealMCPConfig, file_path: Optional[Union[str, Path]] = None) -> None:
        """
        Save configuration to file.
        
        Args:
            config: Configuration to save
            file_path: Optional path to save to (defaults to current config file)
        """
        if file_path:
            save_path = Path(file_path)
        elif self._config_file_path:
            save_path = self._config_file_path
        else:
            save_path = self.config_dir / "unreal_mcp.yaml"
        
        # Convert to dictionary
        config_dict = config.dict()
        
        # Save based on file extension
        suffix = save_path.suffix.lower()
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                if suffix in ['.yaml', '.yml']:
                    yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
                elif suffix == '.json':
                    json.dump(config_dict, f, indent=2, sort_keys=False)
                elif suffix == '.toml':
                    try:
                        import tomli_w
                    except ImportError:
                        raise ImportError("TOML writing support requires tomli-w package")
                    tomli_w.dump(config_dict, f)
            
            logger.info(f"Configuration saved to: {save_path}")
            self._config_file_path = save_path
            self._last_modified = save_path.stat().st_mtime
            
        except Exception as e:
            logger.error(f"Error saving configuration to {save_path}: {e}")
            raise
    
    def create_default_config(self, file_path: Optional[Union[str, Path]] = None) -> Path:
        """
        Create a default configuration file.
        
        Args:
            file_path: Optional path to create config file (defaults to config/unreal_mcp.yaml)
            
        Returns:
            Path to created configuration file
        """
        if file_path:
            save_path = Path(file_path)
        else:
            save_path = self.config_dir / "unreal_mcp.yaml"
        
        # Create default configuration
        default_config = UnrealMCPConfig()
        
        # Save to file
        self.save_config(default_config, save_path)
        
        logger.info(f"Created default configuration file: {save_path}")
        return save_path
    
    def get_tool_config(self, tool_name: str) -> ToolConfig:
        """
        Get configuration for a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool configuration
        """
        config = self.get_config()
        return config.tools.get(tool_name, ToolConfig())
    
    def update_tool_config(self, tool_name: str, tool_config: ToolConfig) -> None:
        """
        Update configuration for a specific tool.
        
        Args:
            tool_name: Name of the tool
            tool_config: New tool configuration
        """
        config = self.get_config()
        config.tools[tool_name] = tool_config
        self._config = config
    
    def validate_config(self, config: UnrealMCPConfig) -> List[str]:
        """
        Validate configuration and return any issues.
        
        Args:
            config: Configuration to validate
            
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        # Validate connection settings
        if not config.connection.host:
            issues.append("Connection host cannot be empty")
        
        if not (1 <= config.connection.port <= 65535):
            issues.append("Connection port must be between 1 and 65535")
        
        # Validate project settings
        if config.project.project_path and not Path(config.project.project_path).exists():
            issues.append(f"Project path does not exist: {config.project.project_path}")
        
        # Validate security settings
        if config.security.api_key_required and not config.security.api_key:
            issues.append("API key is required when api_key_required is enabled")
        
        # Validate tool configurations
        for tool_name, tool_config in config.tools.items():
            if tool_config.timeout <= 0:
                issues.append(f"Tool '{tool_name}' timeout must be positive")
        
        return issues

# Global configuration manager instance
_config_manager: Optional[ConfigManager] = None

def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def get_config() -> UnrealMCPConfig:
    """Get the current configuration."""
    return get_config_manager().get_config()

def load_config(config_file: Optional[Union[str, Path]] = None) -> UnrealMCPConfig:
    """Load configuration from file."""
    return get_config_manager().load_config(config_file)

def reload_config() -> UnrealMCPConfig:
    """Reload configuration from file."""
    return get_config_manager().reload_config()
