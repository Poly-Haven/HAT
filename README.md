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
* [ ] Texture datablock should match file name
* [ ] Material names should start with slug
* [ ] Texture paths should all be relative
* [ ] "Sphere" object is default dimensions
* [ ] Slug naming convention
* [x] Warning if file has unsaved changes

Tools:

* [ ] Test FBX export
* [ ] Create GLTF button (fix common path issues automatically, and test)
* [ ] Clean file (remove unused datablocks, including force-saved ones (e.g. in case of incompatibly licensed node groups))

Misc:

* [x] Pre-save handler to set viewport shading solid
