"""
UMG Events Tools for Unreal MCP.

This module provides comprehensive event binding and interaction capabilities for UMG Widget Blueprints.
Includes input events, custom events, delegates, and animation triggers.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_umg_event_tools(mcp: FastMCP):
    """Register UMG event tools with the MCP server."""

    @mcp.tool()
    def bind_input_events(
        ctx: Context,
        widget_name: str,
        component_name: str,
        input_events: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Bind multiple input events to a widget component at once.
        
        Input events define what happens when users interact with the widget.
        Common events include OnClicked, OnHovered, OnPressed, OnReleased, etc.
        
        Example input_events:
        {
            "OnClicked": "HandleButtonClick",
            "OnHovered": "HandleButtonHover",
            "OnPressed": "HandleButtonPress"
        }
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component to bind events to
            input_events: Dictionary mapping event names to function names
            
        Returns:
            Dict containing event binding confirmation and details
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
                "input_events": input_events
            }
            
            logger.info(f"Binding input events for {component_name} in {widget_name}")
            response = unreal.send_command("bind_input_events", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input events binding response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error binding input events: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def create_custom_event(
        ctx: Context,
        widget_name: str,
        event_name: str,
        event_parameters: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a custom event in a Widget Blueprint.
        
        Custom events allow you to define your own event functions that can be
        called from other parts of your widget or from external code.
        
        Args:
            widget_name: Name of the widget blueprint
            event_name: Name of the custom event to create
            event_parameters: List of parameter definitions for the event
            
        Returns:
            Dict containing custom event creation confirmation
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "event_name": event_name,
                "event_parameters": event_parameters or []
            }
            
            logger.info(f"Creating custom event {event_name} in {widget_name}")
            response = unreal.send_command("create_custom_event", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Custom event creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating custom event: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def bind_delegate_event(
        ctx: Context,
        widget_name: str,
        component_name: str,
        delegate_name: str,
        target_function: str
    ) -> Dict[str, Any]:
        """
        Bind a delegate event to a target function.
        
        Delegates provide a way to call multiple functions when an event occurs,
        allowing for flexible event handling patterns.
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component containing the delegate
            delegate_name: Name of the delegate to bind
            target_function: Name of the function to bind to the delegate
            
        Returns:
            Dict containing delegate binding confirmation
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
                "delegate_name": delegate_name,
                "target_function": target_function
            }
            
            logger.info(f"Binding delegate {delegate_name} to {target_function} in {widget_name}")
            response = unreal.send_command("bind_delegate_event", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Delegate binding response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error binding delegate event: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def create_animation_event(
        ctx: Context,
        widget_name: str,
        animation_name: str,
        event_name: str,
        trigger_time: float
    ) -> Dict[str, Any]:
        """
        Create an animation event that triggers at a specific time during animation playback.
        
        Animation events allow you to trigger functions or other events at specific
        points during widget animations.
        
        Args:
            widget_name: Name of the widget blueprint
            animation_name: Name of the animation sequence
            event_name: Name of the event to trigger
            trigger_time: Time in seconds when the event should trigger
            
        Returns:
            Dict containing animation event creation confirmation
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "animation_name": animation_name,
                "event_name": event_name,
                "trigger_time": trigger_time
            }
            
            logger.info(f"Creating animation event {event_name} at {trigger_time}s in {widget_name}")
            response = unreal.send_command("create_animation_event", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Animation event creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating animation event: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def list_widget_events(
        ctx: Context,
        widget_name: str
    ) -> Dict[str, Any]:
        """
        List all events defined in a Widget Blueprint.
        
        Shows both built-in events and custom events, including:
        - Input events (OnClicked, OnHovered, etc.)
        - Custom events created by the user
        - Delegate events and their bindings
        - Animation events and triggers
        
        Args:
            widget_name: Name of the widget blueprint to inspect
            
        Returns:
            Dict containing comprehensive list of all widget events
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"widget_name": widget_name}
            
            logger.info(f"Listing events for widget: {widget_name}")
            response = unreal.send_command("list_widget_events", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget events response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error listing widget events: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_event_bindings(
        ctx: Context,
        widget_name: str,
        component_name: str
    ) -> Dict[str, Any]:
        """
        Get all event bindings for a specific widget component.
        
        Shows which events are bound and what functions they call.
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component to inspect
            
        Returns:
            Dict containing event binding information
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
            
            logger.info(f"Getting event bindings for {component_name} in {widget_name}")
            response = unreal.send_command("get_event_bindings", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Event bindings response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting event bindings: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def remove_event_binding(
        ctx: Context,
        widget_name: str,
        component_name: str,
        event_name: str
    ) -> Dict[str, Any]:
        """
        Remove an event binding from a widget component.
        
        Args:
            widget_name: Name of the widget blueprint
            component_name: Name of the component
            event_name: Name of the event to unbind
            
        Returns:
            Dict containing event removal confirmation
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
                "event_name": event_name
            }
            
            logger.info(f"Removing event binding {event_name} from {component_name} in {widget_name}")
            response = unreal.send_command("remove_event_binding", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Event binding removal response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error removing event binding: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_event_guide() -> Dict[str, Any]:
        """
        Get comprehensive guide for UMG event system and best practices.
        
        Returns:
            Dict containing event system guide with examples and patterns
        """
        return {
            "success": True,
            "event_guide": {
                "input_events": {
                    "button": ["OnClicked", "OnHovered", "OnPressed", "OnReleased"],
                    "text_input": ["OnTextChanged", "OnTextCommitted", "OnFocusReceived", "OnFocusLost"],
                    "slider": ["OnValueChanged", "OnMouseCaptureBegin", "OnMouseCaptureEnd"],
                    "checkbox": ["OnCheckStateChanged"]
                },
                "custom_events": {
                    "purpose": "Define your own events for widget communication",
                    "parameters": "Can accept parameters like functions",
                    "usage": "Call from Blueprint graphs or external code"
                },
                "delegates": {
                    "purpose": "Allow multiple functions to respond to one event",
                    "types": ["Single-cast", "Multi-cast"],
                    "binding": "Can bind/unbind functions dynamically"
                },
                "best_practices": [
                    "Use descriptive event and function names",
                    "Keep event handling functions simple and focused",
                    "Use custom events for widget-to-widget communication",
                    "Test event handling thoroughly with user interactions",
                    "Document event parameters and expected behavior"
                ],
                "common_patterns": [
                    "Button click handlers for navigation",
                    "Text input validation events",
                    "Slider value change callbacks",
                    "Animation completion triggers"
                ]
            }
        }
