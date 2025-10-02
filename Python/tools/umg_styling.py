"""
UMG Styling Tools for Unreal MCP.

This module provides advanced styling and theming capabilities for UMG Widget Blueprints.
Includes style sets, theming systems, and comprehensive property management.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_umg_styling_tools(mcp: FastMCP):
    """Register UMG styling tools with the MCP server."""

    @mcp.tool()
    def create_widget_style_set(
        ctx: Context,
        style_set_name: str,
        style_properties: Dict[str, Any],
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create a reusable style set for consistent theming across widgets.
        
        Style sets allow you to define common styling properties that can be applied
        to multiple components, ensuring consistent theming throughout your UI.
        
        Example style properties:
        {
            "BackgroundColor": {"R": 0.08, "G": 0.15, "B": 0.4, "A": 0.95},
            "BorderBrush": {"R": 0, "G": 0.6, "B": 1, "A": 1},
            "Font": {"Size": 14, "TypefaceFontName": "Bold"},
            "Padding": {"Left": 10, "Top": 5, "Right": 10, "Bottom": 5},
            "RenderOpacity": 0.92
        }
        
        Args:
            style_set_name: Unique name for the style set
            style_properties: Dictionary of style properties to define
            description: Optional description of the style set
            
        Returns:
            Dict containing style set creation confirmation and metadata
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "style_set_name": style_set_name,
                "style_properties": style_properties,
                "description": description
            }
            
            logger.info(f"Creating widget style set: {style_set_name}")
            response = unreal.send_command("create_widget_style_set", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Style set creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating style set: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def apply_widget_theme(
        ctx: Context,
        widget_name: str,
        component_name: str,
        theme_name: str
    ) -> Dict[str, Any]:
        """
        Apply a stored style set to a specific widget component.
        
        This allows you to quickly apply consistent styling across multiple components
        using pre-defined style sets.
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component to style
            theme_name: Name of the style set to apply
            
        Returns:
            Dict containing theme application confirmation
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
                "theme_name": theme_name
            }
            
            logger.info(f"Applying theme {theme_name} to {component_name} in {widget_name}")
            response = unreal.send_command("apply_widget_theme", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Theme application response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error applying theme: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_widget_style(
        ctx: Context,
        widget_name: str,
        component_name: str,
        style_properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set multiple style properties on a widget component at once.
        
        More efficient than setting properties individually when making multiple
        style changes to a component.
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component to style
            style_properties: Dictionary of style properties to set
            
        Returns:
            Dict containing style application confirmation
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
                "style_properties": style_properties
            }
            
            logger.info(f"Setting widget style for {component_name} in {widget_name}")
            response = unreal.send_command("set_widget_style", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget style response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error setting widget style: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_widget_slot_properties(
        ctx: Context,
        widget_name: str,
        widget_component_name: str,
        slot_properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set slot-specific properties for layout containers.
        
        Slot properties control how widgets are positioned and sized within
        their parent containers (Canvas, Box, Grid, etc.).
        
        Common slot properties:
        - Padding: {"Left": 10, "Top": 5, "Right": 10, "Bottom": 5}
        - Alignment: {"X": 0.5, "Y": 0.5}  # Center alignment
        - Anchors: {"Min": [0.0, 0.0], "Max": [1.0, 1.0]}  # Full stretch
        - Size: {"X": 200, "Y": 100}  # Fixed size
        
        Args:
            widget_name: Name of the widget blueprint
            widget_component_name: Name of the widget component
            slot_properties: Dictionary of slot properties to set
            
        Returns:
            Dict containing slot property update confirmation
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "widget_component_name": widget_component_name,
                "slot_properties": slot_properties
            }
            
            logger.info(f"Setting slot properties for {widget_component_name} in {widget_name}")
            response = unreal.send_command("set_widget_slot_properties", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Slot properties response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error setting slot properties: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_widget_style_guide() -> Dict[str, Any]:
        """
        Get comprehensive styling guide and best practices for UMG widgets.
        
        Provides detailed information about:
        - Color format specifications (RGBA values)
        - Font property configurations
        - Layout and sizing strategies
        - Animation property formats
        - Performance optimization tips
        - Common styling patterns
        
        Returns:
            Dict containing comprehensive styling guide and examples
        """
        return {
            "success": True,
            "style_guide": {
                "color_formats": {
                    "rgba": "Values from 0.0 to 1.0 for each component",
                    "examples": {
                        "white": {"R": 1.0, "G": 1.0, "B": 1.0, "A": 1.0},
                        "black": {"R": 0.0, "G": 0.0, "B": 0.0, "A": 1.0},
                        "transparent_blue": {"R": 0.0, "G": 0.0, "B": 1.0, "A": 0.5}
                    }
                },
                "font_properties": {
                    "size": "Font size in points (integer)",
                    "typeface": "Font family name (string)",
                    "example": {"Size": 16, "TypefaceFontName": "Bold"}
                },
                "layout_properties": {
                    "padding": {"Left": 10, "Top": 5, "Right": 10, "Bottom": 5},
                    "margin": {"Left": 5, "Top": 2, "Right": 5, "Bottom": 2},
                    "alignment": {"X": 0.5, "Y": 0.5},  # Center
                    "anchors": {"Min": [0.0, 0.0], "Max": [1.0, 1.0]}  # Full stretch
                },
                "best_practices": [
                    "Use style sets for consistent theming across multiple widgets",
                    "Apply themes after creating components for better performance",
                    "Use appropriate container types for different layout needs",
                    "Test styling on different screen resolutions",
                    "Keep style properties organized by category"
                ],
                "performance_tips": [
                    "Minimize nested styling overrides",
                    "Use native widget properties when possible",
                    "Cache frequently used style sets",
                    "Avoid excessive transparency for better rendering performance"
                ]
            }
        }

    @mcp.tool()
    def list_available_style_sets() -> Dict[str, Any]:
        """
        List all available style sets in the project.
        
        Returns:
            Dict containing list of available style sets with descriptions
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Listing available style sets")
            response = unreal.send_command("list_available_style_sets", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Available style sets response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error listing style sets: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_style_set_properties(
        ctx: Context,
        style_set_name: str
    ) -> Dict[str, Any]:
        """
        Get the properties defined in a specific style set.
        
        Args:
            style_set_name: Name of the style set to inspect
            
        Returns:
            Dict containing style set properties and metadata
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"style_set_name": style_set_name}
            
            logger.info(f"Getting style set properties for: {style_set_name}")
            response = unreal.send_command("get_style_set_properties", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Style set properties response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting style set properties: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
