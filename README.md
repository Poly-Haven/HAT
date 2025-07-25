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

* [x] All objects have applied scale (1.0) to ensure no unexpected behaviour
* [x] Blender version is the latest official release
* [x] Model collection name should match the asset slug
* [x] Texture datablock names should match their file names
* [x] File size is within acceptable limits for the asset type
* [x] All referenced texture files exist on disk
* [x] Geometry nodes collections are properly structured with LOD0 or static collections
* [x] LOD (Level of Detail) collections and objects are properly structured
* [x] Texture map names follow standardized naming conventions
* [x] Material IOR (Index of Refraction) values are not set to 0
* [x] Material names should match the asset slug
* [x] No world or HDRI data blocks should be present in the asset
* [x] Texture maps use appropriate color space settings (Non-Color Data when required)
* [x] Objects should be at the origin
* [x] File should contain only one scene and one view layer
* [x] No orphaned data blocks (unused data) should be present
* [x] No texture files should be packed into the blend file
* [x] All texture paths should be relative and point to the textures folder
* [x] All texture resolutions should match within the asset
* [x] Objects should not have shape keys which may cause issues for GLTF export
* [x] Asset slug follows proper naming conventions (lowercase, allowed characters only)
* [x] Texture preview plane has non-default dimensions
* [x] Texture file names should start with the asset slug and follow naming conventions
* [x] Scene unit scale is set to 1.0 meters
* [x] Objects should not have vertex colors which may break GLTF export

To do:

* [ ] Main collection is visible and renderable

Tools:

* [ ] Test FBX export
* [x] Export GLTF
* [x] Clean file of unused datablocks, including fake-user ones
* [x] Make image datablock names match their file names
* [ ] Make mesh datablock name match object name

Misc:

* [x] Pre-save handler to set viewport shading solid
