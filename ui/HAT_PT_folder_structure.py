import bpy
import fnmatch
from pathlib import Path
from ..utils.filename_utils import get_slug, remove_num, get_map_name
from ..utils.standard_map_names import names as standard_map_names
from .. import icons


class HAT_PT_folder_structure(bpy.types.Panel):
    bl_label = "Folder Structure"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.filepath)

    def draw_folder(self, layout, slug, folder_path, depth, required, valid, ignored):
        """
        Recursively draw folder structure with file/folder validation
        """
        if depth >= 6:  # Limit recursion depth
            return

        folder_path = Path(folder_path)
        if folder_path.is_file():
            folder_path = folder_path.parent

        if not folder_path.exists():
            return

        # Get current folder name for pattern matching
        current_folder = "/" if depth == 0 else folder_path.name

        # Get icons
        i = icons.get_icons()

        # Get items in current folder
        try:
            items = list(folder_path.iterdir())
        except (PermissionError, OSError):
            return

        # Separate files and folders, sort alphabetically (case-insensitive)
        folders = [item for item in items if item.is_dir()]
        files = [item for item in items if item.is_file()]
        folders.sort(key=lambda x: x.name.lower())
        files.sort(key=lambda x: x.name.lower())

        # Process all items (folders first, then files)
        all_items = folders + files

        # Track which required items we've found
        found_required = set()

        for item in all_items:
            item_name = item.name

            # Check if item should be ignored
            if self._should_ignore(item_name, ignored):
                continue

            # Add indentation based on depth
            row = layout.row(align=True)
            for _ in range(depth):
                row.label(text="", icon="BLANK1")

            # Determine item status
            is_folder = item.is_dir()
            status = self._get_item_status(item_name, current_folder, required, valid, slug, is_folder)

            # Track found required items
            if status == "required":
                found_required.add(self._normalize_pattern(item_name, slug))

            # Draw the item
            if is_folder:
                row.label(text=item_name, icon="FILE_FOLDER")
                if status == "required":
                    row.label(text="", icon="CHECKMARK")
                elif status == "valid":
                    row.label(text="", icon="CHECKMARK")
                elif status == "invalid":
                    row.label(text="", icon_value=i["exclamation-triangle"].icon_id)

                # Recursively draw folder contents
                self.draw_folder(layout, slug, item, depth + 1, required, valid, ignored)
            else:
                file_icon = self._get_file_icon(item_name)
                row.label(text=item_name, icon=file_icon)
                if status == "required":
                    row.label(text="", icon="CHECKMARK")
                elif status == "valid":
                    row.label(text="", icon="CHECKMARK")
                elif status == "invalid":
                    row.label(text="", icon_value=i["exclamation-triangle"].icon_id)
                elif status == "unknown":
                    row.label(text="", icon_value=i["question"].icon_id)

        # Check for missing required items (files)
        if current_folder in required:
            required_patterns = required[current_folder]
            for pattern in required_patterns:
                # Replace slug placeholder
                actual_pattern = pattern.replace("slug", slug)

                # Check if this required pattern was found
                pattern_found = False
                for item in all_items:
                    if not self._should_ignore(item.name, ignored):
                        item_name = item.name
                        if current_folder == "textures":
                            basename, ext = Path(item_name).stem, Path(item_name).suffix
                            item_name = remove_num(basename) + ext
                        if fnmatch.fnmatch(item_name.lower(), actual_pattern.lower()):
                            pattern_found = True
                            break

                if not pattern_found:
                    # Show missing required item
                    row = layout.row()
                    for _ in range(depth):
                        row.label(text="", icon="BLANK1")
                    row.label(text=f"Missing: {actual_pattern}", icon_value=i["exclamation-triangle"].icon_id)

        # Check for missing required folders (only at root level)
        if depth == 0:
            for folder_name in required.keys():
                if folder_name != "/":  # Skip root folder
                    folder_exists = any(item.is_dir() and item.name == folder_name for item in all_items)
                    if not folder_exists:
                        row = layout.row()
                        row.label(text=f"Missing: {folder_name} folder", icon_value=i["exclamation-triangle"].icon_id)

    def _get_file_icon(self, filename):
        """Get appropriate icon based on file extension"""
        ext = Path(filename).suffix.lower()

        # Image files
        if ext in [".png", ".jpg", ".jpeg", ".tiff", ".tga", ".exr", ".hdr"]:
            return "IMAGE_DATA"
        # Blender files
        elif ext == ".blend":
            return "BLENDER"
        # 3D model files
        elif ext in [".gltf", ".glb", ".fbx", ".obj", ".bin"]:
            return "MESH_DATA"
        # Text files
        elif ext in [".txt", ".json", ".md"]:
            return "TEXT"
        else:
            return "FILE"

    def _should_ignore(self, item_name, ignored_patterns):
        """Check if an item should be ignored based on patterns"""
        for pattern in ignored_patterns:
            if fnmatch.fnmatch(item_name.lower(), pattern.lower()):
                return True
        return False

    def _get_item_status(self, item_name, current_folder, required, valid, slug, is_folder=False):
        """Determine if an item is required, valid, or invalid"""
        # For folders, check if the folder name exists as a key in required or valid
        if is_folder:
            # Check if this folder is required
            if item_name in required:
                return "required"
            # Check if this folder is valid
            if item_name in valid:
                return "valid"
            # For root level, folders not in required/valid are invalid
            if current_folder == "/":
                return "invalid"
            # For subfolders, they are valid by default (contents will be checked recursively)
            return "valid"

        # For files, check patterns in the current folder
        # Check required patterns for current folder
        if current_folder in required:
            for pattern in required[current_folder]:
                actual_pattern = pattern.replace("slug", slug)
                if current_folder == "textures":
                    basename, ext = Path(item_name).stem, Path(item_name).suffix
                    item_name = remove_num(basename) + ext
                if fnmatch.fnmatch(item_name.lower(), actual_pattern.lower()):
                    return "required"

        # Flag unknown map types
        if current_folder == "textures":
            map_name = get_map_name(
                item_name, slug, strict=bpy.context.window_manager.hat_props.asset_type == "texture"
            )
            if map_name not in standard_map_names:
                return "unknown"

        # Check valid patterns for current folder
        if current_folder in valid:
            for pattern in valid[current_folder]:
                actual_pattern = pattern.replace("slug", slug)
                if fnmatch.fnmatch(item_name.lower(), actual_pattern.lower()):
                    return "valid"

        return "invalid"

    def _normalize_pattern(self, item_name, slug):
        """Normalize an item name for comparison with patterns"""
        return item_name.lower()

    def draw(self, context):
        props = context.window_manager.hat_props
        slug = get_slug()

        valid_root_common = [
            "*.blend",
            "*.gltf",
            "*.bin",
            "*.txt",
            "*.files.json",
            "*.obj",
            "*.mtl",
            "*.fbx",
            "*.ply",
        ]

        required = {  # These *must* be present
            "texture": {
                "/": [
                    "slug.blend",
                ],
                "textures": [
                    "slug_diff.png",
                    "slug_rough.png",
                    "slug_nor_gl.png",
                ],
                "renders": [
                    "primary.png",
                    "thumbnail.png",
                    "clay.png",
                ],
                "references": [
                    "chart.*",
                    "ref_*.*",
                    "spec_*.*",
                    "comparison_*.*",
                    "comparison.blend",
                ],
            },
            "model": {
                "/": [
                    "slug.blend",
                ],
                "textures": [
                    "slug_*.png",
                ],
                "renders": [
                    "primary.png",
                    "thumbnail.png",
                    "clay.png",
                    "orth_front.png",
                    "orth_side.png",
                    "orth_top.png",
                ],
            },
        }
        valid = {  # These can be present, but are not required
            "texture": {
                "/": valid_root_common,
                "textures": [
                    "slug_*.png",
                ],
                "renders": [
                    "*.png",
                ],
                "references": [
                    "*.*",
                ],
            },
            "model": {
                "/": valid_root_common,
                "renders": [
                    "*.png",
                ],
                "references": [
                    "*.*",
                ],
            },
        }
        ignored = [  # These are hidden
            "_upload",
            "*.blend1",
            "*.blend2",
            "nosubsurf.blend",
            "desktop.ini",
            ".DS_Store",
            "Thumbs.db",
        ]

        self.draw_folder(
            self.layout.column(align=True),
            slug,
            bpy.data.filepath,
            0,
            required[props.asset_type],
            valid[props.asset_type],
            ignored,
        )
