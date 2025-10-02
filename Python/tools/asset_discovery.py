"""
Asset Discovery Tools for Unreal MCP.

This module provides advanced asset management capabilities including smart search,
import/export functionality, and AI analysis integration for Unreal Engine assets.
"""

import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_asset_discovery_tools(mcp: FastMCP):
    """Register asset discovery tools with the MCP server."""

    @mcp.tool()
    def import_texture_asset(
        ctx: Context,
        file_path: str,
        asset_name: str = "",
        destination_path: str = "/Game/Textures",
        import_settings: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Import a texture asset into the Unreal Engine project.
        
        Supports various image formats and provides options for texture compression,
        mipmap generation, and other import settings.
        
        Args:
            file_path: Path to the texture file to import
            asset_name: Name for the imported asset (defaults to filename)
            destination_path: Content browser path for the imported asset
            import_settings: Dictionary of import settings (compression, mipmaps, etc.)
            
        Returns:
            Dict containing import confirmation and asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "file_path": file_path,
                "asset_name": asset_name,
                "destination_path": destination_path,
                "import_settings": import_settings or {}
            }
            
            logger.info(f"Importing texture asset: {file_path}")
            response = unreal.send_command("import_texture_asset", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Texture import response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error importing texture asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def export_texture_for_analysis(
        ctx: Context,
        asset_path: str,
        output_path: str = "",
        export_format: str = "PNG",
        resolution: int = 1024
    ) -> Dict[str, Any]:
        """
        Export a texture asset for AI analysis or external processing.
        
        Useful for analyzing textures with AI tools, creating thumbnails,
        or preparing assets for external editing.
        
        Args:
            asset_path: Path to the texture asset in Unreal
            output_path: Output file path (defaults to asset name with format extension)
            export_format: Export format (PNG, JPG, TGA, etc.)
            resolution: Export resolution (will be clamped to asset's maximum)
            
        Returns:
            Dict containing export confirmation and file path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_path": asset_path,
                "output_path": output_path,
                "export_format": export_format,
                "resolution": resolution
            }
            
            logger.info(f"Exporting texture for analysis: {asset_path}")
            response = unreal.send_command("export_texture_for_analysis", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Texture export response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error exporting texture: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_asset_info(
        ctx: Context,
        asset_path: str
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific asset.
        
        Provides comprehensive asset metadata including:
        - Asset type and class information
        - File size and import settings
        - Dependencies and references
        - Usage statistics
        - Metadata and tags
        
        Args:
            asset_path: Path to the asset in the content browser
            
        Returns:
            Dict containing detailed asset information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"asset_path": asset_path}
            
            logger.info(f"Getting asset info for: {asset_path}")
            response = unreal.send_command("get_asset_info", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Asset info response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting asset info: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def duplicate_asset(
        ctx: Context,
        source_asset_path: str,
        new_asset_name: str,
        destination_path: str = ""
    ) -> Dict[str, Any]:
        """
        Duplicate an existing asset with a new name.
        
        Useful for creating variations of existing assets or templates.
        
        Args:
            source_asset_path: Path to the source asset
            new_asset_name: Name for the duplicated asset
            destination_path: Path for the new asset (defaults to same as source)
            
        Returns:
            Dict containing duplication confirmation and new asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "source_asset_path": source_asset_path,
                "new_asset_name": new_asset_name,
                "destination_path": destination_path
            }
            
            logger.info(f"Duplicating asset: {source_asset_path} to {new_asset_name}")
            response = unreal.send_command("duplicate_asset", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Asset duplication response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error duplicating asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def rename_asset(
        ctx: Context,
        asset_path: str,
        new_name: str
    ) -> Dict[str, Any]:
        """
        Rename an existing asset.
        
        Args:
            asset_path: Current path of the asset
            new_name: New name for the asset
            
        Returns:
            Dict containing rename confirmation and new asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_path": asset_path,
                "new_name": new_name
            }
            
            logger.info(f"Renaming asset: {asset_path} to {new_name}")
            response = unreal.send_command("rename_asset", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Asset rename response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error renaming asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def move_asset(
        ctx: Context,
        asset_path: str,
        destination_path: str
    ) -> Dict[str, Any]:
        """
        Move an asset to a different location in the content browser.
        
        Args:
            asset_path: Current path of the asset
            destination_path: New destination path
            
        Returns:
            Dict containing move confirmation and new asset path
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_path": asset_path,
                "destination_path": destination_path
            }
            
            logger.info(f"Moving asset: {asset_path} to {destination_path}")
            response = unreal.send_command("move_asset", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Asset move response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error moving asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def delete_asset(
        ctx: Context,
        asset_path: str,
        force: bool = False
    ) -> Dict[str, Any]:
        """
        Delete an asset from the project.
        
        ⚠️ WARNING: This operation cannot be undone without version control.
        
        Args:
            asset_path: Path to the asset to delete
            force: Whether to force deletion even if asset is referenced
            
        Returns:
            Dict containing deletion confirmation
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {
                "asset_path": asset_path,
                "force": force
            }
            
            logger.info(f"Deleting asset: {asset_path}")
            response = unreal.send_command("delete_asset", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Asset deletion response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error deleting asset: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_asset_dependencies(
        ctx: Context,
        asset_path: str
    ) -> Dict[str, Any]:
        """
        Get all dependencies and references for an asset.
        
        Shows which other assets this asset depends on and which assets
        depend on this one.
        
        Args:
            asset_path: Path to the asset to analyze
            
        Returns:
            Dict containing dependency information
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"asset_path": asset_path}
            
            logger.info(f"Getting asset dependencies for: {asset_path}")
            response = unreal.send_command("get_asset_dependencies", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Asset dependencies response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting asset dependencies: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def get_asset_usage_stats(
        ctx: Context,
        asset_path: str
    ) -> Dict[str, Any]:
        """
        Get usage statistics for an asset.
        
        Shows how the asset is being used throughout the project,
        including references in Blueprints, levels, and other assets.
        
        Args:
            asset_path: Path to the asset to analyze
            
        Returns:
            Dict containing usage statistics and reference locations
        """
        from unreal_mcp_server import get_unreal_connection
        
        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}
            
            params = {"asset_path": asset_path}
            
            logger.info(f"Getting asset usage stats for: {asset_path}")
            response = unreal.send_command("get_asset_usage_stats", params)
            
            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}
            
            logger.info(f"Asset usage stats response: {response}")
            return response or {}
            
        except Exception as e:
            error_msg = f"Error getting asset usage stats: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
