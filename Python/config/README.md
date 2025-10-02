# Unreal MCP Configuration System

This directory contains configuration files and templates for the Unreal MCP server. The configuration system provides comprehensive control over server behavior, connection settings, logging, security, and tool-specific options.

## Configuration Files

### Main Configuration Files

- **`unreal_mcp.yaml`** - Default configuration file (YAML format)
- **`unreal_mcp.json`** - Default configuration file (JSON format)
- **`development.yaml`** - Development environment template
- **`production.yaml`** - Production environment template

### File Format Support

The configuration system supports multiple file formats:
- **YAML** (.yaml, .yml) - Recommended for human readability
- **JSON** (.json) - Good for programmatic generation
- **TOML** (.toml) - Alternative format support

## Configuration Structure

### Top-Level Configuration

```yaml
version: "0.2.0"                    # Configuration version
environment: "development"           # Environment (development, staging, production)
debug_mode: false                   # Enable debug mode
hot_reload: true                    # Enable configuration hot-reloading
config_watch_interval: 1.0          # Configuration file watch interval in seconds
```

### Connection Settings

```yaml
connection:
  host: "127.0.0.1"                 # Unreal Engine host address
  port: 55557                       # Default UnrealMCP plugin port
  timeout: 5                        # Connection timeout in seconds
  buffer_size: 65536                # Socket buffer size
  auto_reconnect: true              # Enable automatic reconnection
  max_retries: 3                    # Maximum connection retry attempts
  retry_delay: 1.0                  # Delay between retry attempts in seconds
```

### Logging Configuration

```yaml
logging:
  level: "INFO"                     # Default log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  format: "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
  file_enabled: true                # Enable file logging
  file_path: "unreal_mcp.log"       # Log file path
  file_max_size: 10485760           # Maximum log file size in bytes (10MB)
  file_backup_count: 5              # Number of backup log files
  console_enabled: false            # Enable console logging
  console_level: "WARNING"          # Console log level
```

### Project Settings

```yaml
project:
  project_name: ""                  # Unreal project name (auto-detected if empty)
  engine_version: "5.6"             # Unreal Engine version
  project_path: ""                  # Path to .uproject file (auto-detected if empty)
  content_path: "/Game"             # Content browser root path
  plugins_enabled: []               # List of enabled plugins
  plugins_disabled: []              # List of disabled plugins
  build_configuration: "Development" # Build configuration
  target_platform: "Windows"        # Target platform
```

### Security Settings

```yaml
security:
  allowed_hosts:                    # Allowed connection hosts
    - "127.0.0.1"
    - "localhost"
  max_connections: 10               # Maximum concurrent connections
  enable_ssl: false                 # Enable SSL/TLS encryption
  ssl_cert_path: null               # Path to SSL certificate
  ssl_key_path: null                # Path to SSL private key
  api_key_required: false           # Require API key for authentication
  api_key: null                     # API key for authentication
```

### Tool-Specific Configuration

```yaml
tools:
  editor_tools:
    enabled: true
    timeout: 30
    retry_count: 2
    custom_settings: {}

  blueprint_tools:
    enabled: true
    timeout: 60
    retry_count: 2
    custom_settings:
      max_blueprint_size: 1048576
      auto_compile: true

  umg_tools:
    enabled: true
    timeout: 45
    retry_count: 2
    custom_settings:
      default_widget_path: "/Game/UI"
      auto_save: true
```

## Environment Variables

The configuration system supports environment variable overrides for sensitive or environment-specific settings:

| Environment Variable | Configuration Path | Description |
|---------------------|-------------------|-------------|
| `UNREAL_MCP_HOST` | `connection.host` | Unreal Engine host address |
| `UNREAL_MCP_PORT` | `connection.port` | Unreal Engine port |
| `UNREAL_MCP_TIMEOUT` | `connection.timeout` | Connection timeout |
| `UNREAL_MCP_LOG_LEVEL` | `logging.level` | Log level |
| `UNREAL_MCP_LOG_FILE` | `logging.file_path` | Log file path |
| `UNREAL_MCP_PROJECT_PATH` | `project.project_path` | Project path |
| `UNREAL_MCP_ENGINE_VERSION` | `project.engine_version` | Engine version |
| `UNREAL_MCP_DEBUG` | `debug_mode` | Debug mode |
| `UNREAL_MCP_ENVIRONMENT` | `environment` | Environment |

## Configuration Management Tools

The MCP server provides several tools for managing configuration:

### Basic Operations

- **`get_config_info()`** - Get current configuration information
- **`load_config_file(config_file)`** - Load configuration from a file
- **`save_config_file(config_data, config_file)`** - Save configuration to a file
- **`create_default_config(config_file)`** - Create a default configuration file
- **`validate_config(config_file)`** - Validate configuration file
- **`reload_config()`** - Reload configuration from file

### Advanced Operations

- **`get_tool_config(tool_name)`** - Get configuration for a specific tool
- **`update_tool_config(tool_name, tool_config_data)`** - Update configuration for a specific tool
- **`check_config_changes()`** - Check if configuration file has changed since last load
- **`list_config_files(config_dir)`** - List available configuration files

## Usage Examples

### Creating a Default Configuration

```python
# Using MCP tools
result = create_default_config("my_config.yaml")
print(result["config_file"])  # Path to created file
```

### Loading Configuration

```python
# Load from specific file
result = load_config_file("config/production.yaml")

# Auto-detect configuration file
result = load_config_file()
```

### Validating Configuration

```python
# Validate current configuration
result = validate_config()
if result["valid"]:
    print("Configuration is valid")
else:
    print(f"Configuration issues: {result['issues']}")
```

### Updating Tool Configuration

```python
# Update blueprint tools configuration
tool_config = {
    "enabled": True,
    "timeout": 90,
    "retry_count": 3,
    "custom_settings": {
        "auto_compile": False,
        "max_blueprint_size": 2097152
    }
}
result = update_tool_config("blueprint_tools", json.dumps(tool_config))
```

## Environment-Specific Configurations

### Development Environment

The `development.yaml` template is optimized for development:
- Verbose logging (DEBUG level)
- Console logging enabled
- Shorter timeouts for quick feedback
- Auto-compile and auto-save enabled
- Debug mode enabled
- Hot-reload enabled

### Production Environment

The `production.yaml` template is optimized for production:
- Less verbose logging (WARNING level)
- Console logging disabled
- Longer timeouts for stability
- Manual compilation and saves
- SSL/TLS enabled
- API key authentication required
- Hot-reload disabled

## Best Practices

### Configuration Management

1. **Use environment-specific files**: Create separate configuration files for development, staging, and production environments.

2. **Validate configurations**: Always validate configuration files before deployment using the validation tools.

3. **Use environment variables**: For sensitive settings like API keys and passwords, use environment variables instead of hardcoding them.

4. **Version control**: Keep configuration files in version control, but be careful with sensitive information.

5. **Document custom settings**: Document any custom configuration settings and their purposes.

### Security

1. **API Keys**: Use environment variables for API keys and other sensitive information.

2. **SSL/TLS**: Enable SSL/TLS encryption in production environments.

3. **Host Restrictions**: Limit allowed hosts to only necessary addresses.

4. **Connection Limits**: Set appropriate limits on concurrent connections.

### Performance

1. **Logging Levels**: Use appropriate logging levels for each environment (DEBUG for development, WARNING for production).

2. **Buffer Sizes**: Adjust buffer sizes based on expected workload.

3. **Timeouts**: Set appropriate timeouts based on environment and expected response times.

4. **Hot-Reload**: Enable hot-reload in development, disable in production.

## Troubleshooting

### Common Issues

1. **Configuration not found**: The system will use default values if no configuration file is found.

2. **Validation errors**: Use the `validate_config()` tool to identify and fix configuration issues.

3. **Environment variable overrides**: Check that environment variables are set correctly and have valid values.

4. **File format issues**: Ensure configuration files use valid YAML, JSON, or TOML syntax.

### Debugging

1. **Enable debug mode**: Set `debug_mode: true` in configuration for verbose output.

2. **Check logs**: Review log files for configuration loading and validation messages.

3. **Use validation tools**: Use the built-in validation tools to identify issues.

4. **Test configurations**: Test configuration changes in development before applying to production.

## Migration Guide

### From Hardcoded Values

If you're migrating from a system with hardcoded configuration values:

1. Create a configuration file using `create_default_config()`
2. Update the configuration file with your current settings
3. Validate the configuration using `validate_config()`
4. Test the configuration in development
5. Deploy to production

### Between Environments

When moving configurations between environments:

1. Copy the base configuration file
2. Update environment-specific settings
3. Validate the new configuration
4. Test thoroughly before deployment
5. Use environment variables for sensitive differences

## Support

For additional help with the configuration system:

1. Check the tool documentation using the `info()` prompt
2. Use the validation tools to identify issues
3. Review the log files for detailed error messages
4. Consult the configuration examples in this directory
