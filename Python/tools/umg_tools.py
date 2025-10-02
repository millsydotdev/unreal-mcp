"""
UMG Tools for Unreal MCP.

This module provides comprehensive tools for creating and manipulating UMG Widget Blueprints in Unreal Engine.
Supports a wide range of widget components, layout management, styling, and event handling.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_umg_tools(mcp: FastMCP):
    """Register UMG tools with the MCP server."""

    @mcp.tool()
    def create_umg_widget_blueprint(
        ctx: Context,
        widget_name: str,
        parent_class: str = "UserWidget",
        path: str = "/Game/UI"
    ) -> Dict[str, Any]:
        """
        Create a new UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the widget blueprint to create
            parent_class: Parent class for the widget (default: UserWidget)
            path: Content browser path where the widget should be created
            
        Returns:
            Dict containing success status and widget path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "parent_class": parent_class,
                "path": path
            }
            
            logger.info(f"Creating UMG Widget Blueprint with params: {params}")
            response = unreal.send_command("create_umg_widget_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Create UMG Widget Blueprint response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating UMG Widget Blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_text_block_to_widget(
        ctx: Context,
        widget_name: str,
        text_block_name: str,
        text: str = "",
        position: List[float] = [0.0, 0.0],
        size: List[float] = [200.0, 50.0],
        font_size: int = 12,
        color: List[float] = [1.0, 1.0, 1.0, 1.0]
    ) -> Dict[str, Any]:
        """
        Add a Text Block widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            text_block_name: Name to give the new Text Block
            text: Initial text content
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the text block
            font_size: Font size in points
            color: [R, G, B, A] color values (0.0 to 1.0)
            
        Returns:
            Dict containing success status and text block properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "text_block_name": text_block_name,
                "text": text,
                "position": position,
                "size": size,
                "font_size": font_size,
                "color": color
            }
            
            logger.info(f"Adding Text Block to widget with params: {params}")
            response = unreal.send_command("add_text_block_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Text Block response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding Text Block to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_button_to_widget(
        ctx: Context,
        widget_name: str,
        button_name: str,
        text: str = "",
        position: List[float] = [0.0, 0.0],
        size: List[float] = [200.0, 50.0],
        font_size: int = 12,
        color: List[float] = [1.0, 1.0, 1.0, 1.0],
        background_color: List[float] = [0.1, 0.1, 0.1, 1.0]
    ) -> Dict[str, Any]:
        """
        Add a Button widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            button_name: Name to give the new Button
            text: Text to display on the button
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the button
            font_size: Font size for button text
            color: [R, G, B, A] text color values (0.0 to 1.0)
            background_color: [R, G, B, A] button background color values (0.0 to 1.0)
            
        Returns:
            Dict containing success status and button properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "button_name": button_name,
                "text": text,
                "position": position,
                "size": size,
                "font_size": font_size,
                "color": color,
                "background_color": background_color
            }
            
            logger.info(f"Adding Button to widget with params: {params}")
            response = unreal.send_command("add_button_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Button response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding Button to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def bind_widget_event(
        ctx: Context,
        widget_name: str,
        widget_component_name: str,
        event_name: str,
        function_name: str = ""
    ) -> Dict[str, Any]:
        """
        Bind an event on a widget component to a function.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            widget_component_name: Name of the widget component (button, etc.)
            event_name: Name of the event to bind (OnClicked, etc.)
            function_name: Name of the function to create/bind to (defaults to f"{widget_component_name}_{event_name}")
            
        Returns:
            Dict containing success status and binding information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # If no function name provided, create one from component and event names
            if not function_name:
                function_name = f"{widget_component_name}_{event_name}"
            
            params = {
                "widget_name": widget_name,
                "widget_component_name": widget_component_name,
                "event_name": event_name,
                "function_name": function_name
            }
            
            logger.info(f"Binding widget event with params: {params}")
            response = unreal.send_command("bind_widget_event", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Bind widget event response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error binding widget event: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_widget_to_viewport(
        ctx: Context,
        widget_name: str,
        z_order: int = 0
    ) -> Dict[str, Any]:
        """
        Add a Widget Blueprint instance to the viewport.
        
        Args:
            widget_name: Name of the Widget Blueprint to add
            z_order: Z-order for the widget (higher numbers appear on top)
            
        Returns:
            Dict containing success status and widget instance information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "z_order": z_order
            }
            
            logger.info(f"Adding widget to viewport with params: {params}")
            response = unreal.send_command("add_widget_to_viewport", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add widget to viewport response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding widget to viewport: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_text_block_binding(
        ctx: Context,
        widget_name: str,
        text_block_name: str,
        binding_property: str,
        binding_type: str = "Text"
    ) -> Dict[str, Any]:
        """
        Set up a property binding for a Text Block widget.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            text_block_name: Name of the Text Block to bind
            binding_property: Name of the property to bind to
            binding_type: Type of binding (Text, Visibility, etc.)
            
        Returns:
            Dict containing success status and binding information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "text_block_name": text_block_name,
                "binding_property": binding_property,
                "binding_type": binding_type
            }
            
            logger.info(f"Setting text block binding with params: {params}")
            response = unreal.send_command("set_text_block_binding", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set text block binding response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting text block binding: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_image_to_widget(
        ctx: Context,
        widget_name: str,
        image_name: str,
        texture_path: str = "",
        position: List[float] = [0.0, 0.0],
        size: List[float] = [100.0, 100.0],
        tint_color: List[float] = [1.0, 1.0, 1.0, 1.0],
        draw_as: str = "Image"
    ) -> Dict[str, Any]:
        """
        Add an Image widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            image_name: Name to give the new Image widget
            texture_path: Path to the texture asset (optional)
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the image
            tint_color: [R, G, B, A] tint color values (0.0 to 1.0)
            draw_as: How to draw the image (Image, Border, Box)
            
        Returns:
            Dict containing success status and image properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "image_name": image_name,
                "texture_path": texture_path,
                "position": position,
                "size": size,
                "tint_color": tint_color,
                "draw_as": draw_as
            }
            
            logger.info(f"Adding Image to widget with params: {params}")
            response = unreal.send_command("add_image_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Image response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding Image to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_progress_bar_to_widget(
        ctx: Context,
        widget_name: str,
        progress_bar_name: str,
        position: List[float] = [0.0, 0.0],
        size: List[float] = [200.0, 20.0],
        percent: float = 0.0,
        fill_color: List[float] = [0.0, 1.0, 0.0, 1.0],
        background_color: List[float] = [0.2, 0.2, 0.2, 1.0]
    ) -> Dict[str, Any]:
        """
        Add a Progress Bar widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            progress_bar_name: Name to give the new Progress Bar
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the progress bar
            percent: Initial progress value (0.0 to 1.0)
            fill_color: [R, G, B, A] fill color values (0.0 to 1.0)
            background_color: [R, G, B, A] background color values (0.0 to 1.0)
            
        Returns:
            Dict containing success status and progress bar properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "progress_bar_name": progress_bar_name,
                "position": position,
                "size": size,
                "percent": percent,
                "fill_color": fill_color,
                "background_color": background_color
            }
            
            logger.info(f"Adding Progress Bar to widget with params: {params}")
            response = unreal.send_command("add_progress_bar_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Progress Bar response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding Progress Bar to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_slider_to_widget(
        ctx: Context,
        widget_name: str,
        slider_name: str,
        position: List[float] = [0.0, 0.0],
        size: List[float] = [200.0, 20.0],
        value: float = 0.5,
        min_value: float = 0.0,
        max_value: float = 1.0,
        step_size: float = 0.01
    ) -> Dict[str, Any]:
        """
        Add a Slider widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            slider_name: Name to give the new Slider
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the slider
            value: Initial slider value
            min_value: Minimum slider value
            max_value: Maximum slider value
            step_size: Step size for the slider
            
        Returns:
            Dict containing success status and slider properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "slider_name": slider_name,
                "position": position,
                "size": size,
                "value": value,
                "min_value": min_value,
                "max_value": max_value,
                "step_size": step_size
            }
            
            logger.info(f"Adding Slider to widget with params: {params}")
            response = unreal.send_command("add_slider_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Slider response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding Slider to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_checkbox_to_widget(
        ctx: Context,
        widget_name: str,
        checkbox_name: str,
        text: str = "",
        position: List[float] = [0.0, 0.0],
        size: List[float] = [200.0, 20.0],
        is_checked: bool = False
    ) -> Dict[str, Any]:
        """
        Add a CheckBox widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            checkbox_name: Name to give the new CheckBox
            text: Text to display next to the checkbox
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the checkbox
            is_checked: Initial checked state
            
        Returns:
            Dict containing success status and checkbox properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "checkbox_name": checkbox_name,
                "text": text,
                "position": position,
                "size": size,
                "is_checked": is_checked
            }
            
            logger.info(f"Adding CheckBox to widget with params: {params}")
            response = unreal.send_command("add_checkbox_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add CheckBox response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding CheckBox to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_combo_box_to_widget(
        ctx: Context,
        widget_name: str,
        combo_box_name: str,
        options: List[str] = None,
        position: List[float] = [0.0, 0.0],
        size: List[float] = [200.0, 30.0],
        default_index: int = 0
    ) -> Dict[str, Any]:
        """
        Add a ComboBox widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            combo_box_name: Name to give the new ComboBox
            options: List of option strings for the dropdown
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the combo box
            default_index: Index of the initially selected option
            
        Returns:
            Dict containing success status and combo box properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            if options is None:
                options = ["Option 1", "Option 2", "Option 3"]
            
            params = {
                "widget_name": widget_name,
                "combo_box_name": combo_box_name,
                "options": options,
                "position": position,
                "size": size,
                "default_index": default_index
            }
            
            logger.info(f"Adding ComboBox to widget with params: {params}")
            response = unreal.send_command("add_combo_box_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add ComboBox response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding ComboBox to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_vertical_box_to_widget(
        ctx: Context,
        widget_name: str,
        vertical_box_name: str,
        position: List[float] = [0.0, 0.0],
        size: List[float] = [200.0, 300.0],
        alignment: str = "Fill"
    ) -> Dict[str, Any]:
        """
        Add a VerticalBox widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            vertical_box_name: Name to give the new VerticalBox
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the vertical box
            alignment: Alignment of child widgets (Fill, Top, Center, Bottom)
            
        Returns:
            Dict containing success status and vertical box properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "vertical_box_name": vertical_box_name,
                "position": position,
                "size": size,
                "alignment": alignment
            }
            
            logger.info(f"Adding VerticalBox to widget with params: {params}")
            response = unreal.send_command("add_vertical_box_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add VerticalBox response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding VerticalBox to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_horizontal_box_to_widget(
        ctx: Context,
        widget_name: str,
        horizontal_box_name: str,
        position: List[float] = [0.0, 0.0],
        size: List[float] = [400.0, 50.0],
        alignment: str = "Fill"
    ) -> Dict[str, Any]:
        """
        Add a HorizontalBox widget to a UMG Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            horizontal_box_name: Name to give the new HorizontalBox
            position: [X, Y] position in the canvas panel
            size: [Width, Height] of the horizontal box
            alignment: Alignment of child widgets (Fill, Left, Center, Right)
            
        Returns:
            Dict containing success status and horizontal box properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "horizontal_box_name": horizontal_box_name,
                "position": position,
                "size": size,
                "alignment": alignment
            }
            
            logger.info(f"Adding HorizontalBox to widget with params: {params}")
            response = unreal.send_command("add_horizontal_box_to_widget", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add HorizontalBox response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding HorizontalBox to widget: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_widget_anchors(
        ctx: Context,
        widget_name: str,
        widget_component_name: str,
        anchor_min: List[float] = [0.0, 0.0],
        anchor_max: List[float] = [1.0, 1.0],
        offset_min: List[float] = [0.0, 0.0],
        offset_max: List[float] = [0.0, 0.0]
    ) -> Dict[str, Any]:
        """
        Set anchor and offset properties for a widget component.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            widget_component_name: Name of the widget component to modify
            anchor_min: Minimum anchor point [X, Y] (0.0 to 1.0)
            anchor_max: Maximum anchor point [X, Y] (0.0 to 1.0)
            offset_min: Minimum offset from anchor
            offset_max: Maximum offset from anchor
            
        Returns:
            Dict containing success status and anchor information
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
                "anchor_min": anchor_min,
                "anchor_max": anchor_max,
                "offset_min": offset_min,
                "offset_max": offset_max
            }
            
            logger.info(f"Setting widget anchors with params: {params}")
            response = unreal.send_command("set_widget_anchors", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set widget anchors response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting widget anchors: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_widget_visibility(
        ctx: Context,
        widget_name: str,
        widget_component_name: str,
        visibility: str = "Visible"
    ) -> Dict[str, Any]:
        """
        Set the visibility of a widget component.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            widget_component_name: Name of the widget component to modify
            visibility: Visibility state (Visible, Hidden, Collapsed, HitTestInvisible, SelfHitTestInvisible)
            
        Returns:
            Dict containing success status and visibility information
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
                "visibility": visibility
            }
            
            logger.info(f"Setting widget visibility with params: {params}")
            response = unreal.send_command("set_widget_visibility", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set widget visibility response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting widget visibility: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_widget_hierarchy(
        ctx: Context,
        widget_name: str
    ) -> Dict[str, Any]:
        """
        Get the widget hierarchy of a Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            
        Returns:
            Dict containing the widget hierarchy structure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name
            }
            
            logger.info(f"Getting widget hierarchy with params: {params}")
            response = unreal.send_command("get_widget_hierarchy", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get widget hierarchy response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting widget hierarchy: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def remove_widget_from_blueprint(
        ctx: Context,
        widget_name: str,
        widget_component_name: str
    ) -> Dict[str, Any]:
        """
        Remove a widget component from a Widget Blueprint.
        
        Args:
            widget_name: Name of the target Widget Blueprint
            widget_component_name: Name of the widget component to remove
            
        Returns:
            Dict containing success status and removal information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "widget_name": widget_name,
                "widget_component_name": widget_component_name
            }
            
            logger.info(f"Removing widget from blueprint with params: {params}")
            response = unreal.send_command("remove_widget_from_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Remove widget response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error removing widget from blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    logger.info("Enhanced UMG tools registered successfully") 