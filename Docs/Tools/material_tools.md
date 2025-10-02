# Material Tools Documentation

## Overview

The Material Tools module provides comprehensive material management capabilities for Unreal Engine through the MCP (Model Context Protocol) interface. This module enables creation, manipulation, and management of materials, material instances, and material parameter collections.

## Features

### Core Material Operations
- **Material Creation**: Create new materials with customizable properties
- **Material Instance Management**: Create and configure material instances
- **Parameter Management**: Set scalar, vector, texture, and static switch parameters
- **Material Assignment**: Assign materials to static meshes
- **Material Information**: Retrieve detailed material properties and parameters

### Advanced Features
- **Parameter Collections**: Create and manage global material parameter collections
- **Texture-Based Materials**: Create materials with automatic texture assignments
- **Material Duplication**: Duplicate existing materials with all properties
- **Material Domain Support**: Support for Surface, PostProcess, LightFunction, and other domains
- **Blend Mode Configuration**: Opaque, Masked, Translucent, Additive, and more
- **Shading Model Support**: DefaultLit, Unlit, Subsurface, and other shading models

## Available Tools

### 1. create_material
Creates a new material asset with specified properties.

**Parameters:**
- `material_name` (str): Name of the material to create
- `material_path` (str): Path where the material will be created (default: "/Game/Materials")
- `parent_material` (str): Parent material class (default: "/Engine/BasicShapes/BasicShapeMaterial")
- `material_domain` (str): Material domain - Surface, PostProcess, LightFunction, etc. (default: "Surface")
- `blend_mode` (str): Blend mode - Opaque, Masked, Translucent, Additive, etc. (default: "Opaque")
- `shading_model` (str): Shading model - DefaultLit, Unlit, Subsurface, etc. (default: "DefaultLit")

**Returns:**
- Success status and material properties

**Example:**
```python
result = create_material(
    material_name="MyMaterial",
    material_path="/Game/Materials",
    material_domain="Surface",
    blend_mode="Opaque",
    shading_model="DefaultLit"
)
```

### 2. create_material_instance
Creates a new material instance from a parent material.

**Parameters:**
- `instance_name` (str): Name of the material instance
- `parent_material` (str): Path to the parent material
- `instance_path` (str): Path where the instance will be created (default: "/Game/Materials/Instances")

**Returns:**
- Success status and material instance properties

**Example:**
```python
result = create_material_instance(
    instance_name="MyMaterialInstance",
    parent_material="/Game/Materials/MyMaterial",
    instance_path="/Game/Materials/Instances"
)
```

### 3. set_material_parameter
Sets parameter values on materials or material instances.

**Parameters:**
- `material_path` (str): Path to the material or material instance
- `parameter_name` (str): Name of the parameter to set
- `parameter_value` (Any): Value to set the parameter to
- `parameter_type` (str): Type of parameter - Scalar, Vector, Texture, StaticSwitch (default: "Scalar")

**Returns:**
- Success status and parameter information

**Example:**
```python
# Set scalar parameter
result = set_material_parameter(
    material_path="/Game/Materials/Instances/MyMaterialInstance",
    parameter_name="Metallic",
    parameter_value=0.5,
    parameter_type="Scalar"
)

# Set vector parameter (RGBA)
result = set_material_parameter(
    material_path="/Game/Materials/Instances/MyMaterialInstance",
    parameter_name="BaseColor",
    parameter_value=[1.0, 0.5, 0.2, 1.0],
    parameter_type="Vector"
)
```

### 4. assign_material_to_mesh
Assigns a material to a static mesh.

**Parameters:**
- `mesh_path` (str): Path to the static mesh asset
- `material_path` (str): Path to the material to assign
- `material_slot` (int): Material slot index to assign to (default: 0)

**Returns:**
- Success status and assignment information

**Example:**
```python
result = assign_material_to_mesh(
    mesh_path="/Game/Meshes/MyMesh",
    material_path="/Game/Materials/MyMaterial",
    material_slot=0
)
```

### 5. create_material_parameter_collection
Creates a new material parameter collection for global parameters.

**Parameters:**
- `collection_name` (str): Name of the parameter collection
- `collection_path` (str): Path where the collection will be created (default: "/Game/Materials/ParameterCollections")

**Returns:**
- Success status and collection properties

**Example:**
```python
result = create_material_parameter_collection(
    collection_name="GlobalParameters",
    collection_path="/Game/Materials/ParameterCollections"
)
```

### 6. add_parameter_to_collection
Adds a parameter to a material parameter collection.

**Parameters:**
- `collection_path` (str): Path to the parameter collection
- `parameter_name` (str): Name of the parameter to add
- `parameter_type` (str): Type of parameter - Scalar, Vector, Texture (default: "Scalar")
- `default_value` (Any): Default value for the parameter (default: 0.0)

**Returns:**
- Success status and parameter information

**Example:**
```python
result = add_parameter_to_collection(
    collection_path="/Game/Materials/ParameterCollections/GlobalParameters",
    parameter_name="GlobalMetallic",
    parameter_type="Scalar",
    default_value=0.3
)
```

### 7. get_material_info
Retrieves detailed information about a material or material instance.

**Parameters:**
- `material_path` (str): Path to the material asset

**Returns:**
- Success status and detailed material information

**Example:**
```python
result = get_material_info(
    material_path="/Game/Materials/MyMaterial"
)
```

### 8. create_material_from_textures
Creates a material with automatic texture assignments.

**Parameters:**
- `material_name` (str): Name of the material to create
- `base_color_texture` (str): Path to base color texture (optional)
- `normal_texture` (str): Path to normal map texture (optional)
- `roughness_texture` (str): Path to roughness texture (optional)
- `metallic_texture` (str): Path to metallic texture (optional)
- `emissive_texture` (str): Path to emissive texture (optional)
- `material_path` (str): Path where the material will be created (default: "/Game/Materials")

**Returns:**
- Success status, material properties, and texture assignments

**Example:**
```python
result = create_material_from_textures(
    material_name="TexturedMaterial",
    base_color_texture="/Game/Textures/BaseColor",
    normal_texture="/Game/Textures/Normal",
    roughness_texture="/Game/Textures/Roughness",
    material_path="/Game/Materials"
)
```

### 9. duplicate_material
Duplicates an existing material.

**Parameters:**
- `source_material_path` (str): Path to the source material to duplicate
- `new_material_name` (str): Name for the new material
- `new_material_path` (str): Path for the new material (optional, defaults to same directory as source)

**Returns:**
- Success status and duplicated material properties

**Example:**
```python
result = duplicate_material(
    source_material_path="/Game/Materials/MyMaterial",
    new_material_name="DuplicatedMaterial",
    new_material_path="/Game/Materials"
)
```

## Material Domains

The material system supports various domains for different use cases:

- **Surface**: Standard surface materials for meshes
- **PostProcess**: Post-processing effects
- **LightFunction**: Light function materials
- **DeferredDecal**: Deferred decal materials
- **Volume**: Volume materials
- **Blendable**: Blendable materials

## Blend Modes

Materials support various blend modes:

- **Opaque**: Standard opaque rendering
- **Masked**: Alpha masking with threshold
- **Translucent**: Alpha blending
- **Additive**: Additive blending
- **Modulate**: Modulate blending
- **AlphaComposite**: Alpha composite blending

## Shading Models

Different shading models are available:

- **DefaultLit**: Standard physically-based shading
- **Unlit**: Unlit shading (no lighting)
- **Subsurface**: Subsurface scattering
- **PreintegratedSkin**: Pre-integrated skin shading
- **ClearCoat**: Clear coat shading
- **SubsurfaceProfile**: Subsurface profile shading
- **TwoSidedFoliage**: Two-sided foliage shading

## Parameter Types

### Scalar Parameters
- Single float values
- Used for metallic, roughness, opacity, etc.
- Example: `0.5` for 50% metallic

### Vector Parameters
- RGBA color values
- Used for base color, emissive color, etc.
- Example: `[1.0, 0.5, 0.2, 1.0]` for orange color

### Texture Parameters
- Texture asset references
- Used for base color maps, normal maps, etc.
- Example: `"/Game/Textures/BaseColor"`

### Static Switch Parameters
- Boolean values
- Used for enabling/disabling material features
- Example: `True` or `False`

## Best Practices

### Material Organization
1. **Use descriptive names**: Choose clear, descriptive names for materials
2. **Organize in folders**: Group related materials in appropriate folders
3. **Use instances**: Create material instances for variations rather than new materials
4. **Parameter collections**: Use parameter collections for global parameters

### Performance Considerations
1. **Minimize parameters**: Only expose necessary parameters
2. **Use appropriate blend modes**: Choose the most efficient blend mode
3. **Optimize textures**: Use appropriate texture sizes and formats
4. **Instance reuse**: Reuse material instances when possible

### Workflow Tips
1. **Start with base materials**: Create base materials first, then instances
2. **Use parameter collections**: For global parameters that affect multiple materials
3. **Test in context**: Always test materials in their intended use context
4. **Document parameters**: Keep track of parameter purposes and ranges

## Error Handling

The material tools include comprehensive error handling:

- **Connection errors**: Handles Unreal Engine connection failures
- **Asset not found**: Validates asset existence before operations
- **Parameter validation**: Validates parameter types and values
- **Path validation**: Ensures valid asset paths
- **Type checking**: Validates parameter types match expected formats

## Integration with Other Tools

Material tools integrate seamlessly with other MCP tools:

- **Blueprint Tools**: Assign materials to Blueprint components
- **Actor Tools**: Apply materials to spawned actors
- **Project Tools**: Manage material-related project settings
- **UMG Tools**: Use materials in UI elements

## Examples

### Complete Material Workflow
```python
# 1. Create base material
base_material = create_material(
    material_name="MetalMaterial",
    material_path="/Game/Materials",
    material_domain="Surface",
    blend_mode="Opaque",
    shading_model="DefaultLit"
)

# 2. Create material instance
material_instance = create_material_instance(
    instance_name="RustedMetal",
    parent_material="/Game/Materials/MetalMaterial",
    instance_path="/Game/Materials/Instances"
)

# 3. Set parameters
set_material_parameter(
    material_path="/Game/Materials/Instances/RustedMetal",
    parameter_name="Metallic",
    parameter_value=0.8,
    parameter_type="Scalar"
)

set_material_parameter(
    material_path="/Game/Materials/Instances/RustedMetal",
    parameter_name="BaseColor",
    parameter_value=[0.7, 0.5, 0.3, 1.0],
    parameter_type="Vector"
)

# 4. Assign to mesh
assign_material_to_mesh(
    mesh_path="/Game/Meshes/MetalMesh",
    material_path="/Game/Materials/Instances/RustedMetal",
    material_slot=0
)
```

### Global Parameter Collection
```python
# 1. Create parameter collection
collection = create_material_parameter_collection(
    collection_name="GlobalLighting",
    collection_path="/Game/Materials/ParameterCollections"
)

# 2. Add global parameters
add_parameter_to_collection(
    collection_path="/Game/Materials/ParameterCollections/GlobalLighting",
    parameter_name="GlobalMetallic",
    parameter_type="Scalar",
    default_value=0.3
)

add_parameter_to_collection(
    collection_path="/Game/Materials/ParameterCollections/GlobalLighting",
    parameter_name="GlobalRoughness",
    parameter_type="Scalar",
    default_value=0.5
)
```

This comprehensive material tools system provides everything needed for advanced material management in Unreal Engine through the MCP interface.
