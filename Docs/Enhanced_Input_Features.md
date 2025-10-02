# Enhanced Input Action Support for Unreal MCP

This document provides comprehensive documentation for the enhanced input action system in Unreal MCP, which extends the basic input mapping functionality with advanced features for professional game development.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Input Action Mapping Tools](#input-action-mapping-tools)
- [Input Axis Mapping](#input-axis-mapping)
- [Input Presets and Templates](#input-presets-and-templates)
- [Input Management](#input-management)
- [Enhanced Blueprint Integration](#enhanced-blueprint-integration)
- [Validation and Testing](#validation-and-testing)
- [Import/Export Functionality](#importexport-functionality)
- [Advanced Features](#advanced-features)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)

## Overview

The Enhanced Input Action system provides a comprehensive suite of tools for managing input in Unreal Engine projects through the MCP interface. It extends beyond basic input mapping to include advanced features like multiple key bindings, input presets, validation, and seamless Blueprint integration.

## Features

### Core Features
- **Enhanced Input Action Mapping**: Create input actions with primary and secondary key bindings
- **Input Axis Mapping**: Support for continuous input (movement, camera, etc.)
- **Multiple Key Bindings**: Alternative key bindings for the same action
- **Input Presets**: Pre-configured input setups for common game types
- **Validation System**: Conflict detection and input mapping validation
- **Import/Export**: Save and load input configurations
- **Blueprint Integration**: Enhanced input nodes for Blueprint systems

### Advanced Features
- **Input Contexts**: Context-sensitive input handling
- **Input Triggers**: Custom trigger conditions (Hold, Toggle, DoubleTap, etc.)
- **Category Organization**: Organize input actions by categories
- **Real-time Testing**: Test input actions in real-time
- **Conflict Resolution**: Automatic detection of key binding conflicts

## Input Action Mapping Tools

### `create_enhanced_input_action_mapping`

Creates an enhanced input action mapping with multiple key bindings and metadata.

**Parameters:**
- `action_name` (string): Name of the input action
- `primary_key` (string): Primary key to bind (e.g., "SpaceBar", "LeftMouseButton")
- `secondary_key` (string, optional): Secondary key binding
- `input_type` (string): Type of input mapping ("Action" or "Axis")
- `shift/ctrl/alt/cmd` (boolean): Key modifier flags
- `category` (string): Category for organizing input actions
- `description` (string): Description of the input action

**Example:**
```python
response = send_command("create_enhanced_input_action_mapping", {
    "action_name": "Fire",
    "primary_key": "LeftMouseButton",
    "secondary_key": "RightTrigger",
    "input_type": "Action",
    "category": "Combat",
    "description": "Primary fire action with mouse and controller support"
})
```

### `add_alternative_key_binding`

Adds an alternative key binding to an existing input action.

**Parameters:**
- `action_name` (string): Name of the existing input action
- `alternative_key` (string): Alternative key to bind
- `shift/ctrl/alt/cmd` (boolean): Key modifier flags

**Example:**
```python
response = send_command("add_alternative_key_binding", {
    "action_name": "Fire",
    "alternative_key": "SpaceBar"
})
```

## Input Axis Mapping

### `create_input_axis_mapping`

Creates an input axis mapping for continuous input (movement, camera, etc.).

**Parameters:**
- `axis_name` (string): Name of the input axis
- `positive_key` (string): Key for positive axis value (e.g., "W", "Up Arrow")
- `negative_key` (string, optional): Key for negative axis value (e.g., "S", "Down Arrow")
- `scale` (float): Scale factor for the axis input
- `category` (string): Category for organizing input axes
- `description` (string): Description of the input axis

**Example:**
```python
response = send_command("create_input_axis_mapping", {
    "axis_name": "MoveForward",
    "positive_key": "W",
    "negative_key": "S",
    "scale": 1.0,
    "category": "Movement",
    "description": "Forward/backward movement axis"
})
```

## Input Presets and Templates

### `create_input_preset`

Creates an input preset with common game input mappings.

**Parameters:**
- `preset_name` (string): Name for the input preset
- `preset_type` (string): Type of preset ("FPS", "ThirdPerson", "Platformer", "Racing", "Strategy")
- `custom_mappings` (dict, optional): Custom key mappings to override defaults

**Supported Preset Types:**

#### FPS Preset
- **Actions**: Fire, Aim, Reload, Jump, Crouch
- **Axes**: MoveForward, MoveRight, LookUp, LookRight
- **Keys**: WASD movement, mouse look, space jump, shift crouch

#### Third Person Preset
- **Actions**: Attack, Jump, Dodge, Interact
- **Axes**: MoveForward, MoveRight, LookUp, LookRight
- **Keys**: WASD movement, mouse look, space jump, left shift dodge

#### Platformer Preset
- **Actions**: Jump, Dash, Interact, Pause
- **Axes**: MoveRight
- **Keys**: A/D movement, space jump, left shift dash

### `apply_input_preset`

Applies an existing input preset to the project.

**Parameters:**
- `preset_name` (string): Name of the preset to apply
- `merge_with_existing` (boolean): Whether to merge with existing mappings or replace them

**Example:**
```python
response = send_command("apply_input_preset", {
    "preset_name": "FPS_Controls",
    "merge_with_existing": True
})
```

## Input Management

### `list_input_actions`

Lists all input actions and axes in the project.

**Parameters:**
- `category` (string, optional): Filter by category (empty string for all)
- `include_axes` (boolean): Whether to include axis mappings

**Example:**
```python
response = send_command("list_input_actions", {
    "category": "Combat",
    "include_axes": False
})
```

### `update_input_action_mapping`

Updates an existing input action mapping.

**Parameters:**
- `action_name` (string): Name of the input action to update
- `new_key` (string, optional): New key binding (empty to keep existing)
- `new_shift/ctrl/alt/cmd` (boolean, optional): New modifier settings
- `new_category` (string, optional): New category
- `new_description` (string, optional): New description

### `remove_input_action_mapping`

Removes an input action mapping or specific key binding.

**Parameters:**
- `action_name` (string): Name of the input action
- `key_binding` (string, optional): Specific key binding to remove (empty to remove all bindings)

## Enhanced Blueprint Integration

### `create_enhanced_input_action_blueprint_node`

Creates an enhanced input action node in a Blueprint with advanced features.

**Parameters:**
- `blueprint_name` (string): Name of the target Blueprint
- `action_name` (string): Name of the input action to respond to
- `event_type` (string): Type of input event ("Pressed", "Released", "Hold")
- `node_position` (array, optional): [X, Y] position in the graph
- `auto_connect` (boolean): Whether to automatically connect to BeginPlay if it exists

**Example:**
```python
response = send_command("create_enhanced_input_action_blueprint_node", {
    "blueprint_name": "PlayerCharacter",
    "action_name": "Fire",
    "event_type": "Pressed",
    "node_position": [100, 100],
    "auto_connect": True
})
```

### `create_input_axis_blueprint_node`

Creates an input axis node in a Blueprint for continuous input.

**Parameters:**
- `blueprint_name` (string): Name of the target Blueprint
- `axis_name` (string): Name of the input axis to respond to
- `node_position` (array, optional): [X, Y] position in the graph
- `auto_connect` (boolean): Whether to automatically connect to Tick if it exists

## Validation and Testing

### `validate_input_mappings`

Validates input mappings for conflicts, missing actions, and unused actions.

**Parameters:**
- `check_conflicts` (boolean): Whether to check for key binding conflicts
- `check_missing_actions` (boolean): Whether to check for actions referenced in Blueprints but not mapped
- `check_unused_actions` (boolean): Whether to check for mapped actions not used in Blueprints

**Example:**
```python
response = send_command("validate_input_mappings", {
    "check_conflicts": True,
    "check_missing_actions": True,
    "check_unused_actions": True
})
```

### `test_input_action`

Tests an input action by monitoring its activation in real-time.

**Parameters:**
- `action_name` (string): Name of the input action to test
- `duration` (float): Duration in seconds to monitor the action

## Import/Export Functionality

### `export_input_mappings`

Exports input mappings to a file.

**Parameters:**
- `file_path` (string): Path where to save the exported mappings
- `format` (string): Export format ("json", "csv", "ini")
- `include_axes` (boolean): Whether to include axis mappings
- `include_categories` (boolean): Whether to include category information

### `import_input_mappings`

Imports input mappings from a file.

**Parameters:**
- `file_path` (string): Path to the file containing input mappings
- `merge_with_existing` (boolean): Whether to merge with existing mappings or replace them
- `backup_existing` (boolean): Whether to backup existing mappings before import

## Advanced Features

### `create_input_context`

Creates an input context for context-sensitive input handling.

**Parameters:**
- `context_name` (string): Name of the input context
- `priority` (integer): Priority level (higher numbers take precedence)
- `description` (string): Description of the input context

### `create_input_trigger`

Creates an input trigger with custom conditions.

**Parameters:**
- `trigger_name` (string): Name of the input trigger
- `trigger_type` (string): Type of trigger ("Hold", "Toggle", "DoubleTap", etc.)
- `action_name` (string): Name of the action to trigger
- `parameters` (dict): Additional parameters for the trigger

## Usage Examples

### Setting Up FPS Controls

```python
# Create FPS preset
response = send_command("create_input_preset", {
    "preset_name": "FPS_Controls",
    "preset_type": "FPS"
})

# Add custom mappings
response = send_command("create_enhanced_input_action_mapping", {
    "action_name": "SpecialAbility",
    "primary_key": "Q",
    "category": "Combat",
    "description": "Special ability activation"
})

# Validate the setup
response = send_command("validate_input_mappings", {
    "check_conflicts": True
})
```

### Creating Platformer Controls

```python
# Create platformer preset
response = send_command("create_input_preset", {
    "preset_name": "Platformer_Controls",
    "preset_type": "Platformer"
})

# Add movement axis
response = send_command("create_input_axis_mapping", {
    "axis_name": "MoveRight",
    "positive_key": "D",
    "negative_key": "A",
    "scale": 1.0,
    "category": "Movement"
})

# Add dash action
response = send_command("create_enhanced_input_action_mapping", {
    "action_name": "Dash",
    "primary_key": "LeftShift",
    "category": "Movement",
    "description": "Quick dash movement"
})
```

### Blueprint Integration

```python
# Create a character blueprint
response = send_command("create_blueprint", {
    "name": "PlayerCharacter",
    "parent_class": "Character"
})

# Add input action nodes
response = send_command("create_enhanced_input_action_blueprint_node", {
    "blueprint_name": "PlayerCharacter",
    "action_name": "Jump",
    "event_type": "Pressed",
    "auto_connect": True
})

response = send_command("create_input_axis_blueprint_node", {
    "blueprint_name": "PlayerCharacter",
    "axis_name": "MoveForward",
    "auto_connect": True
})
```

## Best Practices

### Input Action Naming
- Use clear, descriptive names: "Fire", "Jump", "Reload"
- Use consistent naming conventions across your project
- Group related actions with categories

### Key Binding Design
- Provide multiple key bindings for important actions
- Consider accessibility with alternative input methods
- Use intuitive key combinations (Shift + R for reload, etc.)

### Organization
- Use categories to group related input actions
- Document complex input mappings with descriptions
- Regularly validate input mappings to avoid conflicts

### Testing
- Test input actions in real-time during development
- Validate input mappings before shipping
- Export input configurations for team collaboration

### Performance
- Avoid creating unnecessary duplicate mappings
- Use appropriate input types (Action vs Axis)
- Consider input context switching for complex games

## Troubleshooting

### Common Issues

**Key Binding Conflicts**
- Use the validation system to detect conflicts
- Provide alternative key bindings for conflicted actions
- Consider input context switching

**Missing Input Actions**
- Check Blueprint references against input mappings
- Use the validation system to find missing actions
- Ensure input actions are created before Blueprint integration

**Export/Import Issues**
- Verify file paths and permissions
- Check file format compatibility
- Use backup functionality when importing

### Getting Help

For additional support with the Enhanced Input Action system:
1. Check the validation system for configuration issues
2. Use the test suite to verify functionality
3. Review the example scripts for implementation patterns
4. Consult the Unreal Engine documentation for advanced input features

## Conclusion

The Enhanced Input Action system provides a comprehensive solution for managing input in Unreal Engine projects. With features ranging from basic input mapping to advanced validation and Blueprint integration, it supports the full spectrum of game development needs while maintaining ease of use and professional quality.

By following the best practices and utilizing the full feature set, developers can create robust, accessible, and maintainable input systems for their games.
