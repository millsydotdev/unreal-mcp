# Project Tools

This document describes the comprehensive project management tools available in the Unreal MCP system.

## Overview

The Project Tools module provides comprehensive tools for managing project-wide settings, configuration, plugins, build targets, and project validation. These tools enable AI assistants to manage Unreal Engine projects at a high level.

## Available Tools

### Input Management

#### `create_input_mapping`
Create an input mapping for the project with support for key modifiers.

**Parameters:**
- `action_name` (str): Name of the input action
- `key` (str): Key to bind (e.g., "SpaceBar", "LeftMouseButton", "W")
- `input_type` (str, optional): Type of input mapping ("Action" or "Axis"), defaults to "Action"
- `shift` (bool, optional): Whether Shift key modifier is required, defaults to False
- `ctrl` (bool, optional): Whether Ctrl key modifier is required, defaults to False
- `alt` (bool, optional): Whether Alt key modifier is required, defaults to False
- `cmd` (bool, optional): Whether Cmd key modifier is required (Mac only), defaults to False

**Returns:**
- Dict containing success status and response message

**Example:**
```python
create_input_mapping(
    action_name="Jump",
    key="SpaceBar",
    input_type="Action"
)

create_input_mapping(
    action_name="Sprint",
    key="LeftShift",
    input_type="Action",
    shift=True
)
```

### Project Information

#### `get_project_info`
Get comprehensive project information including name, engine version, modules, and plugins.

**Parameters:**
- None

**Returns:**
- Dict containing project details

**Example:**
```python
project_info = get_project_info()
# Returns information about project name, engine version, modules, etc.
```

### Engine Settings Management

#### `get_engine_settings`
Get current engine settings and configuration.

**Parameters:**
- None

**Returns:**
- Dict containing engine settings information

#### `set_engine_setting`
Set an engine setting value.

**Parameters:**
- `setting_name` (str): Name of the setting to modify
- `setting_value` (str): New value for the setting
- `section` (str, optional): Configuration section, defaults to "SystemSettings"

**Returns:**
- Dict containing success status and response message

**Example:**
```python
set_engine_setting(
    setting_name="MaxFPS",
    setting_value="60",
    section="SystemSettings"
)
```

### Plugin Management

#### `get_plugin_info`
Get information about plugins in the project.

**Parameters:**
- `plugin_name` (str, optional): Specific plugin name to query (returns all if None)

**Returns:**
- Dict containing plugin information

**Example:**
```python
# Get info for all plugins
all_plugins = get_plugin_info()

# Get info for specific plugin
umg_plugin = get_plugin_info(plugin_name="UMG")
```

#### `enable_plugin`
Enable a plugin in the project.

**Parameters:**
- `plugin_name` (str): Name of the plugin to enable

**Returns:**
- Dict containing success status and response message

#### `disable_plugin`
Disable a plugin in the project.

**Parameters:**
- `plugin_name` (str): Name of the plugin to disable

**Returns:**
- Dict containing success status and response message

**Example:**
```python
# Enable UMG plugin
enable_plugin("UMG")

# Disable experimental plugin
disable_plugin("ExperimentalPlugin")
```

### Build Configuration

#### `get_build_targets`
Get information about build targets in the project.

**Parameters:**
- None

**Returns:**
- Dict containing build targets information

**Example:**
```python
build_targets = get_build_targets()
# Returns information about available build targets (Game, Editor, etc.)
```

### Project Structure Management

#### `create_content_folder`
Create a new folder in the content browser.

**Parameters:**
- `folder_path` (str): Path where to create the folder (e.g., "/Game/UI")
- `folder_name` (str): Name of the folder to create

**Returns:**
- Dict containing success status and response message

**Example:**
```python
create_content_folder(
    folder_path="/Game",
    folder_name="Weapons"
)

create_content_folder(
    folder_path="/Game/UI",
    folder_name="HUD"
)
```

### Project Validation and Diagnostics

#### `get_project_diagnostics`
Get project diagnostics and validation information.

**Parameters:**
- None

**Returns:**
- Dict containing project diagnostics including warnings, errors, and recommendations

#### `validate_project`
Validate project integrity and configuration.

**Parameters:**
- `check_plugins` (bool, optional): Whether to validate plugin configurations, defaults to True
- `check_blueprints` (bool, optional): Whether to validate Blueprint assets, defaults to True
- `check_assets` (bool, optional): Whether to validate all asset references, defaults to False

**Returns:**
- Dict containing validation results and any issues found

**Example:**
```python
# Quick validation
validation_result = validate_project()

# Comprehensive validation
full_validation = validate_project(
    check_plugins=True,
    check_blueprints=True,
    check_assets=True
)
```

## Best Practices

### Input Mapping
- Use descriptive action names that clearly indicate the action's purpose
- Group related actions with consistent naming conventions (e.g., "MoveForward", "MoveBackward")
- Consider using modifier keys for secondary actions (e.g., "Sprint" with Shift modifier)
- Test input mappings in the game to ensure they work as expected

### Plugin Management
- Always check plugin dependencies before enabling/disabling plugins
- Use `get_plugin_info` to verify plugin status before making changes
- Be cautious when disabling core plugins as this may break project functionality
- Document any custom plugins used in your project

### Project Structure
- Organize content into logical folder hierarchies
- Use consistent naming conventions for folders and assets
- Create folders before adding assets to maintain organization
- Consider using the validation tools to check for orphaned or missing assets

### Engine Settings
- Be careful when modifying engine settings as they can affect project performance
- Test changes in a development environment before applying to production
- Document any custom engine settings for team reference
- Use the diagnostics tools to identify potential configuration issues

### Validation and Diagnostics
- Run project validation regularly during development
- Address warnings and errors promptly to maintain project health
- Use diagnostics information to optimize project performance
- Keep validation reports for reference and debugging

## Error Handling

All project tools include comprehensive error handling:

- **Connection Errors**: Tools will return appropriate error messages if unable to connect to Unreal Engine
- **Parameter Validation**: Tools validate required parameters and provide clear error messages
- **Unreal Engine Errors**: Tools capture and report errors from the Unreal Engine side
- **Logging**: All operations are logged for debugging and monitoring purposes

## Integration with Other Tools

Project tools work seamlessly with other MCP tool categories:

- **Blueprint Tools**: Use project tools to manage Blueprint-related plugins and settings
- **UMG Tools**: Use project tools to enable UMG plugin and manage UI-related settings
- **Editor Tools**: Use project tools to configure editor-specific settings and behaviors
- **Actor Tools**: Use project tools to manage actor-related engine settings

## Examples

### Setting up a new project
```python
# Get project information
project_info = get_project_info()

# Enable required plugins
enable_plugin("UMG")
enable_plugin("EnhancedInput")

# Set up input mappings
create_input_mapping("MoveForward", "W")
create_input_mapping("MoveBackward", "S")
create_input_mapping("Jump", "SpaceBar")
create_input_mapping("Sprint", "LeftShift", shift=True)

# Create content organization
create_content_folder("/Game", "Characters")
create_content_folder("/Game", "UI")
create_content_folder("/Game/UI", "HUD")
create_content_folder("/Game/UI", "Menus")

# Validate project setup
validation_result = validate_project()
```

### Managing plugin configurations
```python
# Check current plugin status
plugins = get_plugin_info()

# Enable specific plugins
enable_plugin("ModelingToolsEditorMode")
enable_plugin("GeometryCollection")

# Disable unused plugins
disable_plugin("ExperimentalPlugin")

# Validate plugin configuration
plugin_validation = validate_project(check_plugins=True)
```

### Project maintenance
```python
# Get comprehensive diagnostics
diagnostics = get_project_diagnostics()

# Run full project validation
validation = validate_project(
    check_plugins=True,
    check_blueprints=True,
    check_assets=True
)

# Check build targets
build_targets = get_build_targets()

# Review engine settings
engine_settings = get_engine_settings()
```
