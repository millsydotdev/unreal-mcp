"""
UMG Discovery Tools for Unreal MCP.

This module provides tools for discovering, inspecting, and validating UMG Widget Blueprints.
Includes comprehensive widget search, component inspection, and hierarchy validation.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_umg_discovery_tools(mcp: FastMCP):
    """Register UMG discovery tools with the MCP server."""

    @mcp.tool()
    def search_items(
        ctx: Context,
        search_term: str = "",
        asset_type: str = "Widget",
        path: str = "/Game",
        case_sensitive: bool = False
    ) -> Dict[str, Any]:
        """
        Search for assets in the Unreal Engine project.
        
        ⚠️ CRITICAL FOR AI ASSISTANTS: Always use this tool before modifying widgets or assets.
        Widget names are case-sensitive and must match exactly. This tool provides the exact names.
        
        Args:
            search_term: Text to search for (empty string returns all assets of type)
            asset_type: Type of asset to search for (Widget, Blueprint, Material, etc.)
            path: Content browser path to search within (default: /Game)
            case_sensitive: Whether search should be case sensitive
            
        Returns:
            Dict containing array of matching assets with name, path, and type information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "search_term": search_term,
                "asset_type": asset_type,
                "path": path,
                "case_sensitive": case_sensitive
            }
            
            logger.info(f"Searching for assets with params: {params}")
            response = unreal.send_command("search_items", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Asset search response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error searching assets: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_widget_blueprint_info(
        ctx: Context,
        widget_name: str
    ) -> Dict[str, Any]:
        """
        Get comprehensive information about a Widget Blueprint.
        
        Provides complete widget structure including:
        - Component hierarchy and relationships
        - Property bindings and data sources
        - Event connections and delegates
        - Layout constraints and sizing
        - Animation and transition information
        
        Args:
            widget_name: Name of the widget blueprint to inspect
            
        Returns:
            Dict containing complete widget structure and metadata
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"widget_name": widget_name}
            
            logger.info(f"Getting widget blueprint info for: {widget_name}")
            response = unreal.send_command("get_widget_blueprint_info", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget blueprint info response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting widget blueprint info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def list_widget_components(
        ctx: Context,
        widget_name: str
    ) -> Dict[str, Any]:
        """
        List all components in a Widget Blueprint with their hierarchy and properties.
        
        Shows the complete component tree structure, making it easy to understand
        widget organization and find specific components for modification.
        
        Args:
            widget_name: Name of the widget blueprint to inspect
            
        Returns:
            Dict containing component hierarchy with names, types, and relationships
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"widget_name": widget_name}
            
            logger.info(f"Listing widget components for: {widget_name}")
            response = unreal.send_command("list_widget_components", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget components response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error listing widget components: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def validate_widget_hierarchy(
        ctx: Context,
        widget_name: str
    ) -> Dict[str, Any]:
        """
        Validate widget structure for issues and optimization opportunities.
        
        Checks for common problems like:
        - Missing or invalid parent-child relationships
        - Circular references in component hierarchy
        - Performance issues with deep nesting
        - Layout constraint conflicts
        - Missing required properties
        
        Args:
            widget_name: Name of the widget blueprint to validate
            
        Returns:
            Dict containing validation results with warnings and recommendations
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"widget_name": widget_name}
            
            logger.info(f"Validating widget hierarchy for: {widget_name}")
            response = unreal.send_command("validate_widget_hierarchy", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget hierarchy validation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error validating widget hierarchy: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_widget_component_properties(
        ctx: Context,
        widget_name: str,
        component_name: str
    ) -> Dict[str, Any]:
        """
        Get all properties of a specific widget component with current values.
        
        Provides detailed property information including:
        - Current property values
        - Property types and constraints
        - Available options for enum properties
        - Binding information for bound properties
        - Inheritance hierarchy for inherited properties
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component to inspect
            
        Returns:
            Dict containing all component properties with values and metadata
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "component_name": component_name
            }
            
            logger.info(f"Getting component properties for {component_name} in {widget_name}")
            response = unreal.send_command("get_widget_component_properties", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Component properties response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting component properties: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def list_widget_properties(
        ctx: Context,
        widget_name: str,
        component_name: str,
        include_inherited: bool = True,
        category_filter: str = ""
    ) -> Dict[str, Any]:
        """
        List available properties for a widget component with metadata.
        
        Provides comprehensive property information including:
        - Property names and types
        - Default values and constraints
        - Property categories and descriptions
        - Binding capabilities
        - Animation support
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component to inspect
            include_inherited: Whether to include inherited properties
            category_filter: Filter properties by category (e.g., "Appearance", "Layout")
            
        Returns:
            Dict containing property list with metadata and categories
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
                "include_inherited": include_inherited,
                "category_filter": category_filter
            }
            
            logger.info(f"Listing widget properties for {component_name} in {widget_name}")
            response = unreal.send_command("list_widget_properties", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget properties response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error listing widget properties: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_widget_property(
        ctx: Context,
        widget_name: str,
        component_name: str,
        property_name: str
    ) -> Dict[str, Any]:
        """
        Get the current value of a specific widget property.
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component
            property_name: Name of the property to get
            
        Returns:
            Dict containing the current property value and metadata
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
                "property_name": property_name
            }
            
            logger.info(f"Getting widget property {property_name} for {component_name} in {widget_name}")
            response = unreal.send_command("get_widget_property", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget property response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting widget property: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_available_events(
        ctx: Context,
        widget_name: str,
        component_name: str
    ) -> Dict[str, Any]:
        """
        List all available events for a widget component.
        
        Shows available events including:
        - Built-in events (OnClicked, OnHovered, etc.)
        - Custom events defined in the widget
        - Delegate events that can be bound
        - Animation events and triggers
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component to inspect
            
        Returns:
            Dict containing list of available events with binding information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "component_name": component_name
            }
            
            logger.info(f"Getting available events for {component_name} in {widget_name}")
            response = unreal.send_command("get_available_events", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Available events response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting available events: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
