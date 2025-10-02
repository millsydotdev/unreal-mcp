"""
Project Tools for Unreal MCP.

This module provides comprehensive tools for managing project-wide settings and configuration.
Includes project settings, plugin management, build configuration, project information tools,
and configuration management capabilities.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_project_tools(mcp: FastMCP):
    """Register project tools with the MCP server."""
    
    @mcp.tool()
    def create_input_mapping(
        ctx: Context,
        action_name: str,
        key: str,
        input_type: str = "Action",
        shift: bool = False,
        ctrl: bool = False,
        alt: bool = False,
        cmd: bool = False
    ) -> Dict[str, Any]:
        """
        Create an input mapping for the project.
        
        Args:
            action_name: Name of the input action
            key: Key to bind (SpaceBar, LeftMouseButton, etc.)
            input_type: Type of input mapping (Action or Axis)
            shift: Whether Shift key modifier is required
            ctrl: Whether Ctrl key modifier is required
            alt: Whether Alt key modifier is required
            cmd: Whether Cmd key modifier is required (Mac only)
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "action_name": action_name,
                "key": key,
                "input_type": input_type,
                "shift": shift,
                "ctrl": ctrl,
                "alt": alt,
                "cmd": cmd
            }
            
            logger.info(f"Creating input mapping '{action_name}' with key '{key}' and modifiers: shift={shift}, ctrl={ctrl}, alt={alt}, cmd={cmd}")
            response = unreal.send_command("create_input_mapping", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input mapping creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_project_info(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Get comprehensive project information.
        
        Returns:
            Dict containing project details including name, engine version, modules, plugins
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Retrieving project information")
            response = unreal.send_command("get_project_info", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Project info response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting project info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_engine_settings(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Get current engine settings and configuration.
        
        Returns:
            Dict containing engine settings information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Retrieving engine settings")
            response = unreal.send_command("get_engine_settings", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Engine settings response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting engine settings: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def set_engine_setting(
        ctx: Context,
        setting_name: str,
        setting_value: str,
        section: str = "SystemSettings"
    ) -> Dict[str, Any]:
        """
        Set an engine setting value.
        
        Args:
            setting_name: Name of the setting to modify
            setting_value: New value for the setting
            section: Configuration section (default: SystemSettings)
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "setting_name": setting_name,
                "setting_value": setting_value,
                "section": section
            }
            
            logger.info(f"Setting engine setting '{setting_name}' to '{setting_value}' in section '{section}'")
            response = unreal.send_command("set_engine_setting", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Engine setting update response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting engine setting: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_plugin_info(
        ctx: Context,
        plugin_name: str = None
    ) -> Dict[str, Any]:
        """
        Get information about plugins in the project.
        
        Args:
            plugin_name: Specific plugin name to query (optional, returns all if None)
            
        Returns:
            Dict containing plugin information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {}
            if plugin_name:
                params["plugin_name"] = plugin_name
                logger.info(f"Retrieving plugin info for '{plugin_name}'")
            else:
                logger.info("Retrieving all plugin information")
            
            response = unreal.send_command("get_plugin_info", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Plugin info response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting plugin info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def enable_plugin(
        ctx: Context,
        plugin_name: str
    ) -> Dict[str, Any]:
        """
        Enable a plugin in the project.
        
        Args:
            plugin_name: Name of the plugin to enable
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"plugin_name": plugin_name}
            
            logger.info(f"Enabling plugin '{plugin_name}'")
            response = unreal.send_command("enable_plugin", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Plugin enable response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error enabling plugin: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def disable_plugin(
        ctx: Context,
        plugin_name: str
    ) -> Dict[str, Any]:
        """
        Disable a plugin in the project.
        
        Args:
            plugin_name: Name of the plugin to disable
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"plugin_name": plugin_name}
            
            logger.info(f"Disabling plugin '{plugin_name}'")
            response = unreal.send_command("disable_plugin", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Plugin disable response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error disabling plugin: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_build_targets(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Get information about build targets in the project.
        
        Returns:
            Dict containing build targets information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Retrieving build targets information")
            response = unreal.send_command("get_build_targets", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Build targets response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting build targets: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_content_folder(
        ctx: Context,
        folder_path: str,
        folder_name: str
    ) -> Dict[str, Any]:
        """
        Create a new folder in the content browser.
        
        Args:
            folder_path: Path where to create the folder (e.g., "/Game/UI")
            folder_name: Name of the folder to create
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "folder_path": folder_path,
                "folder_name": folder_name
            }
            
            logger.info(f"Creating content folder '{folder_name}' at path '{folder_path}'")
            response = unreal.send_command("create_content_folder", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Content folder creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating content folder: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_project_diagnostics(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Get project diagnostics and validation information.
        
        Returns:
            Dict containing project diagnostics including warnings, errors, and recommendations
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Retrieving project diagnostics")
            response = unreal.send_command("get_project_diagnostics", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Project diagnostics response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting project diagnostics: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def validate_project(
        ctx: Context,
        check_plugins: bool = True,
        check_blueprints: bool = True,
        check_assets: bool = False
    ) -> Dict[str, Any]:
        """
        Validate project integrity and configuration.
        
        Args:
            check_plugins: Whether to validate plugin configurations
            check_blueprints: Whether to validate Blueprint assets
            check_assets: Whether to validate all asset references
            
        Returns:
            Dict containing validation results and any issues found
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "check_plugins": check_plugins,
                "check_blueprints": check_blueprints,
                "check_assets": check_assets
            }
            
            logger.info(f"Validating project with options: plugins={check_plugins}, blueprints={check_blueprints}, assets={check_assets}")
            response = unreal.send_command("validate_project", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Project validation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error validating project: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_config_info(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Get current configuration information.
        
        Returns:
            Dict containing current configuration details
        """
        try:
            from tools.config_manager import get_config_manager
            
            config_manager = get_config_manager()
            config = config_manager.get_config()
            
            # Convert config to dict for JSON serialization
            config_dict = config.dict()
            
            # Add metadata
            result = {
                "success": True,
                "config_file": str(config_manager._config_file_path) if config_manager._config_file_path else None,
                "config_dir": str(config_manager.config_dir),
                "last_modified": config_manager._last_modified,
                "configuration": config_dict
            }
            
            logger.info("Configuration information retrieved successfully")
            return result
            
        except Exception as e:
            error_msg = f"Error getting configuration info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def load_config_file(
        ctx: Context,
        config_file: str = None
    ) -> Dict[str, Any]:
        """
        Load configuration from a file.
        
        Args:
            config_file: Path to configuration file (optional, will auto-detect if not provided)
            
        Returns:
            Response indicating success or failure with loaded configuration
        """
        try:
            from tools.config_manager import get_config_manager
            
            config_manager = get_config_manager()
            
            if config_file:
                config_path = Path(config_file)
                if not config_path.exists():
                    return {"success": False, "message": f"Configuration file not found: {config_file}"}
            else:
                config_path = None
            
            config = config_manager.load_config(config_path)
            
            result = {
                "success": True,
                "message": "Configuration loaded successfully",
                "config_file": str(config_manager._config_file_path) if config_manager._config_file_path else None,
                "configuration": config.dict()
            }
            
            logger.info(f"Configuration loaded from: {config_manager._config_file_path}")
            return result
            
        except Exception as e:
            error_msg = f"Error loading configuration: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def save_config_file(
        ctx: Context,
        config_data: str,
        config_file: str = None
    ) -> Dict[str, Any]:
        """
        Save configuration to a file.
        
        Args:
            config_data: JSON string containing configuration data
            config_file: Path to save configuration file (optional)
            
        Returns:
            Response indicating success or failure
        """
        try:
            from tools.config_manager import get_config_manager, UnrealMCPConfig
            
            # Parse configuration data
            config_dict = json.loads(config_data)
            
            # Validate configuration
            config = UnrealMCPConfig(**config_dict)
            
            config_manager = get_config_manager()
            save_path = Path(config_file) if config_file else None
            
            config_manager.save_config(config, save_path)
            
            result = {
                "success": True,
                "message": "Configuration saved successfully",
                "config_file": str(config_manager._config_file_path)
            }
            
            logger.info(f"Configuration saved to: {config_manager._config_file_path}")
            return result
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in configuration data: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Error saving configuration: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_default_config(
        ctx: Context,
        config_file: str = None
    ) -> Dict[str, Any]:
        """
        Create a default configuration file.
        
        Args:
            config_file: Path to create configuration file (optional)
            
        Returns:
            Response indicating success or failure with file path
        """
        try:
            from tools.config_manager import get_config_manager
            
            config_manager = get_config_manager()
            config_path = Path(config_file) if config_file else None
            
            created_path = config_manager.create_default_config(config_path)
            
            result = {
                "success": True,
                "message": "Default configuration file created successfully",
                "config_file": str(created_path)
            }
            
            logger.info(f"Default configuration created at: {created_path}")
            return result
            
        except Exception as e:
            error_msg = f"Error creating default configuration: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def validate_config(
        ctx: Context,
        config_file: str = None
    ) -> Dict[str, Any]:
        """
        Validate configuration file.
        
        Args:
            config_file: Path to configuration file to validate (optional, uses current if not provided)
            
        Returns:
            Response with validation results
        """
        try:
            from tools.config_manager import get_config_manager
            
            config_manager = get_config_manager()
            
            if config_file:
                config_path = Path(config_file)
                if not config_path.exists():
                    return {"success": False, "message": f"Configuration file not found: {config_file}"}
                config = config_manager.load_config(config_path)
            else:
                config = config_manager.get_config()
            
            issues = config_manager.validate_config(config)
            
            result = {
                "success": True,
                "valid": len(issues) == 0,
                "issues": issues,
                "message": "Configuration is valid" if len(issues) == 0 else f"Configuration has {len(issues)} issue(s)"
            }
            
            logger.info(f"Configuration validation completed: {len(issues)} issues found")
            return result
            
        except Exception as e:
            error_msg = f"Error validating configuration: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def reload_config(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Reload configuration from file.
        
        Returns:
            Response indicating success or failure with reloaded configuration
        """
        try:
            from tools.config_manager import get_config_manager
            
            config_manager = get_config_manager()
            config = config_manager.reload_config()
            
            result = {
                "success": True,
                "message": "Configuration reloaded successfully",
                "config_file": str(config_manager._config_file_path) if config_manager._config_file_path else None,
                "configuration": config.dict()
            }
            
            logger.info("Configuration reloaded successfully")
            return result
            
        except Exception as e:
            error_msg = f"Error reloading configuration: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_tool_config(
        ctx: Context,
        tool_name: str
    ) -> Dict[str, Any]:
        """
        Get configuration for a specific tool.
        
        Args:
            tool_name: Name of the tool to get configuration for
            
        Returns:
            Response with tool configuration
        """
        try:
            from tools.config_manager import get_config_manager
            
            config_manager = get_config_manager()
            tool_config = config_manager.get_tool_config(tool_name)
            
            result = {
                "success": True,
                "tool_name": tool_name,
                "tool_config": tool_config.dict()
            }
            
            logger.info(f"Tool configuration retrieved for: {tool_name}")
            return result
            
        except Exception as e:
            error_msg = f"Error getting tool configuration: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def update_tool_config(
        ctx: Context,
        tool_name: str,
        tool_config_data: str
    ) -> Dict[str, Any]:
        """
        Update configuration for a specific tool.
        
        Args:
            tool_name: Name of the tool to update configuration for
            tool_config_data: JSON string containing tool configuration data
            
        Returns:
            Response indicating success or failure
        """
        try:
            from tools.config_manager import get_config_manager, ToolConfig
            
            # Parse tool configuration data
            config_dict = json.loads(tool_config_data)
            
            # Validate tool configuration
            tool_config = ToolConfig(**config_dict)
            
            config_manager = get_config_manager()
            config_manager.update_tool_config(tool_name, tool_config)
            
            result = {
                "success": True,
                "message": f"Tool configuration updated successfully for: {tool_name}",
                "tool_name": tool_name,
                "tool_config": tool_config.dict()
            }
            
            logger.info(f"Tool configuration updated for: {tool_name}")
            return result
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in tool configuration data: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Error updating tool configuration: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def check_config_changes(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Check if configuration file has changed since last load.
        
        Returns:
            Response indicating if configuration has changed
        """
        try:
            from tools.config_manager import get_config_manager
            
            config_manager = get_config_manager()
            has_changed = config_manager.has_config_changed()
            
            result = {
                "success": True,
                "config_changed": has_changed,
                "message": "Configuration has changed" if has_changed else "Configuration is up to date",
                "config_file": str(config_manager._config_file_path) if config_manager._config_file_path else None
            }
            
            logger.info(f"Configuration change check: {'changed' if has_changed else 'unchanged'}")
            return result
            
        except Exception as e:
            error_msg = f"Error checking configuration changes: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def list_config_files(
        ctx: Context,
        config_dir: str = None
    ) -> Dict[str, Any]:
        """
        List available configuration files in the config directory.
        
        Args:
            config_dir: Directory to search for configuration files (optional)
            
        Returns:
            Response with list of configuration files
        """
        try:
            from tools.config_manager import ConfigManager
            
            if config_dir:
                config_manager = ConfigManager(Path(config_dir))
            else:
                config_manager = ConfigManager()
            
            config_files = []
            config_extensions = ['.yaml', '.yml', '.json', '.toml']
            
            # Search in config directory
            for file_path in config_manager.config_dir.glob("*"):
                if file_path.is_file() and file_path.suffix.lower() in config_extensions:
                    config_files.append({
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime
                    })
            
            # Search in current directory if different from config directory
            if config_manager.config_dir != Path.cwd():
                for file_path in Path.cwd().glob("*"):
                    if file_path.is_file() and file_path.suffix.lower() in config_extensions:
                        config_files.append({
                            "name": file_path.name,
                            "path": str(file_path),
                            "size": file_path.stat().st_size,
                            "modified": file_path.stat().st_mtime
                        })
            
            result = {
                "success": True,
                "config_dir": str(config_manager.config_dir),
                "config_files": config_files,
                "count": len(config_files)
            }
            
            logger.info(f"Found {len(config_files)} configuration files")
            return result
            
        except Exception as e:
            error_msg = f"Error listing configuration files: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("Project tools registered successfully") 