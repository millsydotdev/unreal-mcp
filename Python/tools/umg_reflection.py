"""
UMG Reflection Tools for Unreal MCP.

This module provides reflection-based widget discovery and creation using Unreal's
reflection system. Enables generic widget creation and advanced property manipulation.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_umg_reflection_tools(mcp: FastMCP):
    """Register UMG reflection tools with the MCP server."""

    @mcp.tool()
    def get_available_widget_types() -> Dict[str, Any]:
        """
        Get all available widget types that can be created through reflection.
        
        Returns comprehensive list of UMG widget classes that can be instantiated,
        including their inheritance hierarchy and available properties.
        
        Returns:
            Dict containing list of available widget types with metadata
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Getting available widget types")
            response = unreal.send_command("get_available_widget_types", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Available widget types response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting available widget types: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def create_widget_via_reflection(
        ctx: Context,
        widget_name: str,
        widget_type: str,
        parent_name: str = "",
        properties: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a widget using Unreal's reflection system.
        
        This is a generic widget creation method that can create any UMG widget type
        by using Unreal's reflection system to discover and instantiate widget classes.
        
        Args:
            widget_name: Name of the widget blueprint
            widget_type: Type of widget to create (e.g., "Button", "TextBlock", "Image")
            parent_name: Name of parent widget (optional)
            properties: Dictionary of properties to set on the widget
            
        Returns:
            Dict containing widget creation confirmation and metadata
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "widget_type": widget_type,
                "parent_name": parent_name,
                "properties": properties or {}
            }
            
            logger.info(f"Creating widget via reflection: {widget_type} in {widget_name}")
            response = unreal.send_command("create_widget_via_reflection", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Reflection widget creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating widget via reflection: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_widget_type_info(
        ctx: Context,
        widget_type: str
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific widget type.
        
        Provides comprehensive information about widget properties, inheritance,
        available events, and creation parameters.
        
        Args:
            widget_type: Name of the widget type to inspect
            
        Returns:
            Dict containing detailed widget type information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"widget_type": widget_type}
            
            logger.info(f"Getting widget type info for: {widget_type}")
            response = unreal.send_command("get_widget_type_info", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget type info response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting widget type info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_widget_property_via_reflection(
        ctx: Context,
        widget_name: str,
        component_name: str,
        property_name: str,
        property_value: Any,
        property_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        Set widget properties using reflection system.
        
        This method uses Unreal's reflection system to set properties on widgets,
        providing more flexibility than direct property setting methods.
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component
            property_name: Name of the property to set
            property_value: Value to set (will be converted based on property_type)
            property_type: Type of the property ("auto", "string", "float", "bool", etc.)
            
        Returns:
            Dict containing property setting confirmation
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "component_name": component_name,
                "property_name": property_name,
                "property_value": property_value,
                "property_type": property_type
            }
            
            logger.info(f"Setting widget property via reflection: {property_name} on {component_name}")
            response = unreal.send_command("set_widget_property_via_reflection", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Reflection property setting response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error setting widget property via reflection: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_widget_palette_info() -> Dict[str, Any]:
        """
        Get information about the UMG Widget Palette.
        
        Provides information about all widgets available in the UMG Widget Palette,
        organized by category and including descriptions and usage examples.
        
        Returns:
            Dict containing widget palette information organized by categories
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Getting widget palette information")
            response = unreal.send_command("get_widget_palette_info", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget palette info response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting widget palette info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def create_widget_from_palette(
        ctx: Context,
        widget_name: str,
        palette_widget_name: str,
        parent_name: str = "",
        custom_properties: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a widget based on a Widget Palette entry.
        
        This method creates widgets using the same patterns as the UMG Widget Palette,
        ensuring consistency with Unreal's standard widget creation workflow.
        
        Args:
            widget_name: Name of the widget blueprint
            palette_widget_name: Name of the widget from the palette
            parent_name: Name of parent widget (optional)
            custom_properties: Custom properties to override defaults
            
        Returns:
            Dict containing widget creation confirmation
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "palette_widget_name": palette_widget_name,
                "parent_name": parent_name,
                "custom_properties": custom_properties or {}
            }
            
            logger.info(f"Creating widget from palette: {palette_widget_name} in {widget_name}")
            response = unreal.send_command("create_widget_from_palette", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Palette widget creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating widget from palette: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_reflection_guide() -> Dict[str, Any]:
        """
        Get comprehensive guide for using UMG reflection tools.
        
        Returns:
            Dict containing reflection system guide with examples and best practices
        """
        return {
            "success": True,
            "reflection_guide": {
                "purpose": "Use Unreal's reflection system for generic widget creation and manipulation",
                "advantages": [
                    "Access to all UMG widget types",
                    "Generic property setting without specific tool methods",
                    "Future-proof against Unreal Engine updates",
                    "Consistent with Unreal's internal widget creation patterns"
                ],
                "common_widget_types": {
                    "layout": ["CanvasPanel", "VerticalBox", "HorizontalBox", "GridPanel", "ScrollBox"],
                    "controls": ["Button", "CheckBox", "Slider", "ProgressBar", "EditableText"],
                    "display": ["TextBlock", "RichTextBlock", "Image", "Border", "Spacer"],
                    "input": ["EditableTextBox", "MultiLineEditableTextBox", "ComboBox", "ListBox"]
                },
                "best_practices": [
                    "Use get_available_widget_types() to discover new widget types",
                    "Check widget type info before creating complex widgets",
                    "Use reflection for widgets not covered by specific tools",
                    "Test reflection-created widgets thoroughly",
                    "Document custom widget creation patterns"
                ],
                "workflow_examples": {
                    "discover_widgets": [
                        "1. Call get_available_widget_types()",
                        "2. Browse widget categories",
                        "3. Get detailed info with get_widget_type_info()"
                    ],
                    "create_custom_widget": [
                        "1. Use create_widget_via_reflection()",
                        "2. Set properties with set_widget_property_via_reflection()",
                        "3. Test and validate the widget"
                    ]
                }
            }
        }
