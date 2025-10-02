"""
Animation Blueprint Tools for Unreal MCP.

This module provides comprehensive tools for creating and manipulating Animation Blueprint assets in Unreal Engine.
It includes animation blueprint creation, state machine management, blend space configuration, and animation graph node management.

Features:
- Animation Blueprint creation and configuration
- Animation State Machine management
- Blend Space and Blend Node tools
- Animation Graph node creation and connection
- Animation Blueprint variable management
- Animation montage and sequence integration
- Animation blueprint compilation and validation
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_animation_blueprint_tools(mcp: FastMCP):
    """Register Animation Blueprint tools with the MCP server."""
    
    # ===== ANIMATION BLUEPRINT CREATION TOOLS =====
    
    @mcp.tool()
    def create_animation_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "AnimInstance",
        target_skeleton: str = "",
        path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
        """
        Create a new Animation Blueprint class.
        
        Args:
            name: Name of the Animation Blueprint
            parent_class: Parent class (default: AnimInstance)
            target_skeleton: Target skeleton asset path (optional)
            path: Content browser path where to create the blueprint
            
        Returns:
            Response indicating success or failure with blueprint details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "name": name,
                "parent_class": parent_class,
                "path": path
            }
            
            if target_skeleton:
                params["target_skeleton"] = target_skeleton
            
            logger.info(f"Creating Animation Blueprint '{name}' with params: {params}")
            response = unreal.send_command("create_animation_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Animation Blueprint creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating animation blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_animation_blueprint_with_skeleton(
        ctx: Context,
        name: str,
        skeleton_path: str,
        parent_class: str = "AnimInstance",
        path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
        """
        Create an Animation Blueprint with a specific skeleton target.
        
        Args:
            name: Name of the Animation Blueprint
            skeleton_path: Path to the skeleton asset (e.g., "/Game/Characters/Mannequin/UE4_Mannequin_Skeleton")
            parent_class: Parent class (default: AnimInstance)
            path: Content browser path where to create the blueprint
            
        Returns:
            Response indicating success or failure with blueprint details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "name": name,
                "parent_class": parent_class,
                "target_skeleton": skeleton_path,
                "path": path
            }
            
            logger.info(f"Creating Animation Blueprint '{name}' with skeleton '{skeleton_path}'")
            response = unreal.send_command("create_animation_blueprint_with_skeleton", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Animation Blueprint with skeleton creation response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating animation blueprint with skeleton: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ANIMATION BLUEPRINT CONFIGURATION TOOLS =====
    
    @mcp.tool()
    def set_animation_blueprint_target_skeleton(
        ctx: Context,
        blueprint_name: str,
        skeleton_path: str
    ) -> Dict[str, Any]:
        """
        Set the target skeleton for an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            skeleton_path: Path to the skeleton asset
            
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
                "blueprint_name": blueprint_name,
                "skeleton_path": skeleton_path
            }
            
            logger.info(f"Setting target skeleton for Animation Blueprint '{blueprint_name}' to '{skeleton_path}'")
            response = unreal.send_command("set_animation_blueprint_target_skeleton", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set target skeleton response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting animation blueprint target skeleton: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_animation_blueprint_info(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """
        Get comprehensive information about an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            
        Returns:
            Dict containing animation blueprint information including target skeleton, graphs, and variables
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name
            }
            
            logger.info(f"Getting Animation Blueprint info for '{blueprint_name}'")
            response = unreal.send_command("get_animation_blueprint_info", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get Animation Blueprint info response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting animation blueprint info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ANIMATION STATE MACHINE TOOLS =====
    
    @mcp.tool()
    def create_animation_state_machine(
        ctx: Context,
        blueprint_name: str,
        state_machine_name: str,
        graph_name: str = "AnimGraph"
    ) -> Dict[str, Any]:
        """
        Create an Animation State Machine in an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            state_machine_name: Name for the state machine
            graph_name: Name of the graph to add the state machine to (default: AnimGraph)
            
        Returns:
            Response indicating success or failure with state machine details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "state_machine_name": state_machine_name,
                "graph_name": graph_name
            }
            
            logger.info(f"Creating Animation State Machine '{state_machine_name}' in '{blueprint_name}'")
            response = unreal.send_command("create_animation_state_machine", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Create Animation State Machine response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating animation state machine: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_animation_state(
        ctx: Context,
        blueprint_name: str,
        state_machine_name: str,
        state_name: str,
        animation_sequence: str = "",
        state_type: str = "AnimationState"
    ) -> Dict[str, Any]:
        """
        Add a state to an Animation State Machine.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            state_machine_name: Name of the state machine
            state_name: Name for the new state
            animation_sequence: Path to animation sequence asset (optional)
            state_type: Type of state (AnimationState, BlendSpaceState, etc.)
            
        Returns:
            Response indicating success or failure with state details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "state_machine_name": state_machine_name,
                "state_name": state_name,
                "state_type": state_type
            }
            
            if animation_sequence:
                params["animation_sequence"] = animation_sequence
            
            logger.info(f"Adding Animation State '{state_name}' to state machine '{state_machine_name}'")
            response = unreal.send_command("add_animation_state", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Animation State response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding animation state: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def connect_animation_states(
        ctx: Context,
        blueprint_name: str,
        state_machine_name: str,
        from_state: str,
        to_state: str,
        transition_rule: str = "Always"
    ) -> Dict[str, Any]:
        """
        Connect two states in an Animation State Machine with a transition.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            state_machine_name: Name of the state machine
            from_state: Name of the source state
            to_state: Name of the target state
            transition_rule: Rule for the transition (Always, Custom, etc.)
            
        Returns:
            Response indicating success or failure with transition details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "state_machine_name": state_machine_name,
                "from_state": from_state,
                "to_state": to_state,
                "transition_rule": transition_rule
            }
            
            logger.info(f"Connecting states '{from_state}' to '{to_state}' in state machine '{state_machine_name}'")
            response = unreal.send_command("connect_animation_states", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Connect Animation States response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error connecting animation states: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def set_animation_state_machine_entry_state(
        ctx: Context,
        blueprint_name: str,
        state_machine_name: str,
        entry_state: str
    ) -> Dict[str, Any]:
        """
        Set the entry state for an Animation State Machine.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            state_machine_name: Name of the state machine
            entry_state: Name of the state to set as entry
            
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
                "blueprint_name": blueprint_name,
                "state_machine_name": state_machine_name,
                "entry_state": entry_state
            }
            
            logger.info(f"Setting entry state '{entry_state}' for state machine '{state_machine_name}'")
            response = unreal.send_command("set_animation_state_machine_entry_state", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set entry state response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting animation state machine entry state: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== BLEND SPACE AND BLEND NODE TOOLS =====
    
    @mcp.tool()
    def create_animation_blend_space(
        ctx: Context,
        blueprint_name: str,
        blend_space_name: str,
        blend_space_type: str = "1D",
        skeleton_path: str = ""
    ) -> Dict[str, Any]:
        """
        Create a Blend Space in an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            blend_space_name: Name for the blend space
            blend_space_type: Type of blend space (1D, 2D, etc.)
            skeleton_path: Path to skeleton asset (optional, uses blueprint's target skeleton if not provided)
            
        Returns:
            Response indicating success or failure with blend space details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "blend_space_name": blend_space_name,
                "blend_space_type": blend_space_type
            }
            
            if skeleton_path:
                params["skeleton_path"] = skeleton_path
            
            logger.info(f"Creating Animation Blend Space '{blend_space_name}' in '{blueprint_name}'")
            response = unreal.send_command("create_animation_blend_space", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Create Animation Blend Space response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating animation blend space: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_animation_to_blend_space(
        ctx: Context,
        blueprint_name: str,
        blend_space_name: str,
        animation_sequence: str,
        blend_position: List[float] = [0.0, 0.0]
    ) -> Dict[str, Any]:
        """
        Add an animation sequence to a Blend Space.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            blend_space_name: Name of the blend space
            animation_sequence: Path to the animation sequence asset
            blend_position: Position in blend space [X, Y] coordinates
            
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
                "blueprint_name": blueprint_name,
                "blend_space_name": blend_space_name,
                "animation_sequence": animation_sequence,
                "blend_position": blend_position
            }
            
            logger.info(f"Adding animation '{animation_sequence}' to blend space '{blend_space_name}' at position {blend_position}")
            response = unreal.send_command("add_animation_to_blend_space", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add animation to blend space response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding animation to blend space: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_animation_blend_node(
        ctx: Context,
        blueprint_name: str,
        node_name: str,
        blend_type: str = "BlendPoses",
        input_count: int = 2
    ) -> Dict[str, Any]:
        """
        Create a Blend Node in an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            node_name: Name for the blend node
            blend_type: Type of blend node (BlendPoses, BlendPosesByBool, etc.)
            input_count: Number of input poses for blending
            
        Returns:
            Response indicating success or failure with node details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "node_name": node_name,
                "blend_type": blend_type,
                "input_count": input_count
            }
            
            logger.info(f"Creating Animation Blend Node '{node_name}' of type '{blend_type}' in '{blueprint_name}'")
            response = unreal.send_command("create_animation_blend_node", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Create Animation Blend Node response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating animation blend node: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ANIMATION GRAPH NODE TOOLS =====
    
    @mcp.tool()
    def add_animation_sequence_node(
        ctx: Context,
        blueprint_name: str,
        node_name: str,
        animation_sequence: str,
        graph_name: str = "AnimGraph"
    ) -> Dict[str, Any]:
        """
        Add an Animation Sequence node to an Animation Blueprint graph.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            node_name: Name for the sequence node
            animation_sequence: Path to the animation sequence asset
            graph_name: Name of the graph to add the node to (default: AnimGraph)
            
        Returns:
            Response indicating success or failure with node details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "node_name": node_name,
                "animation_sequence": animation_sequence,
                "graph_name": graph_name
            }
            
            logger.info(f"Adding Animation Sequence node '{node_name}' with sequence '{animation_sequence}' to '{blueprint_name}'")
            response = unreal.send_command("add_animation_sequence_node", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Animation Sequence node response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding animation sequence node: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_animation_output_node(
        ctx: Context,
        blueprint_name: str,
        node_name: str = "OutputPose",
        graph_name: str = "AnimGraph"
    ) -> Dict[str, Any]:
        """
        Add an Animation Output node to an Animation Blueprint graph.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            node_name: Name for the output node (default: OutputPose)
            graph_name: Name of the graph to add the node to (default: AnimGraph)
            
        Returns:
            Response indicating success or failure with node details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "node_name": node_name,
                "graph_name": graph_name
            }
            
            logger.info(f"Adding Animation Output node '{node_name}' to '{blueprint_name}'")
            response = unreal.send_command("add_animation_output_node", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Animation Output node response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding animation output node: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def connect_animation_nodes(
        ctx: Context,
        blueprint_name: str,
        source_node: str,
        target_node: str,
        source_pin: str = "Pose",
        target_pin: str = "Pose",
        graph_name: str = "AnimGraph"
    ) -> Dict[str, Any]:
        """
        Connect two nodes in an Animation Blueprint graph.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            source_node: Name of the source node
            target_node: Name of the target node
            source_pin: Name of the source pin (default: Pose)
            target_pin: Name of the target pin (default: Pose)
            graph_name: Name of the graph containing the nodes (default: AnimGraph)
            
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
                "blueprint_name": blueprint_name,
                "source_node": source_node,
                "target_node": target_node,
                "source_pin": source_pin,
                "target_pin": target_pin,
                "graph_name": graph_name
            }
            
            logger.info(f"Connecting animation nodes '{source_node}' to '{target_node}' in '{blueprint_name}'")
            response = unreal.send_command("connect_animation_nodes", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Connect animation nodes response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error connecting animation nodes: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ANIMATION BLUEPRINT VARIABLE TOOLS =====
    
    @mcp.tool()
    def add_animation_blueprint_variable(
        ctx: Context,
        blueprint_name: str,
        variable_name: str,
        variable_type: str = "Float",
        default_value: Any = None,
        is_exposed: bool = False
    ) -> Dict[str, Any]:
        """
        Add a variable to an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            variable_name: Name of the variable
            variable_type: Type of the variable (Float, Bool, Integer, Vector, etc.)
            default_value: Default value for the variable
            is_exposed: Whether to expose the variable to the editor
            
        Returns:
            Response indicating success or failure with variable details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "variable_name": variable_name,
                "variable_type": variable_type,
                "is_exposed": is_exposed
            }
            
            if default_value is not None:
                params["default_value"] = default_value
            
            logger.info(f"Adding variable '{variable_name}' of type '{variable_type}' to Animation Blueprint '{blueprint_name}'")
            response = unreal.send_command("add_animation_blueprint_variable", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Animation Blueprint variable response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding animation blueprint variable: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_animation_blueprint_variables(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """
        Get all variables in an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            
        Returns:
            Dict containing all variables with their types and values
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name
            }
            
            logger.info(f"Getting variables for Animation Blueprint '{blueprint_name}'")
            response = unreal.send_command("get_animation_blueprint_variables", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get Animation Blueprint variables response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting animation blueprint variables: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ANIMATION MONTAGE AND SEQUENCE TOOLS =====
    
    @mcp.tool()
    def add_animation_montage_node(
        ctx: Context,
        blueprint_name: str,
        node_name: str,
        montage_asset: str,
        graph_name: str = "AnimGraph"
    ) -> Dict[str, Any]:
        """
        Add an Animation Montage node to an Animation Blueprint graph.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            node_name: Name for the montage node
            montage_asset: Path to the animation montage asset
            graph_name: Name of the graph to add the node to (default: AnimGraph)
            
        Returns:
            Response indicating success or failure with node details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "node_name": node_name,
                "montage_asset": montage_asset,
                "graph_name": graph_name
            }
            
            logger.info(f"Adding Animation Montage node '{node_name}' with montage '{montage_asset}' to '{blueprint_name}'")
            response = unreal.send_command("add_animation_montage_node", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Add Animation Montage node response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding animation montage node: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_animation_montage(
        ctx: Context,
        montage_name: str,
        skeleton_path: str,
        animation_sequence: str = "",
        path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
        """
        Create an Animation Montage asset.
        
        Args:
            montage_name: Name of the montage
            skeleton_path: Path to the skeleton asset
            animation_sequence: Path to the animation sequence to add (optional)
            path: Content browser path where to create the montage
            
        Returns:
            Response indicating success or failure with montage details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "montage_name": montage_name,
                "skeleton_path": skeleton_path,
                "path": path
            }
            
            if animation_sequence:
                params["animation_sequence"] = animation_sequence
            
            logger.info(f"Creating Animation Montage '{montage_name}' with skeleton '{skeleton_path}'")
            response = unreal.send_command("create_animation_montage", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Create Animation Montage response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating animation montage: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ANIMATION BLUEPRINT COMPILATION AND VALIDATION TOOLS =====
    
    @mcp.tool()
    def compile_animation_blueprint(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """
        Compile an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            
        Returns:
            Response indicating success or failure with compilation details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name
            }
            
            logger.info(f"Compiling Animation Blueprint '{blueprint_name}'")
            response = unreal.send_command("compile_animation_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Compile Animation Blueprint response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error compiling animation blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def validate_animation_blueprint(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """
        Validate an Animation Blueprint for errors and issues.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            
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
                "blueprint_name": blueprint_name
            }
            
            logger.info(f"Validating Animation Blueprint '{blueprint_name}'")
            response = unreal.send_command("validate_animation_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Validate Animation Blueprint response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error validating animation blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_animation_blueprint_compilation_errors(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """
        Get compilation errors for an Animation Blueprint.
        
        Args:
            blueprint_name: Name of the Animation Blueprint
            
        Returns:
            Dict containing compilation errors and warnings
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name
            }
            
            logger.info(f"Getting compilation errors for Animation Blueprint '{blueprint_name}'")
            response = unreal.send_command("get_animation_blueprint_compilation_errors", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get Animation Blueprint compilation errors response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting animation blueprint compilation errors: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== ANIMATION BLUEPRINT UTILITY TOOLS =====
    
    @mcp.tool()
    def get_available_animation_blueprint_types(
        ctx: Context
    ) -> Dict[str, Any]:
        """
        Get a list of all available Animation Blueprint types and their capabilities.
        
        Returns:
            Dict containing available animation blueprint types and their descriptions
        """
        return {
            "success": True,
            "animation_blueprint_types": [
                {
                    "type": "AnimInstance",
                    "parent_class": "AnimInstance",
                    "description": "Standard Animation Blueprint for character animations",
                    "capabilities": ["State Machines", "Blend Spaces", "Animation Sequences", "Variables", "Functions"]
                },
                {
                    "type": "AnimLayerInterface",
                    "parent_class": "AnimLayerInterface",
                    "description": "Animation Layer Interface for layered animation systems",
                    "capabilities": ["Layer Management", "Animation Layering", "Blend Layers"]
                },
                {
                    "type": "AnimNotifyState",
                    "parent_class": "AnimNotifyState",
                    "description": "Animation Notify State for custom animation events",
                    "capabilities": ["Animation Events", "Custom Notifications", "Timeline Events"]
                }
            ],
            "animation_node_types": [
                {
                    "type": "AnimationSequence",
                    "description": "Plays a single animation sequence",
                    "inputs": ["None"],
                    "outputs": ["Pose"]
                },
                {
                    "type": "StateMachine",
                    "description": "Animation state machine for complex animation logic",
                    "inputs": ["Entry"],
                    "outputs": ["Pose"]
                },
                {
                    "type": "BlendSpace",
                    "description": "Blends between multiple animations based on parameters",
                    "inputs": ["Blend Parameters"],
                    "outputs": ["Pose"]
                },
                {
                    "type": "BlendPoses",
                    "description": "Blends between multiple pose inputs",
                    "inputs": ["Pose Array", "Alpha"],
                    "outputs": ["Pose"]
                },
                {
                    "type": "OutputPose",
                    "description": "Final output node for animation pose",
                    "inputs": ["Pose"],
                    "outputs": ["None"]
                }
            ],
            "animation_variable_types": [
                {
                    "type": "Float",
                    "description": "Floating point number for blend weights and parameters",
                    "default_value": 0.0
                },
                {
                    "type": "Bool",
                    "description": "Boolean value for animation conditions",
                    "default_value": False
                },
                {
                    "type": "Integer",
                    "description": "Integer value for animation indices and counters",
                    "default_value": 0
                },
                {
                    "type": "Vector",
                    "description": "3D vector for position and direction data",
                    "default_value": [0.0, 0.0, 0.0]
                },
                {
                    "type": "Rotator",
                    "description": "Rotation data for orientation",
                    "default_value": [0.0, 0.0, 0.0]
                }
            ]
        }
    
    @mcp.tool()
    def create_complete_animation_blueprint(
        ctx: Context,
        name: str,
        skeleton_path: str,
        include_state_machine: bool = True,
        include_blend_space: bool = True,
        include_basic_animations: bool = True,
        path: str = "/Game/Animations"
    ) -> Dict[str, Any]:
        """
        Create a complete Animation Blueprint with common setup.
        
        Args:
            name: Name of the Animation Blueprint
            skeleton_path: Path to the skeleton asset
            include_state_machine: Whether to create a basic state machine
            include_blend_space: Whether to create a basic blend space
            include_basic_animations: Whether to add basic animation nodes
            path: Content browser path where to create the blueprint
            
        Returns:
            Response indicating success or failure with complete setup details
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "name": name,
                "skeleton_path": skeleton_path,
                "include_state_machine": include_state_machine,
                "include_blend_space": include_blend_space,
                "include_basic_animations": include_basic_animations,
                "path": path
            }
            
            logger.info(f"Creating complete Animation Blueprint '{name}' with skeleton '{skeleton_path}'")
            response = unreal.send_command("create_complete_animation_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Create complete Animation Blueprint response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error creating complete animation blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    logger.info("Animation Blueprint tools registered successfully")
