"""
Enhanced Input Action Tools for Unreal MCP.

This module provides comprehensive tools for managing input actions, mappings, and advanced input features
in Unreal Engine. Includes support for multiple key bindings, axis mappings, input presets, and validation.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_enhanced_input_tools(mcp: FastMCP):
    """Register enhanced input action tools with the MCP server."""
    
    # ===== INPUT ACTION MAPPING TOOLS =====
    
    @mcp.tool()
    def create_enhanced_input_action_mapping(
        ctx: Context,
        action_name: str,
        primary_key: str,
        secondary_key: str = "",
        input_type: str = "Action",
        shift: bool = False,
        ctrl: bool = False,
        alt: bool = False,
        cmd: bool = False,
        category: str = "Default",
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create an enhanced input action mapping with multiple key bindings and metadata.
        
        Args:
            action_name: Name of the input action
            primary_key: Primary key to bind (SpaceBar, LeftMouseButton, etc.)
            secondary_key: Optional secondary key binding
            input_type: Type of input mapping (Action or Axis)
            shift: Whether Shift key modifier is required
            ctrl: Whether Ctrl key modifier is required
            alt: Whether Alt key modifier is required
            cmd: Whether Cmd key modifier is required (Mac only)
            category: Category for organizing input actions
            description: Description of the input action
            
        Returns:
            Response indicating success or failure with mapping details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "action_name": action_name,
                "primary_key": primary_key,
                "secondary_key": secondary_key,
                "input_type": input_type,
                "shift": shift,
                "ctrl": ctrl,
                "alt": alt,
                "cmd": cmd,
                "category": category,
                "description": description
            }
            
            logger.info(f"Creating enhanced input mapping '{action_name}' with keys '{primary_key}' and '{secondary_key}'")
            response = unreal.send_command("create_enhanced_input_action_mapping", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Enhanced input mapping creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating enhanced input mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_input_axis_mapping(
        ctx: Context,
        axis_name: str,
        positive_key: str,
        negative_key: str = "",
        scale: float = 1.0,
        category: str = "Default",
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create an input axis mapping for continuous input (movement, camera, etc.).
        
        Args:
            axis_name: Name of the input axis
            positive_key: Key for positive axis value (W, Up Arrow, etc.)
            negative_key: Key for negative axis value (S, Down Arrow, etc.)
            scale: Scale factor for the axis input
            category: Category for organizing input axes
            description: Description of the input axis
            
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
                "axis_name": axis_name,
                "positive_key": positive_key,
                "negative_key": negative_key,
                "scale": float(scale),
                "category": category,
                "description": description
            }
            
            logger.info(f"Creating input axis mapping '{axis_name}' with keys '{positive_key}' and '{negative_key}'")
            response = unreal.send_command("create_input_axis_mapping", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input axis mapping creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input axis mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_alternative_key_binding(
        ctx: Context,
        action_name: str,
        alternative_key: str,
        shift: bool = False,
        ctrl: bool = False,
        alt: bool = False,
        cmd: bool = False
    ) -> Dict[str, Any]:
        """
        Add an alternative key binding to an existing input action.
        
        Args:
            action_name: Name of the existing input action
            alternative_key: Alternative key to bind
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
                "alternative_key": alternative_key,
                "shift": shift,
                "ctrl": ctrl,
                "alt": alt,
                "cmd": cmd
            }
            
            logger.info(f"Adding alternative key binding '{alternative_key}' to action '{action_name}'")
            response = unreal.send_command("add_alternative_key_binding", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Alternative key binding response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding alternative key binding: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== INPUT ACTION MANAGEMENT TOOLS =====
    
    @mcp.tool()
    def list_input_actions(
        ctx: Context,
        category: str = "",
        include_axes: bool = True
    ) -> Dict[str, Any]:
        """
        List all input actions and axes in the project.
        
        Args:
            category: Filter by category (empty string for all)
            include_axes: Whether to include axis mappings
            
        Returns:
            List of input actions with their bindings and metadata
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "category": category,
                "include_axes": include_axes
            }
            
            logger.info(f"Listing input actions for category '{category}'")
            response = unreal.send_command("list_input_actions", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"List input actions response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error listing input actions: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def update_input_action_mapping(
        ctx: Context,
        action_name: str,
        new_key: str = "",
        new_shift: bool = None,
        new_ctrl: bool = None,
        new_alt: bool = None,
        new_cmd: bool = None,
        new_category: str = "",
        new_description: str = ""
    ) -> Dict[str, Any]:
        """
        Update an existing input action mapping.
        
        Args:
            action_name: Name of the input action to update
            new_key: New key binding (empty to keep existing)
            new_shift: New Shift modifier setting (None to keep existing)
            new_ctrl: New Ctrl modifier setting (None to keep existing)
            new_alt: New Alt modifier setting (None to keep existing)
            new_cmd: New Cmd modifier setting (None to keep existing)
            new_category: New category (empty to keep existing)
            new_description: New description (empty to keep existing)
            
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
                "new_key": new_key,
                "new_shift": new_shift,
                "new_ctrl": new_ctrl,
                "new_alt": new_alt,
                "new_cmd": new_cmd,
                "new_category": new_category,
                "new_description": new_description
            }
            
            logger.info(f"Updating input action mapping '{action_name}'")
            response = unreal.send_command("update_input_action_mapping", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Update input action response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error updating input action mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def remove_input_action_mapping(
        ctx: Context,
        action_name: str,
        key_binding: str = ""
    ) -> Dict[str, Any]:
        """
        Remove an input action mapping or specific key binding.
        
        Args:
            action_name: Name of the input action
            key_binding: Specific key binding to remove (empty to remove all bindings)
            
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
                "key_binding": key_binding
            }
            
            logger.info(f"Removing input action mapping '{action_name}' with key '{key_binding}'")
            response = unreal.send_command("remove_input_action_mapping", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Remove input action response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error removing input action mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== INPUT ACTION PRESETS AND TEMPLATES =====
    
    @mcp.tool()
    def create_input_preset(
        ctx: Context,
        preset_name: str,
        preset_type: str,
        custom_mappings: Dict[str, str] = {}
    ) -> Dict[str, Any]:
        """
        Create an input preset with common game input mappings.
        
        Args:
            preset_name: Name for the input preset
            preset_type: Type of preset (FPS, ThirdPerson, Platformer, Racing, Strategy)
            custom_mappings: Custom key mappings to override defaults
            
        Returns:
            Response indicating success or failure with created mappings
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "preset_name": preset_name,
                "preset_type": preset_type,
                "custom_mappings": custom_mappings
            }
            
            logger.info(f"Creating input preset '{preset_name}' of type '{preset_type}'")
            response = unreal.send_command("create_input_preset", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input preset creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input preset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def apply_input_preset(
        ctx: Context,
        preset_name: str,
        merge_with_existing: bool = True
    ) -> Dict[str, Any]:
        """
        Apply an existing input preset to the project.
        
        Args:
            preset_name: Name of the preset to apply
            merge_with_existing: Whether to merge with existing mappings or replace them
            
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
                "preset_name": preset_name,
                "merge_with_existing": merge_with_existing
            }
            
            logger.info(f"Applying input preset '{preset_name}'")
            response = unreal.send_command("apply_input_preset", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Apply input preset response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error applying input preset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ENHANCED BLUEPRINT INPUT TOOLS =====
    
    @mcp.tool()
    def create_enhanced_input_action_blueprint_node(
        ctx: Context,
        blueprint_name: str,
        action_name: str,
        event_type: str = "Pressed",
        node_position = None,
        auto_connect: bool = True
    ) -> Dict[str, Any]:
        """
        Create an enhanced input action node in a Blueprint with advanced features.
        
        Args:
            blueprint_name: Name of the target Blueprint
            action_name: Name of the input action to respond to
            event_type: Type of input event (Pressed, Released, Hold)
            node_position: Optional [X, Y] position in the graph
            auto_connect: Whether to automatically connect to BeginPlay if it exists
            
        Returns:
            Response containing the node ID and success status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            if node_position is None:
                node_position = [0, 0]
            
            params = {
                "blueprint_name": blueprint_name,
                "action_name": action_name,
                "event_type": event_type,
                "node_position": node_position,
                "auto_connect": auto_connect
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Creating enhanced input action node for '{action_name}' in blueprint '{blueprint_name}'")
            response = unreal.send_command("create_enhanced_input_action_blueprint_node", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Enhanced input action node creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating enhanced input action node: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_input_axis_blueprint_node(
        ctx: Context,
        blueprint_name: str,
        axis_name: str,
        node_position = None,
        auto_connect: bool = True
    ) -> Dict[str, Any]:
        """
        Create an input axis node in a Blueprint for continuous input.
        
        Args:
            blueprint_name: Name of the target Blueprint
            axis_name: Name of the input axis to respond to
            node_position: Optional [X, Y] position in the graph
            auto_connect: Whether to automatically connect to Tick if it exists
            
        Returns:
            Response containing the node ID and success status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            if node_position is None:
                node_position = [0, 0]
            
            params = {
                "blueprint_name": blueprint_name,
                "axis_name": axis_name,
                "node_position": node_position,
                "auto_connect": auto_connect
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Creating input axis node for '{axis_name}' in blueprint '{blueprint_name}'")
            response = unreal.send_command("create_input_axis_blueprint_node", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input axis node creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input axis node: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== INPUT VALIDATION AND TESTING TOOLS =====
    
    @mcp.tool()
    def validate_input_mappings(
        ctx: Context,
        check_conflicts: bool = True,
        check_missing_actions: bool = True,
        check_unused_actions: bool = True
    ) -> Dict[str, Any]:
        """
        Validate input mappings for conflicts, missing actions, and unused actions.
        
        Args:
            check_conflicts: Whether to check for key binding conflicts
            check_missing_actions: Whether to check for actions referenced in Blueprints but not mapped
            check_unused_actions: Whether to check for mapped actions not used in Blueprints
            
        Returns:
            Validation results with any issues found
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "check_conflicts": check_conflicts,
                "check_missing_actions": check_missing_actions,
                "check_unused_actions": check_unused_actions
            }
            
            logger.info("Validating input mappings")
            response = unreal.send_command("validate_input_mappings", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input validation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error validating input mappings: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def test_input_action(
        ctx: Context,
        action_name: str,
        duration: float = 5.0
    ) -> Dict[str, Any]:
        """
        Test an input action by monitoring its activation in real-time.
        
        Args:
            action_name: Name of the input action to test
            duration: Duration in seconds to monitor the action
            
        Returns:
            Test results showing when the action was triggered
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "action_name": action_name,
                "duration": float(duration)
            }
            
            logger.info(f"Testing input action '{action_name}' for {duration} seconds")
            response = unreal.send_command("test_input_action", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input action test response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error testing input action: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== INPUT IMPORT/EXPORT TOOLS =====
    
    @mcp.tool()
    def export_input_mappings(
        ctx: Context,
        file_path: str,
        format: str = "json",
        include_axes: bool = True,
        include_categories: bool = True
    ) -> Dict[str, Any]:
        """
        Export input mappings to a file.
        
        Args:
            file_path: Path where to save the exported mappings
            format: Export format (json, csv, ini)
            include_axes: Whether to include axis mappings
            include_categories: Whether to include category information
            
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
                "file_path": file_path,
                "format": format,
                "include_axes": include_axes,
                "include_categories": include_categories
            }
            
            logger.info(f"Exporting input mappings to '{file_path}' in {format} format")
            response = unreal.send_command("export_input_mappings", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Export input mappings response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error exporting input mappings: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def import_input_mappings(
        ctx: Context,
        file_path: str,
        merge_with_existing: bool = True,
        backup_existing: bool = True
    ) -> Dict[str, Any]:
        """
        Import input mappings from a file.
        
        Args:
            file_path: Path to the file containing input mappings
            merge_with_existing: Whether to merge with existing mappings or replace them
            backup_existing: Whether to backup existing mappings before import
            
        Returns:
            Response indicating success or failure with import details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "file_path": file_path,
                "merge_with_existing": merge_with_existing,
                "backup_existing": backup_existing
            }
            
            logger.info(f"Importing input mappings from '{file_path}'")
            response = unreal.send_command("import_input_mappings", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Import input mappings response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error importing input mappings: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ADVANCED INPUT FEATURES =====
    
    @mcp.tool()
    def create_input_context(
        ctx: Context,
        context_name: str,
        priority: int = 0,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create an input context for context-sensitive input handling.
        
        Args:
            context_name: Name of the input context
            priority: Priority level (higher numbers take precedence)
            description: Description of the input context
            
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
                "context_name": context_name,
                "priority": int(priority),
                "description": description
            }
            
            logger.info(f"Creating input context '{context_name}' with priority {priority}")
            response = unreal.send_command("create_input_context", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input context creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input context: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_input_trigger(
        ctx: Context,
        trigger_name: str,
        trigger_type: str,
        action_name: str,
        parameters: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Create an input trigger with custom conditions.
        
        Args:
            trigger_name: Name of the input trigger
            trigger_type: Type of trigger (Hold, Toggle, DoubleTap, etc.)
            action_name: Name of the action to trigger
            parameters: Additional parameters for the trigger
            
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
                "trigger_name": trigger_name,
                "trigger_type": trigger_type,
                "action_name": action_name,
                "parameters": parameters
            }
            
            logger.info(f"Creating input trigger '{trigger_name}' of type '{trigger_type}'")
            response = unreal.send_command("create_input_trigger", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Input trigger creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating input trigger: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("Enhanced input action tools registered successfully")
