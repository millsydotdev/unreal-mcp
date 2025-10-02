"""
Blueprint Tools for Unreal MCP.

This module provides comprehensive tools for creating and manipulating Blueprint assets in Unreal Engine.
It includes both basic and enhanced blueprint creation, component management, and blueprint information tools.
"""

import logging
from typing import Dict, List, Any
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_blueprint_tools(mcp: FastMCP):
    """Register Blueprint tools with the MCP server."""
    
    @mcp.tool()
    def create_blueprint(
        ctx: Context,
        name: str,
        parent_class: str
    ) -> Dict[str, Any]:
        """Create a new Blueprint class."""
        # Import inside function to avoid circular imports
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_component_to_blueprint(
        ctx: Context,
        blueprint_name: str,
        component_type: str,
        component_name: str,
        location: List[float] = [],
        rotation: List[float] = [],
        scale: List[float] = [],
        component_properties: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Add a component to a Blueprint.
        
        Args:
            blueprint_name: Name of the target Blueprint
            component_type: Type of component to add (use component class name without U prefix)
            component_name: Name for the new component
            location: [X, Y, Z] coordinates for component's position
            rotation: [Pitch, Yaw, Roll] values for component's rotation
            scale: [X, Y, Z] values for component's scale
            component_properties: Additional properties to set on the component
        
        Returns:
            Information about the added component
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            # Ensure all parameters are properly formatted
            params = {
                "blueprint_name": blueprint_name,
                "component_type": component_type,
                "component_name": component_name,
                "location": location or [0.0, 0.0, 0.0],
                "rotation": rotation or [0.0, 0.0, 0.0],
                "scale": scale or [1.0, 1.0, 1.0]
            }
            
            # Add component_properties if provided
            if component_properties and len(component_properties) > 0:
                params["component_properties"] = component_properties
            
            # Validate location, rotation, and scale formats
            for param_name in ["location", "rotation", "scale"]:
                param_value = params[param_name]
                if not isinstance(param_value, list) or len(param_value) != 3:
                    logger.error(f"Invalid {param_name} format: {param_value}. Must be a list of 3 float values.")
                    return {"success": False, "message": f"Invalid {param_name} format. Must be a list of 3 float values."}
                # Ensure all values are float
                params[param_name] = [float(val) for val in param_value]
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            logger.info(f"Adding component to blueprint with params: {params}")
            response = unreal.send_command("add_component_to_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Component addition response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding component to blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def set_static_mesh_properties(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        static_mesh: str = "/Engine/BasicShapes/Cube.Cube"
    ) -> Dict[str, Any]:
        """
        Set static mesh properties on a StaticMeshComponent.
        
        Args:
            blueprint_name: Name of the target Blueprint
            component_name: Name of the StaticMeshComponent
            static_mesh: Path to the static mesh asset (e.g., "/Engine/BasicShapes/Cube.Cube")
            
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
                "component_name": component_name,
                "static_mesh": static_mesh
            }
            
            logger.info(f"Setting static mesh properties with params: {params}")
            response = unreal.send_command("set_static_mesh_properties", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set static mesh properties response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting static mesh properties: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def set_component_property(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        property_name: str,
        property_value,
    ) -> Dict[str, Any]:
        """Set a property on a component in a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "component_name": component_name,
                "property_name": property_name,
                "property_value": property_value
            }
            
            logger.info(f"Setting component property with params: {params}")
            response = unreal.send_command("set_component_property", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set component property response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting component property: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def set_physics_properties(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        simulate_physics: bool = True,
        gravity_enabled: bool = True,
        mass: float = 1.0,
        linear_damping: float = 0.01,
        angular_damping: float = 0.0
    ) -> Dict[str, Any]:
        """Set physics properties on a component."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "component_name": component_name,
                "simulate_physics": simulate_physics,
                "gravity_enabled": gravity_enabled,
                "mass": float(mass),
                "linear_damping": float(linear_damping),
                "angular_damping": float(angular_damping)
            }
            
            logger.info(f"Setting physics properties with params: {params}")
            response = unreal.send_command("set_physics_properties", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set physics properties response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting physics properties: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def compile_blueprint(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Compile a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name
            }
            
            logger.info(f"Compiling blueprint: {blueprint_name}")
            response = unreal.send_command("compile_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Compile blueprint response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error compiling blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_blueprint_property(
        ctx: Context,
        blueprint_name: str,
        property_name: str,
        property_value
    ) -> Dict[str, Any]:
        """
        Set a property on a Blueprint class default object.
        
        Args:
            blueprint_name: Name of the target Blueprint
            property_name: Name of the property to set
            property_value: Value to set the property to
            
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
                "property_name": property_name,
                "property_value": property_value
            }
            
            logger.info(f"Setting blueprint property with params: {params}")
            response = unreal.send_command("set_blueprint_property", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set blueprint property response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting blueprint property: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    # @mcp.tool() commented out, just use set_component_property instead
    def set_pawn_properties(
        ctx: Context,
        blueprint_name: str,
        auto_possess_player: str = "",
        use_controller_rotation_yaw: bool = None,
        use_controller_rotation_pitch: bool = None,
        use_controller_rotation_roll: bool = None,
        can_be_damaged: bool = None
    ) -> Dict[str, Any]:
        """
        Set common Pawn properties on a Blueprint.
        This is a utility function that sets multiple pawn-related properties at once.
        
        Args:
            blueprint_name: Name of the target Blueprint (must be a Pawn or Character)
            auto_possess_player: Auto possess player setting (None, "Disabled", "Player0", "Player1", etc.)
            use_controller_rotation_yaw: Whether the pawn should use the controller's yaw rotation
            use_controller_rotation_pitch: Whether the pawn should use the controller's pitch rotation
            use_controller_rotation_roll: Whether the pawn should use the controller's roll rotation
            can_be_damaged: Whether the pawn can be damaged
            
        Returns:
            Response indicating success or failure with detailed results for each property
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Define the properties to set
            properties = {}
            if auto_possess_player and auto_possess_player != "":
                properties["auto_possess_player"] = auto_possess_player
            
            # Only include boolean properties if they were explicitly set
            if use_controller_rotation_yaw is not None:
                properties["bUseControllerRotationYaw"] = use_controller_rotation_yaw
            if use_controller_rotation_pitch is not None:
                properties["bUseControllerRotationPitch"] = use_controller_rotation_pitch
            if use_controller_rotation_roll is not None:
                properties["bUseControllerRotationRoll"] = use_controller_rotation_roll
            if can_be_damaged is not None:
                properties["bCanBeDamaged"] = can_be_damaged
                
            if not properties:
                logger.warning("No properties specified to set")
                return {"success": True, "message": "No properties specified to set", "results": {}}
            
            # Set each property using the generic set_blueprint_property function
            results = {}
            overall_success = True
            
            for prop_name, prop_value in properties.items():
                params = {
                    "blueprint_name": blueprint_name,
                    "property_name": prop_name,
                    "property_value": prop_value
                }
                
                logger.info(f"Setting pawn property {prop_name} to {prop_value}")
                response = unreal.send_command("set_blueprint_property", params)
                
                if not response:
                    logger.error(f"No response from Unreal Engine for property {prop_name}")
                    results[prop_name] = {"success": False, "message": "No response from Unreal Engine"}
                    overall_success = False
                    continue
                
                results[prop_name] = response
                if not response.get("success", False):
                    overall_success = False
            
            return {
                "success": overall_success,
                "message": "Pawn properties set" if overall_success else "Some pawn properties failed to set",
                "results": results
            }
            
        except Exception as e:
            error_msg = f"Error setting pawn properties: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # Enhanced Blueprint Creation Tools
    
    @mcp.tool()
    def create_actor_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "Actor"
    ) -> Dict[str, Any]:
        """Create a new Actor Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Actor Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating actor blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_component_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "ActorComponent"
    ) -> Dict[str, Any]:
        """Create a new Component Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Component Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating component blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_pawn_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "Pawn"
    ) -> Dict[str, Any]:
        """Create a new Pawn Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Pawn Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating pawn blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_character_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "Character"
    ) -> Dict[str, Any]:
        """Create a new Character Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Character Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating character blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # Enhanced Component Addition Tools
    
    @mcp.tool()
    def add_static_mesh_component(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        static_mesh: str = "/Engine/BasicShapes/Cube.Cube",
        location: List[float] = [0, 0, 0],
        rotation: List[float] = [0, 0, 0],
        scale: List[float] = [1, 1, 1]
    ) -> Dict[str, Any]:
        """Add a StaticMeshComponent to a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "component_type": "StaticMeshComponent",
                "component_name": component_name,
                "location": location,
                "rotation": rotation,
                "scale": scale,
                "component_properties": {
                    "StaticMesh": static_mesh
                }
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Adding StaticMeshComponent with params: {params}")
            response = unreal.send_command("add_component_to_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"StaticMeshComponent addition response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding StaticMeshComponent: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_skeletal_mesh_component(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        skeletal_mesh: str = "",
        location: List[float] = [0, 0, 0],
        rotation: List[float] = [0, 0, 0],
        scale: List[float] = [1, 1, 1]
    ) -> Dict[str, Any]:
        """Add a SkeletalMeshComponent to a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "component_type": "SkeletalMeshComponent",
                "component_name": component_name,
                "location": location,
                "rotation": rotation,
                "scale": scale,
                "component_properties": {
                    "SkeletalMesh": skeletal_mesh
                }
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Adding SkeletalMeshComponent with params: {params}")
            response = unreal.send_command("add_component_to_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"SkeletalMeshComponent addition response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding SkeletalMeshComponent: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_camera_component(
        ctx: Context,
        blueprint_name: str,
        component_name: str = "Camera",
        location: List[float] = [0, 0, 0],
        rotation: List[float] = [0, 0, 0],
        scale: List[float] = [1, 1, 1]
    ) -> Dict[str, Any]:
        """Add a CameraComponent to a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "component_type": "CameraComponent",
                "component_name": component_name,
                "location": location,
                "rotation": rotation,
                "scale": scale
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Adding CameraComponent with params: {params}")
            response = unreal.send_command("add_component_to_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"CameraComponent addition response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding CameraComponent: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # Blueprint Node Management Tools
    
    @mcp.tool()
    def delete_blueprint_node(
        ctx: Context,
        blueprint_name: str,
        node_id: str
    ) -> Dict[str, Any]:
        """Delete a specific node from a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "node_id": node_id
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Deleting node '{node_id}' from blueprint '{blueprint_name}'")
            response = unreal.send_command("delete_blueprint_node", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Delete node response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error deleting blueprint node: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def clear_blueprint_graph(
        ctx: Context,
        blueprint_name: str,
        graph_name: str = "EventGraph"
    ) -> Dict[str, Any]:
        """Clear all nodes from a Blueprint graph."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "graph_name": graph_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Clearing graph '{graph_name}' from blueprint '{blueprint_name}'")
            response = unreal.send_command("clear_blueprint_graph", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Clear graph response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error clearing blueprint graph: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # Blueprint Information Tools
    
    @mcp.tool()
    def get_blueprint_compilation_errors(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Get compilation errors for a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Getting compilation errors for blueprint '{blueprint_name}'")
            response = unreal.send_command("get_blueprint_compilation_errors", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get compilation errors response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting blueprint compilation errors: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_blueprint_info(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Get comprehensive information about a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Getting info for blueprint '{blueprint_name}'")
            response = unreal.send_command("get_blueprint_info", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get blueprint info response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting blueprint info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_blueprint_variables(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Get all variables in a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Getting variables for blueprint '{blueprint_name}'")
            response = unreal.send_command("get_blueprint_variables", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get variables response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting blueprint variables: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_blueprint_functions(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Get all functions in a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Getting functions for blueprint '{blueprint_name}'")
            response = unreal.send_command("get_blueprint_functions", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get functions response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting blueprint functions: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_blueprint_components(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Get all components in a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Getting components for blueprint '{blueprint_name}'")
            response = unreal.send_command("get_blueprint_components", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get components response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting blueprint components: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== BLUEPRINT TYPE CREATION TOOLS =====
    
    @mcp.tool()
    def create_actor_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "Actor"
    ) -> Dict[str, Any]:
        """Create a new Actor Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Actor Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating actor blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_component_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "ActorComponent"
    ) -> Dict[str, Any]:
        """Create a new Component Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Component Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating component blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_pawn_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "Pawn"
    ) -> Dict[str, Any]:
        """Create a new Pawn Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Pawn Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating pawn blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_character_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "Character"
    ) -> Dict[str, Any]:
        """Create a new Character Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Character Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating character blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    # ===== COMPONENT MANAGEMENT TOOLS =====
    
    @mcp.tool()
    def add_static_mesh_component(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        static_mesh: str = "/Engine/BasicShapes/Cube.Cube",
        location: List[float] = [0, 0, 0],
        rotation: List[float] = [0, 0, 0],
        scale: List[float] = [1, 1, 1]
    ) -> Dict[str, Any]:
        """Add a StaticMeshComponent to a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "component_type": "StaticMeshComponent",
                "component_name": component_name,
                "location": location,
                "rotation": rotation,
                "scale": scale,
                "component_properties": {
                    "StaticMesh": static_mesh
                }
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Adding StaticMeshComponent with params: {params}")
            response = unreal.send_command("add_component_to_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"StaticMeshComponent addition response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding StaticMeshComponent: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_skeletal_mesh_component(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        skeletal_mesh: str = "",
        location: List[float] = [0, 0, 0],
        rotation: List[float] = [0, 0, 0],
        scale: List[float] = [1, 1, 1]
    ) -> Dict[str, Any]:
        """Add a SkeletalMeshComponent to a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "component_type": "SkeletalMeshComponent",
                "component_name": component_name,
                "location": location,
                "rotation": rotation,
                "scale": scale,
                "component_properties": {
                    "SkeletalMesh": skeletal_mesh
                }
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Adding SkeletalMeshComponent with params: {params}")
            response = unreal.send_command("add_component_to_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"SkeletalMeshComponent addition response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding SkeletalMeshComponent: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_camera_component(
        ctx: Context,
        blueprint_name: str,
        component_name: str = "Camera",
        location: List[float] = [0, 0, 0],
        rotation: List[float] = [0, 0, 0],
        scale: List[float] = [1, 1, 1]
    ) -> Dict[str, Any]:
        """Add a CameraComponent to a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "component_type": "CameraComponent",
                "component_name": component_name,
                "location": location,
                "rotation": rotation,
                "scale": scale
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Adding CameraComponent with params: {params}")
            response = unreal.send_command("add_component_to_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"CameraComponent addition response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding CameraComponent: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def add_collision_component(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        collision_type: str = "Box",
        location: List[float] = [0, 0, 0],
        rotation: List[float] = [0, 0, 0],
        scale: List[float] = [1, 1, 1]
    ) -> Dict[str, Any]:
        """Add a collision component to a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            component_type = f"{collision_type}Component"
            params = {
                "blueprint_name": blueprint_name,
                "component_type": component_type,
                "component_name": component_name,
                "location": location,
                "rotation": rotation,
                "scale": scale
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Adding {component_type} with params: {params}")
            response = unreal.send_command("add_component_to_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"{component_type} addition response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error adding collision component: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def remove_component_from_blueprint(
        ctx: Context,
        blueprint_name: str,
        component_name: str
    ) -> Dict[str, Any]:
        """Remove a component from a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "component_name": component_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Removing component '{component_name}' from blueprint '{blueprint_name}'")
            response = unreal.send_command("remove_component_from_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Component removal response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error removing component: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    # ===== NODE MANAGEMENT TOOLS =====
    
    @mcp.tool()
    def delete_blueprint_node(
        ctx: Context,
        blueprint_name: str,
        node_id: str
    ) -> Dict[str, Any]:
        """Delete a specific node from a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "node_id": node_id
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Deleting node '{node_id}' from blueprint '{blueprint_name}'")
            response = unreal.send_command("delete_blueprint_node", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Delete node response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error deleting blueprint node: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def clear_blueprint_graph(
        ctx: Context,
        blueprint_name: str,
        graph_name: str = "EventGraph"
    ) -> Dict[str, Any]:
        """Clear all nodes from a Blueprint graph."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name,
                "graph_name": graph_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Clearing graph '{graph_name}' from blueprint '{blueprint_name}'")
            response = unreal.send_command("clear_blueprint_graph", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Clear graph response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error clearing blueprint graph: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== BLUEPRINT INSPECTION TOOLS =====
    
    @mcp.tool()
    def get_blueprint_compilation_errors(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Get compilation errors for a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Getting compilation errors for blueprint '{blueprint_name}'")
            response = unreal.send_command("get_blueprint_compilation_errors", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get compilation errors response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting blueprint compilation errors: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def validate_blueprint(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Validate a Blueprint for errors and issues."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Validating blueprint '{blueprint_name}'")
            response = unreal.send_command("validate_blueprint", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Validate blueprint response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error validating blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_blueprint_info(
        ctx: Context,
        blueprint_name: str
    ) -> Dict[str, Any]:
        """Get comprehensive information about a Blueprint."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            params = {
                "blueprint_name": blueprint_name
            }
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Getting info for blueprint '{blueprint_name}'")
            response = unreal.send_command("get_blueprint_info", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Get blueprint info response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error getting blueprint info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    # ===== ADDITIONAL BLUEPRINT TYPES =====
    
    @mcp.tool()
    def create_widget_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "UserWidget"
    ) -> Dict[str, Any]:
        """Create a new Widget Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Widget Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating widget blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_interface_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "Interface"
    ) -> Dict[str, Any]:
        """Create a new Interface Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Interface Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating interface blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_macro_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "BlueprintMacroLibrary"
    ) -> Dict[str, Any]:
        """Create a new Macro Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Macro Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating macro blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_animation_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "AnimInstance"
    ) -> Dict[str, Any]:
        """Create a new Animation Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Animation Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating animation blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_gameplay_ability_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "GameplayAbility"
    ) -> Dict[str, Any]:
        """Create a new Gameplay Ability Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Gameplay Ability Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating gameplay ability blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_controller_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "PlayerController"
    ) -> Dict[str, Any]:
        """Create a new Controller Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Controller Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating controller blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_game_mode_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "GameModeBase"
    ) -> Dict[str, Any]:
        """Create a new Game Mode Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Game Mode Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating game mode blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_hud_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "HUD"
    ) -> Dict[str, Any]:
        """Create a new HUD Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"HUD Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating HUD blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_game_state_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "GameStateBase"
    ) -> Dict[str, Any]:
        """Create a new Game State Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Game State Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating game state blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def create_player_state_blueprint(
        ctx: Context,
        name: str,
        parent_class: str = "PlayerState"
    ) -> Dict[str, Any]:
        """Create a new Player State Blueprint class."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("create_blueprint", {
                "name": name,
                "parent_class": parent_class
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Player State Blueprint creation response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error creating player state blueprint: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    # ===== BLUEPRINT SPAWNING TOOLS =====
    
    @mcp.tool()
    def spawn_blueprint_actor(
        ctx: Context,
        blueprint_name: str,
        actor_name: str,
        location: List[float] = [0, 0, 0],
        rotation: List[float] = [0, 0, 0],
        scale: List[float] = [1, 1, 1]
    ) -> Dict[str, Any]:
        """Spawn a Blueprint actor in the level."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "blueprint_name": blueprint_name,
                "actor_name": actor_name,
                "location": location,
                "rotation": rotation,
                "scale": scale
            }
            
            logger.info(f"Spawning blueprint actor with params: {params}")
            response = unreal.send_command("spawn_blueprint_actor", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Spawn blueprint actor response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error spawning blueprint actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def spawn_all_blueprint_types(
        ctx: Context,
        base_name: str = "TestBlueprint",
        location: List[float] = [0, 0, 0]
    ) -> Dict[str, Any]:
        """Create and spawn all different types of blueprints for testing."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Define all blueprint types to create
            blueprint_types = [
                ("Actor", "Actor"),
                ("Pawn", "Pawn"),
                ("Character", "Character"),
                ("Component", "ActorComponent"),
                ("Widget", "UserWidget"),
                ("Interface", "Interface"),
                ("Macro", "BlueprintMacroLibrary"),
                ("Animation", "AnimInstance"),
                ("GameplayAbility", "GameplayAbility"),
                ("Controller", "PlayerController"),
                ("GameMode", "GameModeBase"),
                ("HUD", "HUD"),
                ("GameState", "GameStateBase"),
                ("PlayerState", "PlayerState")
            ]
            
            results = {}
            spawn_location = location.copy()
            
            for blueprint_type, parent_class in blueprint_types:
                blueprint_name = f"{base_name}_{blueprint_type}"
                actor_name = f"Spawned_{blueprint_name}"
                
                # Create the blueprint
                create_response = unreal.send_command("create_blueprint", {
                    "name": blueprint_name,
                    "parent_class": parent_class
                })
                
                if create_response and create_response.get("success", False):
                    # Only spawn actors that can be placed in the level
                    if blueprint_type in ["Actor", "Pawn", "Character"]:
                        spawn_response = unreal.send_command("spawn_blueprint_actor", {
                            "blueprint_name": blueprint_name,
                            "actor_name": actor_name,
                            "location": spawn_location,
                            "rotation": [0, 0, 0],
                            "scale": [1, 1, 1]
                        })
                        results[blueprint_type] = {
                            "blueprint_created": True,
                            "actor_spawned": spawn_response.get("success", False) if spawn_response else False,
                            "spawn_response": spawn_response
                        }
                        # Move spawn location for next actor
                        spawn_location[0] += 200
                    else:
                        results[blueprint_type] = {
                            "blueprint_created": True,
                            "actor_spawned": False,
                            "reason": f"{blueprint_type} blueprints cannot be spawned as actors"
                        }
                else:
                    results[blueprint_type] = {
                        "blueprint_created": False,
                        "actor_spawned": False,
                        "error": create_response.get("message", "Unknown error") if create_response else "No response"
                    }
            
            return {
                "success": True,
                "message": f"Created and spawned {len(blueprint_types)} different blueprint types",
                "results": results
            }
            
        except Exception as e:
            error_msg = f"Error creating and spawning all blueprint types: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def get_available_blueprint_types(
        ctx: Context
    ) -> Dict[str, Any]:
        """Get a list of all available blueprint types and their parent classes."""
        return {
            "success": True,
            "blueprint_types": [
                {
                    "type": "Actor",
                    "parent_class": "Actor",
                    "description": "Basic actor that can be placed in the level",
                    "can_spawn": True
                },
                {
                    "type": "Pawn",
                    "parent_class": "Pawn",
                    "description": "Actor that can be possessed by a controller",
                    "can_spawn": True
                },
                {
                    "type": "Character",
                    "parent_class": "Character",
                    "description": "Pawn with built-in movement capabilities",
                    "can_spawn": True
                },
                {
                    "type": "Component",
                    "parent_class": "ActorComponent",
                    "description": "Reusable component that can be added to actors",
                    "can_spawn": False
                },
                {
                    "type": "Widget",
                    "parent_class": "UserWidget",
                    "description": "UI widget for creating user interfaces",
                    "can_spawn": False
                },
                {
                    "type": "Interface",
                    "parent_class": "Interface",
                    "description": "Blueprint interface for defining contracts",
                    "can_spawn": False
                },
                {
                    "type": "Macro",
                    "parent_class": "BlueprintMacroLibrary",
                    "description": "Macro library for reusable blueprint functions",
                    "can_spawn": False
                },
                {
                    "type": "Animation",
                    "parent_class": "AnimInstance",
                    "description": "Animation blueprint for character animations",
                    "can_spawn": False
                },
                {
                    "type": "GameplayAbility",
                    "parent_class": "GameplayAbility",
                    "description": "Gameplay ability blueprint (requires GameplayAbilities plugin)",
                    "can_spawn": False
                },
                {
                    "type": "Controller",
                    "parent_class": "PlayerController",
                    "description": "Player controller blueprint",
                    "can_spawn": False
                },
                {
                    "type": "GameMode",
                    "parent_class": "GameModeBase",
                    "description": "Game mode blueprint",
                    "can_spawn": False
                },
                {
                    "type": "HUD",
                    "parent_class": "HUD",
                    "description": "HUD blueprint for rendering game UI",
                    "can_spawn": False
                },
                {
                    "type": "GameState",
                    "parent_class": "GameStateBase",
                    "description": "Game state blueprint",
                    "can_spawn": False
                },
                {
                    "type": "PlayerState",
                    "parent_class": "PlayerState",
                    "description": "Player state blueprint",
                    "can_spawn": False
                }
            ]
        }

    logger.info("Enhanced Blueprint tools registered successfully") 