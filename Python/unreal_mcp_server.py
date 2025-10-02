"""
Unreal Engine MCP Server

Advanced Model Context Protocol server for comprehensive Unreal Engine 5.6 integration.
Provides complete UMG widget system, Blueprint management, actor manipulation, and 
enhanced UI building capabilities with persistent style sets and complex property support.

Features:
- Socket-based TCP communication on localhost:55557
- Hierarchical UI construction with JSON definitions
- Style set system for consistent theming
- Data binding and MVVM pattern support
- Widget animation and event handling
- Blueprint graph introspection and node management
- Actor spawning and property manipulation
- Enhanced Blueprint node property system with pin value support
- Comprehensive configuration management system

Architecture:
- FastMCP framework with async context management
- Connection-per-command pattern (Unreal closes after each operation)
- Comprehensive error handling and logging
- Modular tool registration system
- Configuration-driven behavior with validation

Usage:
1. Ensure Unreal Engine 5.6 is running with UnrealMCP plugin loaded
2. Start this server via stdio transport
3. Use MCP client to interact with registered tools
4. All responses include 'success' field for error checking

For complete tool documentation, use the info() prompt.
"""

import logging
import socket
import sys
import json
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

# Initialize logger first (will be reconfigured after config load)
logger = logging.getLogger("UnrealMCP")

# Default configuration values (used if no config file is found)
DEFAULT_UNREAL_HOST = "127.0.0.1"  # Always localhost - Unreal plugin listens locally only
DEFAULT_UNREAL_PORT = 55557        # Default UnrealMCP plugin port - must match plugin settings

# Global configuration state
_config = None

def load_configuration():
    """Load configuration from file or use defaults."""
    global _config
    
    try:
        from tools.config_manager import get_config_manager
        config_manager = get_config_manager()
        _config = config_manager.load_config()
        
        # Reconfigure logging based on loaded config
        logging_config = _config.logging
        
        # Clear existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Configure logging level
        log_level = getattr(logging, logging_config.level.value)
        logger.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(logging_config.format)
        
        # Add file handler if enabled
        if logging_config.file_enabled:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                logging_config.file_path,
                maxBytes=logging_config.file_max_size,
                backupCount=logging_config.file_backup_count
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Add console handler if enabled
        if logging_config.console_enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, logging_config.console_level.value))
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        logger.info(f"Configuration loaded successfully from: {config_manager._config_file_path}")
        logger.info(f"Environment: {_config.environment}, Debug mode: {_config.debug_mode}")
        
        return _config
        
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        logger.info("Using default configuration")
        
        # Use default configuration
        from tools.config_manager import UnrealMCPConfig
        _config = UnrealMCPConfig()
        
        # Configure basic logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            handlers=[
                logging.FileHandler('unreal_mcp.log'),
            ]
        )
        
        return _config

def get_config():
    """Get the current configuration."""
    global _config
    if _config is None:
        _config = load_configuration()
    return _config

class UnrealConnection:
    """Connection to an Unreal Engine instance."""
    
    def __init__(self):
        """Initialize the connection."""
        self.socket = None
        self.connected = False
    
    def connect(self) -> bool:
        """Connect to the Unreal Engine instance."""
        try:
            # Close any existing socket
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            
            # Get configuration
            config = get_config()
            connection_config = config.connection
            
            logger.info(f"Connecting to Unreal at {connection_config.host}:{connection_config.port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(connection_config.timeout)
            
            # Set socket options for better stability
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            # Set buffer sizes from configuration
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, connection_config.buffer_size)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, connection_config.buffer_size)
            
            self.socket.connect((connection_config.host, connection_config.port))
            self.connected = True
            logger.info("Connected to Unreal Engine")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Unreal: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from the Unreal Engine instance."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        self.connected = False

    def receive_full_response(self, sock, buffer_size=4096) -> bytes:
        """Receive a complete response from Unreal, handling chunked data."""
        chunks = []
        sock.settimeout(5)  # 5 second timeout
        try:
            while True:
                chunk = sock.recv(buffer_size)
                if not chunk:
                    if not chunks:
                        raise Exception("Connection closed before receiving data")
                    break
                chunks.append(chunk)
                
                # Process the data received so far
                data = b''.join(chunks)
                decoded_data = data.decode('utf-8')
                
                # Try to parse as JSON to check if complete
                try:
                    json.loads(decoded_data)
                    logger.info(f"Received complete response ({len(data)} bytes)")
                    return data
                except json.JSONDecodeError:
                    # Not complete JSON yet, continue reading
                    logger.debug(f"Received partial response, waiting for more data...")
                    continue
                except Exception as e:
                    logger.warning(f"Error processing response chunk: {str(e)}")
                    continue
        except socket.timeout:
            logger.warning("Socket timeout during receive")
            if chunks:
                # If we have some data already, try to use it
                data = b''.join(chunks)
                try:
                    json.loads(data.decode('utf-8'))
                    logger.info(f"Using partial response after timeout ({len(data)} bytes)")
                    return data
                except:
                    pass
            raise Exception("Timeout receiving Unreal response")
        except Exception as e:
            logger.error(f"Error during receive: {str(e)}")
            raise
    
    def send_command(self, command: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send a command to Unreal Engine and get the response."""
        # Always reconnect for each command, since Unreal closes the connection after each command
        # This is different from Unity which keeps connections alive
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            self.connected = False
        
        if not self.connect():
            logger.error("Failed to connect to Unreal Engine for command")
            return None
        
        try:
            # Match Unity's command format exactly
            command_obj = {
                "type": command,  # Use "type" instead of "command"
                "params": params or {}  # Use Unity's params or {} pattern
            }
            
            # Send without newline, exactly like Unity
            command_json = json.dumps(command_obj)
            logger.info(f"Sending command: {command_json}")
            self.socket.sendall(command_json.encode('utf-8'))
            
            # Read response using improved handler
            response_data = self.receive_full_response(self.socket)
            response = json.loads(response_data.decode('utf-8'))
            
            # Log complete response for debugging
            logger.info(f"Complete response from Unreal: {response}")
            
            # Check for both error formats: {"status": "error", ...} and {"success": false, ...}
            if response.get("status") == "error":
                error_message = response.get("error") or response.get("message", "Unknown Unreal error")
                logger.error(f"Unreal error (status=error): {error_message}")
                # We want to preserve the original error structure but ensure error is accessible
                if "error" not in response:
                    response["error"] = error_message
            elif response.get("success") is False:
                # This format uses {"success": false, "error": "message"} or {"success": false, "message": "message"}
                error_message = response.get("error") or response.get("message", "Unknown Unreal error")
                logger.error(f"Unreal error (success=false): {error_message}")
                # Convert to the standard format expected by higher layers
                response = {
                    "status": "error",
                    "error": error_message
                }
            
            # Always close the connection after command is complete
            # since Unreal will close it on its side anyway
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            self.connected = False
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending command: {e}")
            # Always reset connection state on any error
            self.connected = False
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            return {
                "status": "error",
                "error": str(e)
            }

# Global connection state
_unreal_connection: UnrealConnection = None

def get_unreal_connection() -> Optional[UnrealConnection]:
    """Get the connection to Unreal Engine."""
    global _unreal_connection
    try:
        if _unreal_connection is None:
            _unreal_connection = UnrealConnection()
            if not _unreal_connection.connect():
                logger.warning("Could not connect to Unreal Engine")
                _unreal_connection = None
        else:
            # Verify connection is still valid with a ping-like test
            try:
                # Simple test by sending an empty buffer to check if socket is still connected
                _unreal_connection.socket.sendall(b'\x00')
                logger.debug("Connection verified with ping test")
            except Exception as e:
                logger.warning(f"Existing connection failed: {e}")
                _unreal_connection.disconnect()
                _unreal_connection = None
                # Try to reconnect
                _unreal_connection = UnrealConnection()
                if not _unreal_connection.connect():
                    logger.warning("Could not reconnect to Unreal Engine")
                    _unreal_connection = None
                else:
                    logger.info("Successfully reconnected to Unreal Engine")
        
        return _unreal_connection
    except Exception as e:
        logger.error(f"Error getting Unreal connection: {e}")
        return None

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Handle server startup and shutdown."""
    global _unreal_connection
    
    # Load configuration first
    logger.info("UnrealMCP server starting up")
    try:
        config = load_configuration()
        logger.info(f"Configuration loaded: {config.environment} environment, debug={config.debug_mode}")
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        config = None
    
    # Initialize Unreal connection
    try:
        _unreal_connection = get_unreal_connection()
        if _unreal_connection:
            logger.info("Connected to Unreal Engine on startup")
        else:
            logger.warning("Could not connect to Unreal Engine on startup")
    except Exception as e:
        logger.error(f"Error connecting to Unreal Engine on startup: {e}")
        _unreal_connection = None
    
    try:
        yield {}
    finally:
        if _unreal_connection:
            _unreal_connection.disconnect()
            _unreal_connection = None
        logger.info("Unreal MCP server shut down")

# Initialize server
mcp = FastMCP(
    name="UnrealMCP",
    instructions="Unreal Engine integration via Model Context Protocol",
    lifespan=server_lifespan
)

# Import and register tools
from tools.editor_tools import register_editor_tools
from tools.blueprint_tools import register_blueprint_tools
from tools.node_tools import register_blueprint_node_tools
from tools.project_tools import register_project_tools
from tools.umg_tools import register_umg_tools
from tools.animation_blueprint_tools import register_animation_blueprint_tools
from tools.material_tools import register_material_tools
from tools.enhanced_input_tools import register_enhanced_input_tools
from tools.umg_reflection import register_umg_reflection_tools
from tools.asset_discovery import register_asset_discovery_tools
from tools.umg_events import register_umg_event_tools
from tools.system_diagnostics import register_system_diagnostic_tools
from tools.umg_styling import register_umg_styling_tools
from tools.umg_discovery import register_umg_discovery_tools

# Register tools
register_editor_tools(mcp)
register_blueprint_tools(mcp)
register_blueprint_node_tools(mcp)
register_project_tools(mcp)
register_umg_tools(mcp)
register_animation_blueprint_tools(mcp)
register_material_tools(mcp)
register_enhanced_input_tools(mcp)
register_umg_reflection_tools(mcp)
register_asset_discovery_tools(mcp)
register_umg_event_tools(mcp)
register_system_diagnostic_tools(mcp)
register_umg_styling_tools(mcp)
register_umg_discovery_tools(mcp)  

@mcp.prompt()
def info():
    """Information about available Unreal MCP tools and best practices."""
    return """
    # Unreal MCP Server Tools and Best Practices
    
    ## UMG (Widget Blueprint) Tools
    - `create_umg_widget_blueprint(widget_name, parent_class="UserWidget", path="/Game/UI")` 
      Create a new UMG Widget Blueprint
    - `add_text_block_to_widget(widget_name, text_block_name, text="", position=[0,0], size=[200,50], font_size=12, color=[1,1,1,1])`
      Add a Text Block widget with customizable properties
    - `add_button_to_widget(widget_name, button_name, text="", position=[0,0], size=[200,50], font_size=12, color=[1,1,1,1], background_color=[0.1,0.1,0.1,1])`
      Add a Button widget with text and styling
    - `bind_widget_event(widget_name, widget_component_name, event_name, function_name="")`
      Bind events like OnClicked to functions
    - `add_widget_to_viewport(widget_name, z_order=0)`
      Add widget instance to game viewport
    - `set_text_block_binding(widget_name, text_block_name, binding_property, binding_type="Text")`
      Set up dynamic property binding for text blocks

    ## Editor Tools
    ### Viewport and Screenshots
    - `focus_viewport(target, location, distance, orientation)` - Focus viewport
    - `take_screenshot(filename, show_ui, resolution)` - Capture screenshots

    ### Actor Management
    - `get_actors_in_level()` - List all actors in current level
    - `find_actors_by_name(pattern)` - Find actors by name pattern
    - `spawn_actor(name, type, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1])` - Create actors
    - `delete_actor(name)` - Remove actors
    - `set_actor_transform(name, location, rotation, scale)` - Modify actor transform
    - `get_actor_properties(name)` - Get actor properties
    
    ## Blueprint Management
    - `create_blueprint(name, parent_class)` - Create new Blueprint classes
    - `add_component_to_blueprint(blueprint_name, component_type, component_name)` - Add components
    - `set_static_mesh_properties(blueprint_name, component_name, static_mesh)` - Configure meshes
    - `set_physics_properties(blueprint_name, component_name)` - Configure physics
    - `compile_blueprint(blueprint_name)` - Compile Blueprint changes
    - `set_blueprint_property(blueprint_name, property_name, property_value)` - Set properties
    - `set_pawn_properties(blueprint_name)` - Configure Pawn settings
    - `spawn_blueprint_actor(blueprint_name, actor_name)` - Spawn Blueprint actors
    
    ## Animation Blueprint Management
    - `create_animation_blueprint(name, parent_class="AnimInstance", target_skeleton="", path="/Game/Animations")` - Create Animation Blueprint
    - `create_animation_blueprint_with_skeleton(name, skeleton_path, parent_class="AnimInstance", path="/Game/Animations")` - Create with skeleton
    - `set_animation_blueprint_target_skeleton(blueprint_name, skeleton_path)` - Set target skeleton
    - `get_animation_blueprint_info(blueprint_name)` - Get comprehensive animation blueprint info
    - `create_animation_state_machine(blueprint_name, state_machine_name, graph_name="AnimGraph")` - Create state machine
    - `add_animation_state(blueprint_name, state_machine_name, state_name, animation_sequence="", state_type="AnimationState")` - Add animation state
    - `connect_animation_states(blueprint_name, state_machine_name, from_state, to_state, transition_rule="Always")` - Connect states
    - `set_animation_state_machine_entry_state(blueprint_name, state_machine_name, entry_state)` - Set entry state
    - `create_animation_blend_space(blueprint_name, blend_space_name, blend_space_type="1D", skeleton_path="")` - Create blend space
    - `add_animation_to_blend_space(blueprint_name, blend_space_name, animation_sequence, blend_position=[0.0, 0.0])` - Add animation to blend space
    - `create_animation_blend_node(blueprint_name, node_name, blend_type="BlendPoses", input_count=2)` - Create blend node
    - `add_animation_sequence_node(blueprint_name, node_name, animation_sequence, graph_name="AnimGraph")` - Add sequence node
    - `add_animation_output_node(blueprint_name, node_name="OutputPose", graph_name="AnimGraph")` - Add output node
    - `connect_animation_nodes(blueprint_name, source_node, target_node, source_pin="Pose", target_pin="Pose", graph_name="AnimGraph")` - Connect animation nodes
    - `add_animation_blueprint_variable(blueprint_name, variable_name, variable_type="Float", default_value=None, is_exposed=False)` - Add variable
    - `get_animation_blueprint_variables(blueprint_name)` - Get all variables
    - `add_animation_montage_node(blueprint_name, node_name, montage_asset, graph_name="AnimGraph")` - Add montage node
    - `create_animation_montage(montage_name, skeleton_path, animation_sequence="", path="/Game/Animations")` - Create montage asset
    - `compile_animation_blueprint(blueprint_name)` - Compile animation blueprint
    - `validate_animation_blueprint(blueprint_name)` - Validate animation blueprint
    - `get_animation_blueprint_compilation_errors(blueprint_name)` - Get compilation errors
    - `get_available_animation_blueprint_types()` - Get available types and capabilities
    - `create_complete_animation_blueprint(name, skeleton_path, include_state_machine=True, include_blend_space=True, include_basic_animations=True, path="/Game/Animations")` - Create complete setup
    
    ## Blueprint Node Management
    - `add_blueprint_event_node(blueprint_name, event_type)` - Add event nodes
    - `add_blueprint_input_action_node(blueprint_name, action_name)` - Add input nodes
    - `add_blueprint_function_node(blueprint_name, target, function_name)` - Add function nodes
    - `connect_blueprint_nodes(blueprint_name, source_node_id, source_pin, target_node_id, target_pin)` - Connect nodes
    - `add_blueprint_variable(blueprint_name, variable_name, variable_type)` - Add variables
    - `add_blueprint_get_self_component_reference(blueprint_name, component_name)` - Add component refs
    - `add_blueprint_self_reference(blueprint_name)` - Add self references
    - `find_blueprint_nodes(blueprint_name, node_type, event_type)` - Find nodes
    
    ## Project Tools
    - `create_input_mapping(action_name, key, input_type)` - Create input mappings
    - `get_project_info()` - Get comprehensive project information
    - `get_engine_settings()` - Get current engine settings
    - `set_engine_setting(setting_name, setting_value, section)` - Set engine configuration
    - `get_plugin_info(plugin_name)` - Get plugin information (all or specific)
    - `enable_plugin(plugin_name)` - Enable a plugin
    - `disable_plugin(plugin_name)` - Disable a plugin
    - `get_build_targets()` - Get build targets information
    - `create_content_folder(folder_path, folder_name)` - Create content browser folders
    - `get_project_diagnostics()` - Get project diagnostics and validation
    - `validate_project(check_plugins, check_blueprints, check_assets)` - Validate project integrity
    
    ## Configuration Management Tools
    - `get_config_info()` - Get current configuration information
    - `load_config_file(config_file)` - Load configuration from a file
    - `save_config_file(config_data, config_file)` - Save configuration to a file
    - `create_default_config(config_file)` - Create a default configuration file
    - `validate_config(config_file)` - Validate configuration file
    - `reload_config()` - Reload configuration from file
    - `get_tool_config(tool_name)` - Get configuration for a specific tool
    - `update_tool_config(tool_name, tool_config_data)` - Update configuration for a specific tool
    - `check_config_changes()` - Check if configuration file has changed since last load
    - `list_config_files(config_dir)` - List available configuration files
    
    ## Best Practices
    
    ### UMG Widget Development
    - Create widgets with descriptive names that reflect their purpose
    - Use consistent naming conventions for widget components
    - Organize widget hierarchy logically
    - Set appropriate anchors and alignment for responsive layouts
    - Use property bindings for dynamic updates instead of direct setting
    - Handle widget events appropriately with meaningful function names
    - Clean up widgets when no longer needed
    - Test widget layouts at different resolutions
    
    ### Editor and Actor Management
    - Use unique names for actors to avoid conflicts
    - Clean up temporary actors
    - Validate transforms before applying
    - Check actor existence before modifications
    - Take regular viewport screenshots during development
    - Keep the viewport focused on relevant actors during operations
    
    ### Blueprint Development
    - Compile Blueprints after changes
    - Use meaningful names for variables and functions
    - Organize nodes logically
    - Test functionality in isolation
    - Consider performance implications
    - Document complex setups
    
    ### Configuration Management
    - Use environment-specific configuration files (development.yaml, production.yaml)
    - Validate configuration files before deployment
    - Use environment variables for sensitive settings (API keys, passwords)
    - Keep configuration files in version control with appropriate security
    - Test configuration changes in development before production
    - Use configuration validation tools to catch issues early
    - Document custom configuration settings and their purposes
    - Use hot-reload for development, disable for production
    - Monitor configuration changes and log important updates
    
    ### Error Handling
    - Check command responses for success
    - Handle errors gracefully
    - Log important operations
    - Validate parameters
    - Clean up resources on errors
    """

# Run the server
if __name__ == "__main__":
    logger.info("Starting MCP server with stdio transport")
    mcp.run(transport='stdio') 