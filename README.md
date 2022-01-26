# HAT
Haven Asset Tester - A Blender add-on we use for asset QC

## How to install:

1. [Download this](https://github.com/Poly-Haven/HAT/archive/refs/heads/main.zip)
2. Install it inside Blender's Preferences.
3. If you get a big error that ends with *"ModuleNotFoundError: No module named 'HAT'"*, simply rename the `HAT-main` folder in `%appdata%\Blender Foundation\Blender\x.x\scripts\addons` to just `HAT` and restart Blender.

## How to update to new versions:

1. Close Blender.
2. Double click on `_UPDATE.bat` in `%appdata%\Blender Foundation\Blender\x.x\scripts\addons\HAT`.
3. If you're presented with an error like: *"'git' is not recognized as an internal or external command..."*, you need to first [install git](https://git-scm.com/download/win).
4. Restart Blender.

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
