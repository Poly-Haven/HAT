# HAT
Haven Asset Tester - A Blender add-on we use for asset QC

## How to install:

Add the following URL as a new Remote Repository extension in Blender:

> https://raw.githubusercontent.com/Poly-Haven/HAT/main/index.json

Search for the HAT extension and click Install.

## Features / to do:

Checks:

* [x] Check maps use Non-color Data when required
* [x] Check if vertex colors exist (will screw up gltf export)
* [x] Unit Scale is 1.0
* [x] Warning if scale is not applied
* [x] Collection name should be same as slug (file name)
* [x] Texture file names should start with slug
* [x] Texture datablock should match file name
* [x] Texture files exist
* [x] Texture map names should be standardized
* [x] No packed texture files
* [x] Material names should match or start with slug
* [x] Texture paths should all be relative
* [x] Texture "Plane" object is default dimensions
* [x] Slug naming convention
* [x] Warning if file has unsaved changes
* [x] Object origin is not (0,0,0)
* [x] Only one scene and viewlayer
* [x] Make sure units are in meters
* [x] Warn if shapekeys exist which may cause issues for gltf export
* [ ] Main collection is visible and renderable

Tools:

* [ ] Test FBX export
* [x] Export GLTF
* [x] Clean file of unused datablocks, including fake-user ones
* [x] Make image datablock names match their file names
* [ ] Make mesh datablock name match object name

Misc:

* [x] Pre-save handler to set viewport shading solid
