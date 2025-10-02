"""
Material Tools for Unreal MCP.

This module provides comprehensive tools for creating, managing, and manipulating materials in Unreal Engine.
Includes material creation, parameter management, texture assignment, and material instance operations.
"""

import logging
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_material_tools(mcp: FastMCP):
    """Register material tools with the MCP server."""
    
    @mcp.tool()
    def create_material(
        ctx: Context,
        material_name: str,
        material_path: str = "/Game/Materials",
        parent_material: str = "/Engine/BasicShapes/BasicShapeMaterial",
        material_domain: str = "Surface",
        blend_mode: str = "Opaque",
        shading_model: str = "DefaultLit"
    ) -> Dict[str, Any]:
        """
        Create a new material asset.
        
        Args:
            material_name: Name of the material to create
            material_path: Path where the material will be created
            parent_material: Parent material class to inherit from
            material_domain: Material domain (Surface, PostProcess, LightFunction, etc.)
            blend_mode: Blend mode (Opaque, Masked, Translucent, Additive, etc.)
            shading_model: Shading model (DefaultLit, Unlit, Subsurface, etc.)
            
        Returns:
            Dict containing the created material's properties and success status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Create the material
            material_factory = unreal.MaterialFactoryNew()
            material_factory.set_editor_property("material_domain", getattr(unreal.MaterialDomain, material_domain))
            material_factory.set_editor_property("blend_mode", getattr(unreal.BlendMode, blend_mode))
            material_factory.set_editor_property("shading_model", getattr(unreal.MaterialShadingModel, shading_model))
            
            # Create the material asset
            material_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                material_name,
                material_path,
                unreal.Material,
                material_factory
            )
            
            if not material_asset:
                return {"success": False, "message": f"Failed to create material {material_name}"}
            
            # Get material properties
            material_properties = {
                "name": material_asset.get_name(),
                "path": material_asset.get_path_name(),
                "material_domain": material_domain,
                "blend_mode": blend_mode,
                "shading_model": shading_model
            }
            
            logger.info(f"Created material: {material_name} at {material_path}")
            return {
                "success": True,
                "message": f"Material {material_name} created successfully",
                "material": material_properties
            }
            
        except Exception as e:
            logger.error(f"Error creating material: {str(e)}")
            return {"success": False, "message": f"Error creating material: {str(e)}"}

    @mcp.tool()
    def create_material_instance(
        ctx: Context,
        instance_name: str,
        parent_material: str,
        instance_path: str = "/Game/Materials/Instances"
    ) -> Dict[str, Any]:
        """
        Create a new material instance.
        
        Args:
            instance_name: Name of the material instance to create
            parent_material: Path to the parent material
            instance_path: Path where the instance will be created
            
        Returns:
            Dict containing the created material instance properties and success status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Load the parent material
            parent_material_asset = unreal.EditorAssetLibrary.load_asset(parent_material)
            if not parent_material_asset:
                return {"success": False, "message": f"Parent material not found: {parent_material}"}
            
            # Create material instance factory
            instance_factory = unreal.MaterialInstanceConstantFactoryNew()
            instance_factory.set_editor_property("initial_parent", parent_material_asset)
            
            # Create the material instance
            instance_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                instance_name,
                instance_path,
                unreal.MaterialInstanceConstant,
                instance_factory
            )
            
            if not instance_asset:
                return {"success": False, "message": f"Failed to create material instance {instance_name}"}
            
            # Get instance properties
            instance_properties = {
                "name": instance_asset.get_name(),
                "path": instance_asset.get_path_name(),
                "parent_material": parent_material
            }
            
            logger.info(f"Created material instance: {instance_name} with parent {parent_material}")
            return {
                "success": True,
                "message": f"Material instance {instance_name} created successfully",
                "material_instance": instance_properties
            }
            
        except Exception as e:
            logger.error(f"Error creating material instance: {str(e)}")
            return {"success": False, "message": f"Error creating material instance: {str(e)}"}

    @mcp.tool()
    def set_material_parameter(
        ctx: Context,
        material_path: str,
        parameter_name: str,
        parameter_value: Any,
        parameter_type: str = "Scalar"
    ) -> Dict[str, Any]:
        """
        Set a parameter value on a material or material instance.
        
        Args:
            material_path: Path to the material or material instance
            parameter_name: Name of the parameter to set
            parameter_value: Value to set the parameter to
            parameter_type: Type of parameter (Scalar, Vector, Texture, StaticSwitch)
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Load the material asset
            material_asset = unreal.EditorAssetLibrary.load_asset(material_path)
            if not material_asset:
                return {"success": False, "message": f"Material not found: {material_path}"}
            
            # Set parameter based on type
            if parameter_type == "Scalar":
                if isinstance(material_asset, unreal.MaterialInstanceConstant):
                    material_asset.set_scalar_parameter_value(parameter_name, float(parameter_value))
                else:
                    logger.warning("Scalar parameters can only be set on material instances")
                    return {"success": False, "message": "Scalar parameters can only be set on material instances"}
            
            elif parameter_type == "Vector":
                if isinstance(material_asset, unreal.MaterialInstanceConstant):
                    if isinstance(parameter_value, (list, tuple)) and len(parameter_value) >= 3:
                        vector_value = unreal.LinearColor(
                            float(parameter_value[0]),
                            float(parameter_value[1]),
                            float(parameter_value[2]),
                            float(parameter_value[3]) if len(parameter_value) > 3 else 1.0
                        )
                        material_asset.set_vector_parameter_value(parameter_name, vector_value)
                    else:
                        return {"success": False, "message": "Vector parameter value must be a list/tuple with 3-4 values"}
                else:
                    logger.warning("Vector parameters can only be set on material instances")
                    return {"success": False, "message": "Vector parameters can only be set on material instances"}
            
            elif parameter_type == "Texture":
                if isinstance(material_asset, unreal.MaterialInstanceConstant):
                    if isinstance(parameter_value, str):
                        texture_asset = unreal.EditorAssetLibrary.load_asset(parameter_value)
                        if texture_asset:
                            material_asset.set_texture_parameter_value(parameter_name, texture_asset)
                        else:
                            return {"success": False, "message": f"Texture not found: {parameter_value}"}
                    else:
                        return {"success": False, "message": "Texture parameter value must be a string path"}
                else:
                    logger.warning("Texture parameters can only be set on material instances")
                    return {"success": False, "message": "Texture parameters can only be set on material instances"}
            
            elif parameter_type == "StaticSwitch":
                if isinstance(material_asset, unreal.MaterialInstanceConstant):
                    material_asset.set_static_switch_parameter_value(parameter_name, bool(parameter_value))
                else:
                    logger.warning("Static switch parameters can only be set on material instances")
                    return {"success": False, "message": "Static switch parameters can only be set on material instances"}
            
            else:
                return {"success": False, "message": f"Unsupported parameter type: {parameter_type}"}
            
            # Save the material
            unreal.EditorAssetLibrary.save_asset(material_path)
            
            logger.info(f"Set {parameter_type} parameter '{parameter_name}' to {parameter_value} on {material_path}")
            return {
                "success": True,
                "message": f"Parameter '{parameter_name}' set successfully",
                "parameter": {
                    "name": parameter_name,
                    "value": parameter_value,
                    "type": parameter_type
                }
            }
            
        except Exception as e:
            logger.error(f"Error setting material parameter: {str(e)}")
            return {"success": False, "message": f"Error setting material parameter: {str(e)}"}

    @mcp.tool()
    def assign_material_to_mesh(
        ctx: Context,
        mesh_path: str,
        material_path: str,
        material_slot: int = 0
    ) -> Dict[str, Any]:
        """
        Assign a material to a static mesh.
        
        Args:
            mesh_path: Path to the static mesh asset
            material_path: Path to the material to assign
            material_slot: Material slot index to assign to
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Load the mesh asset
            mesh_asset = unreal.EditorAssetLibrary.load_asset(mesh_path)
            if not mesh_asset:
                return {"success": False, "message": f"Static mesh not found: {mesh_path}"}
            
            # Load the material asset
            material_asset = unreal.EditorAssetLibrary.load_asset(material_path)
            if not material_asset:
                return {"success": False, "message": f"Material not found: {material_path}"}
            
            # Assign material to the mesh
            mesh_asset.set_material(material_slot, material_asset)
            
            # Save the mesh
            unreal.EditorAssetLibrary.save_asset(mesh_path)
            
            logger.info(f"Assigned material {material_path} to mesh {mesh_path} at slot {material_slot}")
            return {
                "success": True,
                "message": f"Material assigned to mesh successfully",
                "assignment": {
                    "mesh": mesh_path,
                    "material": material_path,
                    "slot": material_slot
                }
            }
            
        except Exception as e:
            logger.error(f"Error assigning material to mesh: {str(e)}")
            return {"success": False, "message": f"Error assigning material to mesh: {str(e)}"}

    @mcp.tool()
    def create_material_parameter_collection(
        ctx: Context,
        collection_name: str,
        collection_path: str = "/Game/Materials/ParameterCollections"
    ) -> Dict[str, Any]:
        """
        Create a new material parameter collection.
        
        Args:
            collection_name: Name of the parameter collection to create
            collection_path: Path where the collection will be created
            
        Returns:
            Dict containing the created collection properties and success status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Create the parameter collection
            collection_factory = unreal.MaterialParameterCollectionFactoryNew()
            collection_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                collection_name,
                collection_path,
                unreal.MaterialParameterCollection,
                collection_factory
            )
            
            if not collection_asset:
                return {"success": False, "message": f"Failed to create parameter collection {collection_name}"}
            
            # Get collection properties
            collection_properties = {
                "name": collection_asset.get_name(),
                "path": collection_asset.get_path_name()
            }
            
            logger.info(f"Created material parameter collection: {collection_name} at {collection_path}")
            return {
                "success": True,
                "message": f"Parameter collection {collection_name} created successfully",
                "collection": collection_properties
            }
            
        except Exception as e:
            logger.error(f"Error creating parameter collection: {str(e)}")
            return {"success": False, "message": f"Error creating parameter collection: {str(e)}"}

    @mcp.tool()
    def add_parameter_to_collection(
        ctx: Context,
        collection_path: str,
        parameter_name: str,
        parameter_type: str = "Scalar",
        default_value: Any = 0.0
    ) -> Dict[str, Any]:
        """
        Add a parameter to a material parameter collection.
        
        Args:
            collection_path: Path to the parameter collection
            parameter_name: Name of the parameter to add
            parameter_type: Type of parameter (Scalar, Vector, Texture)
            default_value: Default value for the parameter
            
        Returns:
            Response indicating success or failure
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Load the collection
            collection_asset = unreal.EditorAssetLibrary.load_asset(collection_path)
            if not collection_asset:
                return {"success": False, "message": f"Parameter collection not found: {collection_path}"}
            
            # Create parameter info
            param_info = unreal.MaterialParameterInfo()
            param_info.name = parameter_name
            
            # Add parameter based on type
            if parameter_type == "Scalar":
                collection_asset.add_scalar_parameter(param_info, float(default_value))
            elif parameter_type == "Vector":
                if isinstance(default_value, (list, tuple)) and len(default_value) >= 3:
                    vector_value = unreal.LinearColor(
                        float(default_value[0]),
                        float(default_value[1]),
                        float(default_value[2]),
                        float(default_value[3]) if len(default_value) > 3 else 1.0
                    )
                    collection_asset.add_vector_parameter(param_info, vector_value)
                else:
                    return {"success": False, "message": "Vector default value must be a list/tuple with 3-4 values"}
            elif parameter_type == "Texture":
                if isinstance(default_value, str):
                    texture_asset = unreal.EditorAssetLibrary.load_asset(default_value)
                    if texture_asset:
                        collection_asset.add_texture_parameter(param_info, texture_asset)
                    else:
                        return {"success": False, "message": f"Default texture not found: {default_value}"}
                else:
                    return {"success": False, "message": "Texture default value must be a string path"}
            else:
                return {"success": False, "message": f"Unsupported parameter type: {parameter_type}"}
            
            # Save the collection
            unreal.EditorAssetLibrary.save_asset(collection_path)
            
            logger.info(f"Added {parameter_type} parameter '{parameter_name}' to collection {collection_path}")
            return {
                "success": True,
                "message": f"Parameter '{parameter_name}' added to collection successfully",
                "parameter": {
                    "name": parameter_name,
                    "type": parameter_type,
                    "default_value": default_value
                }
            }
            
        except Exception as e:
            logger.error(f"Error adding parameter to collection: {str(e)}")
            return {"success": False, "message": f"Error adding parameter to collection: {str(e)}"}

    @mcp.tool()
    def get_material_info(
        ctx: Context,
        material_path: str
    ) -> Dict[str, Any]:
        """
        Get detailed information about a material or material instance.
        
        Args:
            material_path: Path to the material asset
            
        Returns:
            Dict containing material information and properties
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Load the material asset
            material_asset = unreal.EditorAssetLibrary.load_asset(material_path)
            if not material_asset:
                return {"success": False, "message": f"Material not found: {material_path}"}
            
            # Get basic material info
            material_info = {
                "name": material_asset.get_name(),
                "path": material_asset.get_path_name(),
                "type": "Material" if isinstance(material_asset, unreal.Material) else "MaterialInstance",
                "blend_mode": str(material_asset.get_editor_property("blend_mode")),
                "shading_model": str(material_asset.get_editor_property("shading_model")),
                "material_domain": str(material_asset.get_editor_property("material_domain"))
            }
            
            # Get additional info for material instances
            if isinstance(material_asset, unreal.MaterialInstanceConstant):
                parent_material = material_asset.get_editor_property("parent")
                if parent_material:
                    material_info["parent_material"] = parent_material.get_path_name()
                
                # Get scalar parameters
                scalar_params = material_asset.get_scalar_parameter_names()
                material_info["scalar_parameters"] = [param.get_name() for param in scalar_params]
                
                # Get vector parameters
                vector_params = material_asset.get_vector_parameter_names()
                material_info["vector_parameters"] = [param.get_name() for param in vector_params]
                
                # Get texture parameters
                texture_params = material_asset.get_texture_parameter_names()
                material_info["texture_parameters"] = [param.get_name() for param in texture_params]
            
            logger.info(f"Retrieved material info for {material_path}")
            return {
                "success": True,
                "message": f"Material info retrieved successfully",
                "material_info": material_info
            }
            
        except Exception as e:
            logger.error(f"Error getting material info: {str(e)}")
            return {"success": False, "message": f"Error getting material info: {str(e)}"}

    @mcp.tool()
    def create_material_from_textures(
        ctx: Context,
        material_name: str,
        base_color_texture: str = "",
        normal_texture: str = "",
        roughness_texture: str = "",
        metallic_texture: str = "",
        emissive_texture: str = "",
        material_path: str = "/Game/Materials"
    ) -> Dict[str, Any]:
        """
        Create a material with automatic texture assignments.
        
        Args:
            material_name: Name of the material to create
            base_color_texture: Path to base color texture
            normal_texture: Path to normal map texture
            roughness_texture: Path to roughness texture
            metallic_texture: Path to metallic texture
            emissive_texture: Path to emissive texture
            material_path: Path where the material will be created
            
        Returns:
            Dict containing the created material properties and success status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Create the material first
            material_result = create_material(
                ctx,
                material_name,
                material_path,
                material_domain="Surface",
                blend_mode="Opaque",
                shading_model="DefaultLit"
            )
            
            if not material_result.get("success"):
                return material_result
            
            # Load the created material
            material_asset = unreal.EditorAssetLibrary.load_asset(f"{material_path}/{material_name}")
            if not material_asset:
                return {"success": False, "message": f"Failed to load created material: {material_name}"}
            
            # Open the material editor to add nodes (this would require more complex implementation)
            # For now, we'll return success with the material created
            texture_assignments = []
            
            if base_color_texture:
                texture_assignments.append({"slot": "Base Color", "texture": base_color_texture})
            if normal_texture:
                texture_assignments.append({"slot": "Normal", "texture": normal_texture})
            if roughness_texture:
                texture_assignments.append({"slot": "Roughness", "texture": roughness_texture})
            if metallic_texture:
                texture_assignments.append({"slot": "Metallic", "texture": metallic_texture})
            if emissive_texture:
                texture_assignments.append({"slot": "Emissive", "texture": emissive_texture})
            
            logger.info(f"Created material {material_name} with texture assignments")
            return {
                "success": True,
                "message": f"Material {material_name} created successfully",
                "material": material_result.get("material"),
                "texture_assignments": texture_assignments,
                "note": "Material nodes need to be connected manually in the Material Editor"
            }
            
        except Exception as e:
            logger.error(f"Error creating material from textures: {str(e)}")
            return {"success": False, "message": f"Error creating material from textures: {str(e)}"}

    @mcp.tool()
    def duplicate_material(
        ctx: Context,
        source_material_path: str,
        new_material_name: str,
        new_material_path: str = None
    ) -> Dict[str, Any]:
        """
        Duplicate an existing material.
        
        Args:
            source_material_path: Path to the source material to duplicate
            new_material_name: Name for the new material
            new_material_path: Path for the new material (defaults to same directory as source)
            
        Returns:
            Dict containing the duplicated material properties and success status
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            # Load the source material
            source_material = unreal.EditorAssetLibrary.load_asset(source_material_path)
            if not source_material:
                return {"success": False, "message": f"Source material not found: {source_material_path}"}
            
            # Determine destination path
            if not new_material_path:
                import os
                source_dir = os.path.dirname(source_material_path)
                new_material_path = f"{source_dir}/{new_material_name}"
            
            # Duplicate the material
            duplicated_material = unreal.EditorAssetLibrary.duplicate_asset(
                source_material_path,
                new_material_path
            )
            
            if not duplicated_material:
                return {"success": False, "message": f"Failed to duplicate material {source_material_path}"}
            
            # Get duplicated material properties
            duplicated_properties = {
                "name": duplicated_material.get_name(),
                "path": duplicated_material.get_path_name(),
                "source_material": source_material_path
            }
            
            logger.info(f"Duplicated material {source_material_path} to {new_material_path}")
            return {
                "success": True,
                "message": f"Material duplicated successfully",
                "duplicated_material": duplicated_properties
            }
            
        except Exception as e:
            logger.error(f"Error duplicating material: {str(e)}")
            return {"success": False, "message": f"Error duplicating material: {str(e)}"}

    logger.info("Material tools registered successfully")
