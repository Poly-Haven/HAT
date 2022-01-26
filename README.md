# HAT
Haven Asset Tester - A Blender add-on we use for asset QC

## Features / to do:

Checks:

* [x] Check maps use Non-color Data when required
* [x] Check if vertex colors exist (will screw up gltf export)
* [x] Unit Scale is 1.0
* [x] Warning if scale is not applied
* [x] Collection name should be same as slug (file name)
* [x] Texture file names should start with slug
* [x] Texture datablock should match file name
* [x] Texture map names should be standardized
* [x] No packed texture files
* [x] Material names should match or start with slug
* [x] Texture paths should all be relative
* [x] Texture "Plane" object is default dimensions
* [x] Slug naming convention
* [x] Warning if file has unsaved changes
* [x] Object origin is not (0,0,0)

Tools:

* [ ] Test FBX export
* [x] Export GLTF
* [x] Clean file of unused datablocks, including fake-user ones
* [ ] Measure real world scale of textures

Misc:

* [x] Pre-save handler to set viewport shading solid
