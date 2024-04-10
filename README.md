# HAT
Haven Asset Tester - A Blender add-on we use for asset QC

## How to install:

### Option 1: With easy updates

1. Check if you have `git` installed already by opening a command prompt and running `git --version`.
2. If that gives you an error like *"'git' is not recognized as an internal or external command..."*, then [install git](https://git-scm.com/download/win).
3. Go to this folder in explorer: `%appdata%\Blender Foundation\Blender\x.x\scripts\addons` (where `x.x` is your current Blender version).
4. Click in the address bar, type `cmd`, and press enter. This opens a command prompt in that folder.
5. Run `git clone https://github.com/Poly-Haven/HAT.git`
6. Open Blender and enable the add-on.

### Option 2: Manual download

1. [Download this](https://github.com/Poly-Haven/HAT/archive/refs/heads/main.zip).
2. Install it inside Blender's Preferences.
3. If you get a big error that ends with *"ModuleNotFoundError: No module named 'HAT'"*, simply rename the `HAT-main` folder in `%appdata%\Blender Foundation\Blender\x.x\scripts\addons` to just `HAT` and restart Blender.

## How to update to new versions:

(assuming you used Option 1 above)

1. Close Blender.
2. Double click on `_UPDATE.bat` in `%appdata%\Blender Foundation\Blender\x.x\scripts\addons\HAT`.
3. Restart Blender.

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
* [ ] Only one scene and viewlayer
* [ ] Make sure units are in meters
* [ ] Warn if shapekeys exist which may cause issues for gltf export
* [ ] Main collection is visible and renderable

Tools:

* [ ] Test FBX export
* [x] Export GLTF
* [x] Clean file of unused datablocks, including fake-user ones
* [x] Make image datablock names match their file names
* [ ] Make mesh datablock name match object name

Misc:

* [x] Pre-save handler to set viewport shading solid
