"""
Editor Tools for Unreal MCP.

This module provides comprehensive tools for controlling the Unreal Editor viewport, 
actor management, level operations, and other editor functionality.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")


def validate_vector_param(param_name: str, param_value: List[float], required_length: int = 3) -> List[float]:
    """
    Validate and normalize vector parameters (location, rotation, scale).
    
    Args:
        param_name: Name of the parameter for error messages
        param_value: The parameter value to validate
        required_length: Expected length of the vector (default 3)
        
    Returns:
        Normalized list of floats
        
    Raises:
        ValueError: If parameter format is invalid
    """
    if not isinstance(param_value, list):
        raise ValueError(f"{param_name} must be a list, got {type(param_value).__name__}")
    
    if len(param_value) != required_length:
        raise ValueError(f"{param_name} must have exactly {required_length} elements, got {len(param_value)}")
    
    try:
        return [float(val) for val in param_value]
    except (ValueError, TypeError) as e:
        raise ValueError(f"{param_name} must contain only numeric values: {e}")


def validate_actor_name(name: str) -> str:
    """
    Validate actor name format.
    
    Args:
        name: Actor name to validate
        
    Returns:
        Validated actor name
        
    Raises:
        ValueError: If name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValueError("Actor name must be a non-empty string")
    
    # Remove leading/trailing whitespace
    name = name.strip()
    
    if not name:
        raise ValueError("Actor name cannot be empty or whitespace only")
    
    # Check for invalid characters (basic validation)
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\']
    for char in invalid_chars:
        if char in name:
            raise ValueError(f"Actor name cannot contain '{char}'")
    
    return name

def register_editor_tools(mcp: FastMCP):
    """Register editor tools with the MCP server."""
    
    @mcp.tool()
    def get_actors_in_level(ctx: Context) -> List[Dict[str, Any]]:
        """Get a list of all actors in the current level."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.warning("Failed to connect to Unreal Engine")
                return []
                
            response = unreal.send_command("get_actors_in_level", {})
            
            if not response:
                logger.warning("No response from Unreal Engine")
                return []
                
            # Log the complete response for debugging
            logger.info(f"Complete response from Unreal: {response}")
            
            # Check response format
            if "result" in response and "actors" in response["result"]:
                actors = response["result"]["actors"]
                logger.info(f"Found {len(actors)} actors in level")
                return actors
            elif "actors" in response:
                actors = response["actors"]
                logger.info(f"Found {len(actors)} actors in level")
                return actors
                
            logger.warning(f"Unexpected response format: {response}")
            return []
            
        except Exception as e:
            logger.error(f"Error getting actors: {e}")
            return []

    @mcp.tool()
    def find_actors_by_name(ctx: Context, pattern: str) -> List[str]:
        """Find actors by name pattern."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.warning("Failed to connect to Unreal Engine")
                return []
                
            response = unreal.send_command("find_actors_by_name", {
                "pattern": pattern
            })
            
            if not response:
                return []
                
            return response.get("actors", [])
            
        except Exception as e:
            logger.error(f"Error finding actors: {e}")
            return []
    
    @mcp.tool()
    def spawn_actor(
        ctx: Context,
        name: str,
        type: str,
        location: List[float] = [0.0, 0.0, 0.0],
        rotation: List[float] = [0.0, 0.0, 0.0]
    ) -> Dict[str, Any]:
        """Create a new actor in the current level.
        
        Args:
            ctx: The MCP context
            name: The name to give the new actor (must be unique)
            type: The type of actor to create (e.g. StaticMeshActor, PointLight)
            location: The [x, y, z] world location to spawn at
            rotation: The [pitch, yaw, roll] rotation in degrees
            
        Returns:
            Dict containing the created actor's properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            # Validate inputs
            name = validate_actor_name(name)
            location = validate_vector_param("location", location)
            rotation = validate_vector_param("rotation", rotation)
            
            if not type or not isinstance(type, str):
                return {"success": False, "message": "Actor type must be a non-empty string"}
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Prepare parameters
            params = {
                "name": name,
                "type": type.upper(),  # Make sure type is uppercase
                "location": location,
                "rotation": rotation
            }
            
            logger.info(f"Creating actor '{name}' of type '{type}' with params: {params}")
            response = unreal.send_command("spawn_actor", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            # Log the complete response for debugging
            logger.info(f"Actor creation response: {response}")
            
            # Handle error responses correctly
            if response.get("status") == "error":
                error_message = response.get("error", "Unknown error")
                logger.error(f"Error creating actor: {error_message}")
                return {"success": False, "message": error_message}
            
            return response
            
        except ValueError as e:
            error_msg = f"Validation error: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Error creating actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def delete_actor(ctx: Context, name: str) -> Dict[str, Any]:
        """Delete an actor by name.
        
        Args:
            ctx: The MCP context
            name: Name of the actor to delete
            
        Returns:
            Dict containing the deletion result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            # Validate input
            name = validate_actor_name(name)
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            logger.info(f"Deleting actor '{name}'")
            response = unreal.send_command("delete_actor", {"name": name})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Delete actor response: {response}")
            return response
            
        except ValueError as e:
            error_msg = f"Validation error: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Error deleting actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    @mcp.tool()
    def set_actor_transform(
        ctx: Context,
        name: str,
        location: List[float]  = None,
        rotation: List[float]  = None,
        scale: List[float] = None
    ) -> Dict[str, Any]:
        """Set the transform of an actor."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            params = {"name": name}
            if location is not None:
                params["location"] = location
            if rotation is not None:
                params["rotation"] = rotation
            if scale is not None:
                params["scale"] = scale
                
            response = unreal.send_command("set_actor_transform", params)
            return response or {}
            
        except Exception as e:
            logger.error(f"Error setting transform: {e}")
            return {}
    
    @mcp.tool()
    def get_actor_properties(ctx: Context, name: str) -> Dict[str, Any]:
        """Get all properties of an actor."""
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("get_actor_properties", {
                "name": name
            })
            return response or {}
            
        except Exception as e:
            logger.error(f"Error getting properties: {e}")
            return {}

    @mcp.tool()
    def set_actor_property(
        ctx: Context,
        name: str,
        property_name: str,
        property_value,
    ) -> Dict[str, Any]:
        """
        Set a property on an actor.
        
        Args:
            name: Name of the actor
            property_name: Name of the property to set
            property_value: Value to set the property to
            
        Returns:
            Dict containing response from Unreal with operation status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            response = unreal.send_command("set_actor_property", {
                "name": name,
                "property_name": property_name,
                "property_value": property_value
            })
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set actor property response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting actor property: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    # @mcp.tool() commented out because it's buggy
    def focus_viewport(
        ctx: Context,
        target: str = None,
        location: List[float] = None,
        distance: float = 1000.0,
        orientation: List[float] = None
    ) -> Dict[str, Any]:
        """
        Focus the viewport on a specific actor or location.
        
        Args:
            target: Name of the actor to focus on (if provided, location is ignored)
            location: [X, Y, Z] coordinates to focus on (used if target is None)
            distance: Distance from the target/location
            orientation: Optional [Pitch, Yaw, Roll] for the viewport camera
            
        Returns:
            Response from Unreal Engine
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
                
            params = {}
            if target:
                params["target"] = target
            elif location:
                params["location"] = location
            
            if distance:
                params["distance"] = distance
                
            if orientation:
                params["orientation"] = orientation
                
            response = unreal.send_command("focus_viewport", params)
            return response or {}
            
        except Exception as e:
            logger.error(f"Error focusing viewport: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def spawn_blueprint_actor(
        ctx: Context,
        blueprint_name: str,
        actor_name: str,
        location: List[float] = [0.0, 0.0, 0.0],
        rotation: List[float] = [0.0, 0.0, 0.0]
    ) -> Dict[str, Any]:
        """Spawn an actor from a Blueprint.
        
        Args:
            ctx: The MCP context
            blueprint_name: Name of the Blueprint to spawn from
            actor_name: Name to give the spawned actor
            location: The [x, y, z] world location to spawn at
            rotation: The [pitch, yaw, roll] rotation in degrees
            
        Returns:
            Dict containing the spawned actor's properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Ensure all parameters are properly formatted
            params = {
                "blueprint_name": blueprint_name,
                "actor_name": actor_name,
                "location": location or [0.0, 0.0, 0.0],
                "rotation": rotation or [0.0, 0.0, 0.0]
            }
            
            # Validate location and rotation formats
            for param_name in ["location", "rotation"]:
                param_value = params[param_name]
                if not isinstance(param_value, list) or len(param_value) != 3:
                    logger.error(f"Invalid {param_name} format: {param_value}. Must be a list of 3 float values.")
                    return {"success": False, "message": f"Invalid {param_name} format. Must be a list of 3 float values."}
                # Ensure all values are float
                params[param_name] = [float(val) for val in param_value]
            
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
    def focus_viewport_on_actor(
        ctx: Context,
        actor_name: str,
        distance: float = 1000.0
    ) -> Dict[str, Any]:
        """Focus the viewport camera on a specific actor.
        
        Args:
            ctx: The MCP context
            actor_name: Name of the actor to focus on
            distance: Distance from the actor to position the camera
            
        Returns:
            Dict containing the operation result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            # Validate inputs
            actor_name = validate_actor_name(actor_name)
            
            if not isinstance(distance, (int, float)) or distance <= 0:
                return {"success": False, "message": "Distance must be a positive number"}
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "target": actor_name,
                "distance": float(distance)
            }
            
            logger.info(f"Focusing viewport on actor '{actor_name}' at distance {distance}")
            response = unreal.send_command("focus_viewport", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Focus viewport response: {response}")
            return response
            
        except ValueError as e:
            error_msg = f"Validation error: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Error focusing viewport: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def focus_viewport_on_location(
        ctx: Context,
        location: List[float],
        distance: float = 1000.0,
        orientation: List[float] = None
    ) -> Dict[str, Any]:
        """Focus the viewport camera on a specific location.
        
        Args:
            ctx: The MCP context
            location: [X, Y, Z] world coordinates to focus on
            distance: Distance from the location to position the camera
            orientation: Optional [Pitch, Yaw, Roll] for the viewport camera
            
        Returns:
            Dict containing the operation result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            # Validate inputs
            location = validate_vector_param("location", location)
            
            if not isinstance(distance, (int, float)) or distance <= 0:
                return {"success": False, "message": "Distance must be a positive number"}
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "location": location,
                "distance": float(distance)
            }
            
            if orientation is not None:
                params["orientation"] = validate_vector_param("orientation", orientation)
            
            logger.info(f"Focusing viewport on location {location} at distance {distance}")
            response = unreal.send_command("focus_viewport", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Focus viewport response: {response}")
            return response
            
        except ValueError as e:
            error_msg = f"Validation error: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Error focusing viewport: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def set_viewport_view_mode(
        ctx: Context,
        view_mode: str = "lit"
    ) -> Dict[str, Any]:
        """Set the viewport view mode.
        
        Args:
            ctx: The MCP context
            view_mode: View mode to set (lit, unlit, wireframe, detail_lighting, etc.)
            
        Returns:
            Dict containing the operation result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            valid_modes = ["lit", "unlit", "wireframe", "detail_lighting", "lighting_only", 
                          "reflection_override", "collision_pa", "collision_visibility"]
            
            if view_mode not in valid_modes:
                return {"success": False, "message": f"Invalid view mode. Valid modes: {', '.join(valid_modes)}"}
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info(f"Setting viewport view mode to '{view_mode}'")
            response = unreal.send_command("set_viewport_view_mode", {"view_mode": view_mode})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Set viewport view mode response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error setting viewport view mode: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def select_actor(
        ctx: Context,
        name: str,
        add_to_selection: bool = False
    ) -> Dict[str, Any]:
        """Select an actor in the viewport.
        
        Args:
            ctx: The MCP context
            name: Name of the actor to select
            add_to_selection: Whether to add to existing selection or replace it
            
        Returns:
            Dict containing the selection result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            # Validate input
            name = validate_actor_name(name)
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "name": name,
                "add_to_selection": add_to_selection
            }
            
            logger.info(f"Selecting actor '{name}' (add_to_selection: {add_to_selection})")
            response = unreal.send_command("select_actor", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Select actor response: {response}")
            return response
            
        except ValueError as e:
            error_msg = f"Validation error: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Error selecting actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def clear_selection(ctx: Context) -> Dict[str, Any]:
        """Clear the current actor selection in the viewport.
        
        Args:
            ctx: The MCP context
            
        Returns:
            Dict containing the operation result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Clearing actor selection")
            response = unreal.send_command("clear_selection", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Clear selection response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error clearing selection: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_selected_actors(ctx: Context) -> List[str]:
        """Get a list of currently selected actors.
        
        Args:
            ctx: The MCP context
            
        Returns:
            List of selected actor names
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.warning("Failed to connect to Unreal Engine")
                return []
            
            response = unreal.send_command("get_selected_actors", {})
            
            if not response:
                logger.warning("No response from Unreal Engine")
                return []
            
            actors = response.get("actors", [])
            logger.info(f"Found {len(actors)} selected actors")
            return actors
            
        except Exception as e:
            logger.error(f"Error getting selected actors: {e}")
            return []

    @mcp.tool()
    def save_level(ctx: Context) -> Dict[str, Any]:
        """Save the current level.
        
        Args:
            ctx: The MCP context
            
        Returns:
            Dict containing the save operation result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            logger.info("Saving current level")
            response = unreal.send_command("save_level", {})
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Save level response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Error saving level: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_level_info(ctx: Context) -> Dict[str, Any]:
        """Get information about the current level.
        
        Args:
            ctx: The MCP context
            
        Returns:
            Dict containing level information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.warning("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            response = unreal.send_command("get_level_info", {})
            
            if not response:
                logger.warning("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Level info response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error getting level info: {e}")
            return {"success": False, "message": str(e)}

    @mcp.tool()
    def duplicate_actor(
        ctx: Context,
        source_name: str,
        new_name: str,
        location: List[float] = None,
        rotation: List[float] = None
    ) -> Dict[str, Any]:
        """Duplicate an existing actor.
        
        Args:
            ctx: The MCP context
            source_name: Name of the actor to duplicate
            new_name: Name for the new actor
            location: Optional [x, y, z] location for the new actor
            rotation: Optional [pitch, yaw, roll] rotation for the new actor
            
        Returns:
            Dict containing the duplication result
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            # Validate inputs
            source_name = validate_actor_name(source_name)
            new_name = validate_actor_name(new_name)
            
            if location is not None:
                location = validate_vector_param("location", location)
            if rotation is not None:
                rotation = validate_vector_param("rotation", rotation)
            
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "source_name": source_name,
                "new_name": new_name
            }
            
            if location is not None:
                params["location"] = location
            if rotation is not None:
                params["rotation"] = rotation
            
            logger.info(f"Duplicating actor '{source_name}' to '{new_name}'")
            response = unreal.send_command("duplicate_actor", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Duplicate actor response: {response}")
            return response
            
        except ValueError as e:
            error_msg = f"Validation error: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
        except Exception as e:
            error_msg = f"Error duplicating actor: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    logger.info("Editor tools registered successfully")
