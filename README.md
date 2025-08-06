# HAT
Haven Asset Tester - A Blender add-on we use for texture and model QC

## How to install:

Add the following URL as a new Remote Repository extension in Blender:

> https://raw.githubusercontent.com/Poly-Haven/HAT/main/index.json

Search for the HAT extension and click Install.

## Features:

Checks:

<!-- This list is auto-generated from docstrings in operators/checks/*.py files.
     Run 'python build_readme_checklist.py' to update. -->

### Asset Structure

* [x] Model collection name should match the asset slug
* [x] Texture datablock names should match their file names
* [x] Geometry nodes collections are properly structured with LOD0 or static collections
* [x] LOD (Level of Detail) collections and objects are properly structured
* [x] No world or HDRI data blocks should be present in the asset
* [x] File should contain only one scene and one view layer
* [x] Texture assets should only have "Plane" and "Sphere" objects
* [x] No orphaned data blocks (unused data) should be present

### Files

* [x] File size is within acceptable limits for the asset type
* [x] All referenced texture files exist on disk
* [x] All texture paths should be relative and point to the textures folder

### Geometry

* [x] All objects have applied scale (1.0) to ensure no unexpected behaviour
* [x] Objects should be at the origin
* [x] Objects should not have shape keys which may cause issues for GLTF export
* [x] Scene unit scale is set to 1.0 meters
* [x] Objects should not have vertex colors which may break GLTF export

### Materials

* [x] Material IOR (Index of Refraction) values are within expected range
* [x] Material names should match the asset slug
* [x] Materials should not contain math nodes, which mess with exporters
* [x] Materials should not contain mix nodes
* [x] No unused nodes in materials
* [x] Image node labels (if set) should match map names
* [x] Materials should have exactly one output node
* [x] Only Principled BSDF shaders should be used
* [x] SSS may have been accidentally enabled
* [x] All textures should use UVs for mapping

### Naming

* [x] Asset slug follows proper naming conventions (lowercase, allowed characters only)

### Technical

* [x] Blender version is the latest official release

### Textures

* [x] Texture map names follow standardized naming conventions
* [x] Texture maps use appropriate color space settings (Non-Color Data when required)
* [x] No texture files should be packed into the blend file
* [x] Texture preview plane has non-default dimensions
* [x] Texture file names should start with the asset slug and follow naming conventions

To do:

* [ ] Main collection is visible and renderable

Tools:

* [ ] Test FBX export
* [x] Export GLTF
* [x] Clean file of unused datablocks, including fake-user ones
* [x] Make image datablock names match their file names
* [x] Open folder containing Blend file
* [ ] Make mesh datablock name match object name

Misc:

* [x] Pre-save handler to set viewport shading solid
