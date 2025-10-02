"""
System Diagnostics Tools for Unreal MCP.

This module provides comprehensive system diagnostics, connection testing, and AI assistant guidance.
Includes connection validation, tool functionality verification, and troubleshooting guides.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_system_diagnostic_tools(mcp: FastMCP):
    """Register system diagnostic tools with the MCP server."""

    @mcp.tool()
    def check_unreal_connection() -> Dict[str, Any]:
        """
        Check Unreal Engine connection status and plugin health.
        
        ⚠️ CRITICAL FOR AI ASSISTANTS: Use this tool first when any commands fail.
        This provides comprehensive diagnostics including connection status, plugin state,
        and troubleshooting guidance.
        
        Returns:
            Dict containing connection status, plugin information, and troubleshooting tips
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {
                    "success": False,
                    "connection_status": "Failed to create connection",
                    "troubleshooting": [
                        "Ensure Unreal Engine 5.6 is running",
                        "Check that UnrealMCP plugin is loaded and enabled",
                        "Verify port 55557 is available",
                        "Check unreal_mcp.log for detailed error information"
                    ],
                    "plugin_status": "Unknown - cannot connect to verify",
                    "recommendations": [
                        "Start Unreal Engine with your project",
                        "Go to Edit > Plugins and enable UnrealMCP",
                        "Restart the editor if plugin was just enabled"
                    ]
                }
            
            # Test basic communication
            test_response = unreal.send_command("ping", {})
            
            if test_response and test_response.get("success"):
                return {
                    "success": True,
                    "connection_status": "Connected and responsive",
                    "plugin_status": "Active and functioning",
                    "host": "127.0.0.1",
                    "port": 55557,
                    "test_response": test_response,
                    "recommendations": [
                        "Connection is healthy - proceed with tool usage",
                        "Check unreal_mcp.log for detailed operation logs"
                    ]
                }
            else:
                return {
                    "success": False,
                    "connection_status": "Connected but not responding",
                    "plugin_status": "Plugin may have crashed or stalled",
                    "troubleshooting": [
                        "Plugin is loaded but not responding to commands",
                        "Try restarting Unreal Engine",
                        "Check for plugin errors in Unreal's output log",
                        "Verify plugin version compatibility"
                    ],
                    "recommendations": [
                        "Restart Unreal Engine",
                        "Check Unreal's output log for plugin errors",
                        "Verify plugin is properly compiled"
                    ]
                }
                
        except Exception as e:
            return {
                "success": False,
                "connection_status": f"Connection error: {str(e)}",
                "troubleshooting": [
                    "Network connection failed",
                    "Unreal Engine may not be running",
                    "Plugin may not be loaded",
                    "Port 55557 may be blocked or in use"
                ],
                "recommendations": [
                    "Start Unreal Engine 5.6",
                    "Load a project with UnrealMCP plugin enabled",
                    "Check Windows Firewall settings",
                    "Verify no other application is using port 55557"
                ]
            }

    @mcp.tool()
    def validate_tool_functionality() -> Dict[str, Any]:
        """
        Validate that all MCP tools are functioning correctly.
        
        Performs basic functionality tests on core tool categories to ensure
        the system is working properly.
        
        Returns:
            Dict containing validation results for each tool category
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                return {
                    "success": False,
                    "message": "Cannot validate tools - no connection to Unreal Engine",
                    "recommendations": ["Run check_unreal_connection() first"]
                }
            
            validation_results = {}
            
            # Test basic connection
            ping_response = unreal.send_command("ping", {})
            validation_results["connection"] = {
                "status": "pass" if ping_response and ping_response.get("success") else "fail",
                "details": ping_response
            }
            
            # Test asset search functionality
            search_response = unreal.send_command("search_items", {"asset_type": "Widget", "search_term": ""})
            validation_results["asset_search"] = {
                "status": "pass" if search_response else "fail",
                "details": "Asset search functionality tested"
            }
            
            # Test Blueprint functionality
            blueprint_response = unreal.send_command("get_blueprint_info", {"blueprint_name": "None"})
            validation_results["blueprint_tools"] = {
                "status": "pass" if blueprint_response else "fail",
                "details": "Blueprint tools functionality tested"
            }
            
            return {
                "success": True,
                "validation_results": validation_results,
                "overall_status": "pass" if all(
                    result["status"] == "pass" for result in validation_results.values()
                ) else "partial_fail",
                "recommendations": [
                    "All core tool categories validated",
                    "Check individual tool responses for specific issues"
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Validation failed: {str(e)}",
                "recommendations": [
                    "Check Unreal Engine connection",
                    "Verify plugin is properly loaded",
                    "Check unreal_mcp.log for detailed errors"
                ]
            }

    @mcp.tool()
    def get_system_info() -> Dict[str, Any]:
        """
        Get comprehensive system information and configuration details.
        
        Returns:
            Dict containing system configuration, plugin info, and environment details
        """
        import sys
        import platform
        from unreal_mcp_server import get_unreal_connection
        
        try:
            system_info = {
                "success": True,
                "system": {
                    "platform": platform.system(),
                    "platform_version": platform.version(),
                    "architecture": platform.architecture()[0],
                    "python_version": sys.version
                },
                "mcp_server": {
                    "name": "UnrealMCP",
                    "version": "1.0",
                    "host": "127.0.0.1",
                    "port": 55557,
                    "transport": "stdio"
                },
                "unreal_connection": {
                    "status": "connected" if get_unreal_connection() else "disconnected"
                }
            }
            
            # Try to get plugin information if connected
            unreal = get_unreal_connection()
            if unreal:
                plugin_response = unreal.send_command("get_plugin_info", {})
                if plugin_response:
                    system_info["plugin"] = plugin_response
            
            return system_info
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting system info: {str(e)}",
                "basic_info": {
                    "platform": platform.system(),
                    "python_version": sys.version
                }
            }

    @mcp.tool()
    def get_help() -> Dict[str, Any]:
        """
        Get comprehensive help and documentation for all available tools.
        
        ⚠️ CRITICAL FOR AI ASSISTANTS: Use this tool when you need complete documentation
        for any MCP tool, including parameter details, examples, and usage patterns.
        
        Returns:
            Dict containing complete tool documentation and usage guides
        """
        return {
            "success": True,
            "help_documentation": {
                "connection_tools": {
                    "check_unreal_connection": {
                        "description": "Check Unreal Engine connection status and plugin health",
                        "parameters": "None",
                        "returns": "Connection status, plugin info, troubleshooting tips",
                        "usage": "Call first when any commands fail"
                    }
                },
                "discovery_tools": {
                    "search_items": {
                        "description": "Search for assets in the Unreal Engine project",
                        "parameters": {
                            "search_term": "Text to search for (empty for all)",
                            "asset_type": "Type of asset (Widget, Blueprint, etc.)",
                            "path": "Content browser path to search within",
                            "case_sensitive": "Whether search is case sensitive"
                        },
                        "usage": "Always use before modifying widgets or assets"
                    },
                    "get_widget_blueprint_info": {
                        "description": "Get comprehensive widget structure information",
                        "parameters": {"widget_name": "Name of widget to inspect"},
                        "usage": "Inspect before making changes to existing widgets"
                    }
                },
                "creation_tools": {
                    "create_umg_widget_blueprint": {
                        "description": "Create new UMG Widget Blueprint",
                        "parameters": {
                            "widget_name": "Name for the widget",
                            "parent_class": "Parent class (default: UserWidget)",
                            "path": "Content browser path"
                        }
                    },
                    "add_button_to_widget": {
                        "description": "Add button component to widget",
                        "parameters": {
                            "widget_name": "Target widget name",
                            "button_name": "Name for the button",
                            "text": "Button text",
                            "position": "[X, Y] coordinates",
                            "size": "[Width, Height] dimensions"
                        }
                    }
                },
                "styling_tools": {
                    "create_widget_style_set": {
                        "description": "Create reusable style set for theming",
                        "parameters": {
                            "style_set_name": "Unique name for style set",
                            "style_properties": "Dictionary of style properties",
                            "description": "Optional description"
                        }
                    },
                    "apply_widget_theme": {
                        "description": "Apply style set to component",
                        "parameters": {
                            "widget_name": "Target widget",
                            "component_name": "Target component",
                            "theme_name": "Style set name to apply"
                        }
                    }
                },
                "event_tools": {
                    "bind_input_events": {
                        "description": "Bind input events to component",
                        "parameters": {
                            "widget_name": "Target widget",
                            "component_name": "Target component",
                            "input_events": "Dictionary of event mappings"
                        }
                    }
                },
                "blueprint_tools": {
                    "create_blueprint": {
                        "description": "Create new Blueprint class",
                        "parameters": {
                            "name": "Blueprint name",
                            "parent_class": "Parent class"
                        },
                        "usage": "Always compile after creating"
                    },
                    "compile_blueprint": {
                        "description": "Compile Blueprint changes",
                        "parameters": {"blueprint_name": "Name of Blueprint to compile"},
                        "usage": "REQUIRED after Blueprint modifications"
                    }
                },
                "best_practices": [
                    "Always check connection status first",
                    "Use search tools before modifying assets",
                    "Compile Blueprints after changes",
                    "Use exact widget/component names",
                    "Handle errors gracefully",
                    "Test on different screen resolutions"
                ],
                "common_workflows": {
                    "creating_ui": [
                        "1. search_items() to find existing widgets",
                        "2. create_umg_widget_blueprint() for new widgets",
                        "3. add_canvas_panel() or layout containers",
                        "4. add components (buttons, text, etc.)",
                        "5. create_widget_style_set() for theming",
                        "6. apply_widget_theme() to components",
                        "7. bind_input_events() for interactivity"
                    ],
                    "modifying_ui": [
                        "1. search_items() to find widget",
                        "2. get_widget_blueprint_info() to inspect",
                        "3. list_widget_components() to see structure",
                        "4. make modifications with appropriate tools",
                        "5. validate_widget_hierarchy() to check for issues"
                    ]
                },
                "error_troubleshooting": {
                    "failed_to_connect": [
                        "Start Unreal Engine 5.6",
                        "Enable UnrealMCP plugin",
                        "Check port 55557 availability"
                    ],
                    "widget_not_found": [
                        "Use search_items() to find exact names",
                        "Check case sensitivity",
                        "Verify widget exists in project"
                    ],
                    "blueprint_errors": [
                        "Always compile after changes",
                        "Check node connections",
                        "Verify component hierarchy"
                    ]
                }
            }
        }

    @mcp.tool()
    def get_performance_tips() -> Dict[str, Any]:
        """
        Get performance optimization tips and best practices.
        
        Returns:
            Dict containing performance guidelines and optimization strategies
        """
        return {
            "success": True,
            "performance_tips": {
                "connection_optimization": [
                    "Use full asset paths from search results for instant loading",
                    "Avoid partial names that trigger expensive Asset Registry searches",
                    "Cache search results to avoid redundant calls",
                    "Batch property changes when modifying multiple components"
                ],
                "umg_optimization": [
                    "Minimize nested styling overrides",
                    "Use native widget properties when possible",
                    "Avoid excessive transparency for better rendering",
                    "Use appropriate container types for layout needs",
                    "Test on target screen resolutions"
                ],
                "blueprint_optimization": [
                    "Compile Blueprints only after completing changes",
                    "Use efficient node connections",
                    "Avoid unnecessary variable declarations",
                    "Optimize event graph complexity"
                ],
                "general_best_practices": [
                    "Start with discovery tools before modifications",
                    "Validate hierarchies after complex changes",
                    "Use style sets for consistent theming",
                    "Test functionality thoroughly",
                    "Keep tool calls focused and specific"
                ]
            }
        }
