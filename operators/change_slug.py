import bpy
import time
from bpy.props import StringProperty
from bpy.types import Operator
from pathlib import Path
from ..utils.filename_utils import get_slug
from .. import icons


def find_datablocks_with_slug(slug, max_depth=3):
    """Find all datablocks that start with the slug - generic future-proof version"""
    print(f"DEBUG: Starting search for datablocks with slug: '{slug}'")
    start_time = time.time()
    max_search_time = 10.0  # Maximum 10 seconds to prevent hanging
    affected_datablocks = []

    # Dynamically discover all data types in bpy.data that are iterable containers
    # This approach is future-proof and doesn't hardcode specific types
    discovered_data_types = []

    for attr_name in dir(bpy.data):
        # Skip private attributes and known non-data attributes
        skip_attrs = [
            "bl_rna",
            "rna_type",
            "is_dirty",
            "is_saved",
            "use_autopack",
            "filepath",
            "version",
            "is_library_dirty",  # Known non-iterable data attributes
        ]
        if attr_name.startswith("_") or attr_name in skip_attrs:
            continue

        try:
            attr_value = getattr(bpy.data, attr_name)
            # Check if it's an iterable container (but not string/bytes)
            if (
                hasattr(attr_value, "__iter__")
                and not isinstance(attr_value, (str, bytes))
                and not callable(attr_value)
            ):
                discovered_data_types.append(attr_name)
        except (AttributeError, TypeError):
            continue

    print(f"DEBUG: Discovered {len(discovered_data_types)} data types: {discovered_data_types}")

    for data_type in discovered_data_types:
        # Check time limit
        if time.time() - start_time > max_search_time:
            print(f"DEBUG: Time limit exceeded ({max_search_time}s), stopping search")
            break

        try:
            container = getattr(bpy.data, data_type)
            print(f"DEBUG: Searching bpy.data.{data_type}")

            # Additional safety check - make sure container is actually iterable and has items
            if not hasattr(container, "__iter__"):
                continue

            # Check if container has length - if it's empty, skip it
            try:
                container_len = len(container)
                if container_len == 0:
                    continue
                print(f"DEBUG: {data_type} has {container_len} items")
            except (TypeError, AttributeError):
                # Some containers might not support len(), that's ok
                pass

            # Safety limits to prevent infinite loops
            item_count = 0
            max_items_per_container = 10000  # Reasonable limit for even large scenes

            try:
                for item in container:
                    item_count += 1
                    if item_count > max_items_per_container:
                        print(f"DEBUG: Hit safety limit of {max_items_per_container} items in {data_type}")
                        break

                    # Additional time check inside loop for very large containers
                    if item_count % 1000 == 0 and time.time() - start_time > max_search_time:
                        print(f"DEBUG: Time limit exceeded during {data_type} search")
                        break

                    # Check if item has a name attribute and starts with slug
                    if hasattr(item, "name") and hasattr(item.name, "startswith"):
                        try:
                            if item.name.startswith(slug):
                                print(f"DEBUG: Found datablock: {data_type}.{item.name}")
                                affected_datablocks.append({"type": data_type, "name": item.name, "object": item})
                        except (AttributeError, TypeError):
                            # Some objects might have non-string names or other issues
                            continue

            except (TypeError, AttributeError):
                # Container might not be properly iterable
                print(f"DEBUG: Container {data_type} is not properly iterable")
                continue

        except Exception as e:
            print(f"DEBUG: Error accessing bpy.data.{data_type}: {e}")
            continue

    elapsed_time = time.time() - start_time
    print(
        f"DEBUG: Search completed in {elapsed_time:.2f}s. "
        f"Found {len(affected_datablocks)} datablocks with slug '{slug}'"
    )
    return affected_datablocks


def find_texture_files_with_slug(slug):
    """Find all texture files in the textures folder that start with the slug"""
    print(f"DEBUG: Finding texture files with slug '{slug}'")
    affected_files = []

    blend_filepath = bpy.data.filepath
    if not blend_filepath:
        print("DEBUG: No blend file path available")
        return affected_files

    # Look for textures folder next to the blend file
    blend_path = Path(blend_filepath)
    textures_dir = blend_path.parent / "textures"

    if not textures_dir.exists():
        print(f"DEBUG: No textures folder found at {textures_dir}")
        return affected_files

    if not textures_dir.is_dir():
        print(f"DEBUG: {textures_dir} exists but is not a directory")
        return affected_files

    print(f"DEBUG: Searching textures folder: {textures_dir}")

    try:
        for filepath in textures_dir.iterdir():
            # Only process files (not subdirectories)
            if filepath.is_file() and filepath.name.startswith(slug):
                print(f"DEBUG: Found matching texture file: {filepath.name}")
                affected_files.append(str(filepath))

    except Exception as e:
        print(f"DEBUG: Error reading textures directory: {e}")

    print(f"DEBUG: Found {len(affected_files)} texture files with slug '{slug}'")
    return affected_files


def rename_datablock(datablock_info, old_slug, new_slug):
    """Rename a datablock by replacing the old slug with new slug"""
    datablock = datablock_info["object"]
    old_name = datablock.name

    if old_name.startswith(old_slug):
        if old_name == old_slug:
            new_name = new_slug
        else:
            new_name = new_slug + old_name[len(old_slug) :]
        datablock.name = new_name
        return old_name, new_name

    return old_name, old_name


def rename_image_file(filepath, old_slug, new_slug):
    """Rename an image file by replacing the old slug with new slug"""
    filepath = Path(filepath)
    filename = filepath.name

    if filename.startswith(old_slug):
        if filename == old_slug:
            new_filename = new_slug
        else:
            new_filename = new_slug + filename[len(old_slug) :]
        new_filepath = filepath.parent / new_filename
        return str(filepath), str(new_filepath)

    return str(filepath), str(filepath)


def change_texture_slug(cls, old_slug, new_slug, dry_run=False):
    """Change the asset slug, in all locations where it is necessary"""
    print(f"DEBUG: change_texture_slug called with old_slug='{old_slug}', new_slug='{new_slug}', dry_run={dry_run}")

    if not old_slug or not new_slug:
        print("DEBUG: Empty slug provided, returning empty actions")
        return []

    actions = []

    # 1. Find texture files to rename
    print("DEBUG: Step 1 - Finding texture files")
    texture_files = find_texture_files_with_slug(old_slug)
    for filepath in texture_files:
        old_path, new_path = rename_image_file(filepath, old_slug, new_slug)
        if old_path != new_path:
            print(f"DEBUG: Will rename texture: {Path(old_path).name} -> {Path(new_path).name}")

            # Check if target file already exists during dry run
            has_conflict = dry_run and Path(new_path).exists()
            if has_conflict:
                print(f"DEBUG: WARNING - Target file already exists: {new_path}")

            actions.append(
                {"type": "rename_image_file", "old_path": old_path, "new_path": new_path, "has_conflict": has_conflict}
            )

    # 2. Find datablocks to rename
    print(f"DEBUG: Step 2 - Finding datablocks with slug '{old_slug}'")

    # TEMPORARY: Disable datablock search to test if this is causing the freeze
    # Uncomment the line below to re-enable datablock search
    datablocks = find_datablocks_with_slug(old_slug)
    # datablocks = []  # Disable datablock search temporarily

    print(f"DEBUG: Found {len(datablocks)} datablocks")

    for datablock_info in datablocks:
        old_name = datablock_info["name"]

        # Calculate what the new name would be WITHOUT actually renaming during dry run
        if old_name.startswith(old_slug):
            if old_name == old_slug:
                new_name = new_slug
            else:
                new_name = new_slug + old_name[len(old_slug) :]

            if old_name != new_name:
                # Check for naming conflicts during dry run
                has_conflict = False
                if dry_run:
                    # Check if a datablock with the new name already exists in the same collection
                    container = getattr(bpy.data, datablock_info["type"])
                    has_conflict = new_name in container
                    if has_conflict:
                        print(f"DEBUG: WARNING - Datablock name conflict: {datablock_info['type']}.{new_name} exists")

                actions.append(
                    {
                        "type": "rename_datablock",
                        "datablock_type": datablock_info["type"],
                        "old_name": old_name,
                        "new_name": new_name,
                        "object": datablock_info["object"],
                        "has_conflict": has_conflict,
                    }
                )

    # 3. Find blend file and parent folder rename actions (done last)
    print("DEBUG: Step 3 - Checking blend file and parent folder")
    blend_filepath = bpy.data.filepath
    if blend_filepath:
        blend_path = Path(blend_filepath)
        blend_filename = blend_path.name
        print(f"DEBUG: Blend filename: {blend_filename}")

        if blend_filename.startswith(old_slug):
            new_filename = new_slug + blend_filename[len(old_slug) :]
            new_blend_filepath = blend_path.parent / new_filename

            # Create backup filename (same as new file but with .blend1 extension)
            backup_filename = new_slug + blend_filename[len(old_slug) :].replace(".blend", ".blend1")
            backup_filepath = blend_path.parent / backup_filename

            print(f"DEBUG: Will rename blend file: {blend_filename} -> {new_filename}")
            print(f"DEBUG: Will create backup: {blend_filename} -> {backup_filename}")

            # Check for conflicts during dry run
            blend_conflict = dry_run and new_blend_filepath.exists()
            backup_conflict = dry_run and backup_filepath.exists()

            if blend_conflict:
                print(f"DEBUG: WARNING - Target blend file already exists: {new_blend_filepath}")
            if backup_conflict:
                print(f"DEBUG: WARNING - Backup file already exists: {backup_filepath}")

            actions.append(
                {
                    "type": "rename_blend_file",
                    "old_path": str(blend_path),
                    "new_path": str(new_blend_filepath),
                    "backup_path": str(backup_filepath),
                    "has_conflict": blend_conflict or backup_conflict,
                }
            )

        # Check if parent folder should be renamed
        parent_dir = blend_path.parent.parent
        current_folder_name = blend_path.parent.name
        print(f"DEBUG: Current folder name: {current_folder_name}")

        if current_folder_name == old_slug:
            new_folder_name = new_slug
            new_folder_path = parent_dir / new_folder_name
            print(f"DEBUG: Will rename parent folder: {current_folder_name} -> {new_folder_name}")

            # Check for conflicts during dry run
            folder_conflict = dry_run and new_folder_path.exists()
            if folder_conflict:
                print(f"DEBUG: WARNING - Target folder already exists: {new_folder_path}")

            actions.append(
                {
                    "type": "rename_parent_folder",
                    "old_path": str(blend_path.parent),
                    "new_path": str(new_folder_path),
                    "has_conflict": folder_conflict,
                }
            )

    if not dry_run:
        # Execute the actions
        for action in actions:
            try:
                if action["type"] == "rename_blend_file":
                    # Create backup file first
                    old_path = Path(action["old_path"])
                    backup_path = Path(action["backup_path"])
                    new_path = Path(action["new_path"])

                    old_path.rename(backup_path)
                    print(f"DEBUG: Created backup: {backup_path.name}")
                    # Save as new filename
                    if "rename_parent_folder" not in [a["type"] for a in actions]:
                        bpy.ops.wm.save_as_mainfile(filepath=str(new_path), relative_remap=False)
                        print(f"DEBUG: Saved as: {new_path.name}")
                elif action["type"] == "rename_parent_folder":
                    try:
                        old_path = Path(action["old_path"])
                        new_path = Path(action["new_path"])
                        old_path.rename(new_path)
                        print(f"DEBUG: Renamed folder: {old_path.name} -> {new_path.name}")
                    except Exception as e:
                        print(f"DEBUG: Error renaming folder {action['old_path']} to {action['new_path']}: {e}")
                        cls.report({"ERROR"}, f"Failed to rename folder: {e}")
                        bpy.ops.wm.save_mainfile(relative_remap=False)  # Save without changing path
                        continue
                    bpy.ops.wm.save_as_mainfile(
                        filepath=str(new_path / f"{new_slug}.blend"),
                        relative_remap=False,
                    )
                    print(f"DEBUG: Saved as: {new_path.name}")
                elif action["type"] == "rename_image_file":
                    old_path = Path(action["old_path"])
                    new_path = Path(action["new_path"])
                    old_path.rename(new_path)
                    print(f"DEBUG: Renamed texture: {old_path.name} -> {new_path.name}")

                    # Update image datablocks that reference this file
                    # Use absolute paths for comparison but keep original path format
                    action_old_abs = old_path.resolve()

                    for img in bpy.data.images:
                        if img.filepath:
                            # Get absolute path of the image for comparison
                            img_abs_path = Path(bpy.path.abspath(img.filepath)).resolve()

                            if img_abs_path == action_old_abs:
                                # Update the filepath but keep the original format (relative/absolute)
                                # Get the directory part of the original filepath correctly
                                original_filepath = img.filepath

                                # Handle Blender's relative paths (starting with //)
                                if original_filepath.startswith("//"):
                                    # For relative paths, split on the last path separator
                                    if "\\" in original_filepath:
                                        img_dir = original_filepath.rsplit("\\", 1)[0]
                                    elif "/" in original_filepath:
                                        img_dir = original_filepath.rsplit("/", 1)[0]
                                    else:
                                        img_dir = "//"  # Just the relative prefix
                                else:
                                    # For absolute paths, use Path.parent
                                    img_dir = str(Path(original_filepath).parent)

                                new_basename = new_path.name

                                if img_dir and img_dir != "//":
                                    # Use forward slashes for consistency with Blender paths
                                    if original_filepath.startswith("//"):
                                        img.filepath = img_dir + "/" + new_basename
                                    else:
                                        img.filepath = str(Path(img_dir) / new_basename)
                                else:
                                    img.filepath = new_basename

                                print(f"DEBUG: Updated image datablock filepath: {img.name} -> {img.filepath}")
                elif action["type"] == "rename_datablock":
                    # Actually rename the datablock during execution
                    datablock = action["object"]
                    datablock.name = action["new_name"]
                    print(f"DEBUG: Renamed datablock {action['old_name']} -> {action['new_name']}")
            except Exception as e:
                print(f"DEBUG: Error executing action {action}: {e}")
                cls.report({"ERROR"}, f"Failed to execute action: {e}")

    print(f"DEBUG: change_texture_slug completed. Total actions: {len(actions)}")
    return actions


class HAT_OT_change_slug(Operator):
    bl_idname = "hat.change_slug"
    bl_label = "Change Asset Slug"
    bl_description = (
        "Change the slug of the current asset (renames file, textures, and datablocks). " "Requires saved file"
    )
    bl_options = {"REGISTER", "UNDO"}

    new_slug: StringProperty(name="New Slug", description="The new slug to use for this asset", default="")

    @classmethod
    def poll(cls, context):
        # Require the file to be saved (no unsaved changes)
        return not bpy.data.is_dirty and bpy.data.filepath != ""

    def invoke(self, context, event):
        # Get current slug from filename
        current_slug = get_slug()
        if current_slug:
            self.new_slug = current_slug

        # Show dialog to enter new slug
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "new_slug")

        # Show preview of actions
        current_slug = get_slug()
        if current_slug and self.new_slug and current_slug != self.new_slug:
            actions = change_texture_slug(self, current_slug, self.new_slug, dry_run=True)

            if actions:
                # Check if there are any conflicts
                has_any_conflicts = any(action.get("has_conflict", False) for action in actions)

                if has_any_conflicts:
                    layout.separator()
                    warning_box = layout.box()
                    warning_row = warning_box.row()
                    if "icons" in icons.preview_collections:
                        icon = icons.preview_collections["icons"]["exclamation-triangle"]
                        warning_text = "Warning: Some target files/folders already exist!"
                        warning_row.label(text=warning_text, icon_value=icon.icon_id)
                    else:
                        warning_row.label(text="⚠ Warning: Some target files/folders already exist!")

                layout.separator()
                layout.label(text="Actions to be performed:")

                box = layout.box()
                # Enable alignment for closer spacing
                col = box.column(align=True)

                display_limit = 30
                for action in actions[:display_limit]:  # Limit display to avoid UI overflow
                    if action["type"] == "rename_blend_file":
                        old_name = Path(action["old_path"]).name
                        new_name = Path(action["new_path"]).name
                        backup_name = Path(action["backup_path"]).name

                        # Show backup creation
                        row = col.row()
                        if action.get("has_conflict", False):
                            if "icons" in icons.preview_collections:
                                icon = icons.preview_collections["icons"]["exclamation-triangle"]
                                row.label(text=f"Create backup: {backup_name}", icon_value=icon.icon_id)
                            else:
                                row.label(text=f"⚠ Create backup: {backup_name}")
                        else:
                            row.label(text=f"Create backup: {backup_name}")

                        # Show file rename
                        row = col.row()
                        if action.get("has_conflict", False):
                            if "icons" in icons.preview_collections:
                                icon = icons.preview_collections["icons"]["exclamation-triangle"]
                                row.label(text=f"Rename file: {old_name} → {new_name}", icon_value=icon.icon_id)
                            else:
                                row.label(text=f"⚠ Rename file: {old_name} → {new_name}")
                        else:
                            row.label(text=f"Rename file: {old_name} → {new_name}")

                    elif action["type"] == "rename_parent_folder":
                        old_name = Path(action["old_path"]).name
                        new_name = Path(action["new_path"]).name
                        row = col.row()
                        if action.get("has_conflict", False):
                            if "icons" in icons.preview_collections:
                                icon = icons.preview_collections["icons"]["exclamation-triangle"]
                                row.label(text=f"Rename folder: {old_name} → {new_name}", icon_value=icon.icon_id)
                            else:
                                row.label(text=f"⚠ Rename folder: {old_name} → {new_name}")
                        else:
                            row.label(text=f"Rename folder: {old_name} → {new_name}")

                    elif action["type"] == "rename_image_file":
                        old_name = Path(action["old_path"]).name
                        new_name = Path(action["new_path"]).name
                        row = col.row()
                        if action.get("has_conflict", False):
                            if "icons" in icons.preview_collections:
                                icon = icons.preview_collections["icons"]["exclamation-triangle"]
                                row.label(text=f"Rename texture: {old_name} → {new_name}", icon_value=icon.icon_id)
                            else:
                                row.label(text=f"⚠ Rename texture: {old_name} → {new_name}")
                        else:
                            row.label(text=f"Rename texture: {old_name} → {new_name}")

                    elif action["type"] == "rename_datablock":
                        datablock_type = action["datablock_type"]
                        old_name = action["old_name"]
                        new_name = action["new_name"]
                        row = col.row()
                        if action.get("has_conflict", False):
                            if "icons" in icons.preview_collections:
                                icon = icons.preview_collections["icons"]["exclamation-triangle"]
                                text = f"Rename {datablock_type}: {old_name} → {new_name}"
                                row.label(text=text, icon_value=icon.icon_id)
                            else:
                                row.label(text=f"⚠ Rename {datablock_type}: {old_name} → {new_name}")
                        else:
                            row.label(text=f"Rename {datablock_type}: {old_name} → {new_name}")

                if len(actions) > display_limit:
                    col.label(text=f"... and {len(actions) - display_limit} more actions")

    def execute(self, context):
        current_slug = get_slug()

        if not current_slug:
            self.report({"ERROR"}, "Cannot determine current slug from filename")
            return {"CANCELLED"}

        if not self.new_slug:
            self.report({"ERROR"}, "New slug cannot be empty")
            return {"CANCELLED"}

        if current_slug == self.new_slug:
            self.report({"INFO"}, "New slug is the same as current slug")
            return {"FINISHED"}

        # Perform the slug change
        actions = change_texture_slug(self, current_slug, self.new_slug, dry_run=False)

        if actions:
            message = (
                f"Successfully changed slug from '{current_slug}' to "
                f"'{self.new_slug}' ({len(actions)} actions performed)"
            )
            self.report({"INFO"}, message)
        else:
            self.report({"WARNING"}, "No changes were necessary")

        return {"FINISHED"}
