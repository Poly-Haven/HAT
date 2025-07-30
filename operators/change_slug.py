import bpy
import os
import time
from bpy.props import StringProperty
from bpy.types import Operator
from ..utils.filename_utils import get_slug


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
                print(f"DEBUG: {data_type} is not iterable, skipping")
                continue

            # Check if container has length - if it's empty, skip it
            try:
                container_len = len(container)
                if container_len == 0:
                    print(f"DEBUG: {data_type} is empty, skipping")
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
    blend_dir = os.path.dirname(blend_filepath)
    textures_dir = os.path.join(blend_dir, "textures")

    if not os.path.exists(textures_dir):
        print(f"DEBUG: No textures folder found at {textures_dir}")
        return affected_files

    if not os.path.isdir(textures_dir):
        print(f"DEBUG: {textures_dir} exists but is not a directory")
        return affected_files

    print(f"DEBUG: Searching textures folder: {textures_dir}")

    try:
        for filename in os.listdir(textures_dir):
            filepath = os.path.join(textures_dir, filename)

            # Only process files (not subdirectories)
            if os.path.isfile(filepath) and filename.startswith(slug):
                print(f"DEBUG: Found matching texture file: {filename}")
                affected_files.append(filepath)

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
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    if filename.startswith(old_slug):
        if filename == old_slug:
            new_filename = new_slug
        else:
            new_filename = new_slug + filename[len(old_slug) :]
        new_filepath = os.path.join(directory, new_filename)
        return filepath, new_filepath

    return filepath, filepath


def change_texture_slug(old_slug, new_slug, dry_run=False):
    """Change the asset slug, in all locations where it is necessary"""
    print(f"DEBUG: change_texture_slug called with old_slug='{old_slug}', new_slug='{new_slug}', dry_run={dry_run}")

    if not old_slug or not new_slug:
        print("DEBUG: Empty slug provided, returning empty actions")
        return []

    actions = []

    # 1. Find blend file and parent folder rename actions
    print("DEBUG: Step 1 - Checking blend file and parent folder")
    blend_filepath = bpy.data.filepath
    if blend_filepath:
        blend_dir = os.path.dirname(blend_filepath)
        blend_filename = bpy.path.basename(blend_filepath)
        print(f"DEBUG: Blend filename: {blend_filename}")

        if blend_filename.startswith(old_slug):
            new_filename = new_slug + blend_filename[len(old_slug) :]
            new_blend_filepath = os.path.join(blend_dir, new_filename)

            # Create backup filename (same as new file but with .blend1 extension)
            backup_filename = new_slug + blend_filename[len(old_slug) :].replace(".blend", ".blend1")
            backup_filepath = os.path.join(blend_dir, backup_filename)

            print(f"DEBUG: Will rename blend file: {blend_filename} -> {new_filename}")
            print(f"DEBUG: Will create backup: {blend_filename} -> {backup_filename}")

            actions.append(
                {
                    "type": "rename_blend_file",
                    "old_path": blend_filepath,
                    "new_path": new_blend_filepath,
                    "backup_path": backup_filepath,
                }
            )

        # Check if parent folder should be renamed
        parent_dir = os.path.dirname(blend_dir)
        current_folder_name = os.path.basename(blend_dir)
        print(f"DEBUG: Current folder name: {current_folder_name}")

        if current_folder_name == old_slug:
            new_folder_name = new_slug
            new_folder_path = os.path.join(parent_dir, new_folder_name)
            print(f"DEBUG: Will rename parent folder: {current_folder_name} -> {new_folder_name}")
            actions.append({"type": "rename_parent_folder", "old_path": blend_dir, "new_path": new_folder_path})

    # 2. Find texture files to rename
    print("DEBUG: Step 2 - Finding texture files")
    texture_files = find_texture_files_with_slug(old_slug)
    for filepath in texture_files:
        old_path, new_path = rename_image_file(filepath, old_slug, new_slug)
        if old_path != new_path:
            print(f"DEBUG: Will rename texture: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
            actions.append({"type": "rename_image_file", "old_path": old_path, "new_path": new_path})

    # 3. Find datablocks to rename
    print(f"DEBUG: Step 3 - Finding datablocks with slug '{old_slug}'")

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
                actions.append(
                    {
                        "type": "rename_datablock",
                        "datablock_type": datablock_info["type"],
                        "old_name": old_name,
                        "new_name": new_name,
                        "object": datablock_info["object"],
                    }
                )

    if not dry_run:
        # Execute the actions
        for action in actions:
            try:
                if action["type"] == "rename_blend_file":
                    # Create backup file first
                    os.rename(action["old_path"], action["backup_path"])
                    print(f"DEBUG: Created backup: {os.path.basename(action['backup_path'])}")
                    # Save as new filename
                    bpy.ops.wm.save_as_mainfile(filepath=action["new_path"])
                    print(f"DEBUG: Saved as: {os.path.basename(action['new_path'])}")
                elif action["type"] == "rename_parent_folder":
                    os.rename(action["old_path"], action["new_path"])
                    old_name = os.path.basename(action["old_path"])
                    new_name = os.path.basename(action["new_path"])
                    print(f"DEBUG: Renamed folder: {old_name} -> {new_name}")
                elif action["type"] == "rename_image_file":
                    os.rename(action["old_path"], action["new_path"])
                    old_name = os.path.basename(action["old_path"])
                    new_name = os.path.basename(action["new_path"])
                    print(f"DEBUG: Renamed texture: {old_name} -> {new_name}")
                    # Update image datablocks that reference this file (keep relative paths)
                    for img in bpy.data.images:
                        if img.filepath and img.filepath == action["old_path"]:
                            img.filepath = action["new_path"]
                elif action["type"] == "rename_datablock":
                    # Actually rename the datablock during execution
                    datablock = action["object"]
                    datablock.name = action["new_name"]
                    print(f"DEBUG: Renamed datablock {action['old_name']} -> {action['new_name']}")
            except Exception as e:
                print(f"DEBUG: Error executing action {action}: {e}")

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
            actions = change_texture_slug(current_slug, self.new_slug, dry_run=True)

            if actions:
                layout.separator()
                layout.label(text="Actions to be performed:")

                box = layout.box()
                # Enable alignment for closer spacing
                col = box.column(align=True)

                display_limit = 30
                for action in actions[:display_limit]:  # Limit display to avoid UI overflow
                    if action["type"] == "rename_blend_file":
                        old_name = os.path.basename(action["old_path"])
                        new_name = os.path.basename(action["new_path"])
                        backup_name = os.path.basename(action["backup_path"])
                        col.label(text=f"Create backup: {backup_name}")
                        col.label(text=f"Rename file: {old_name} → {new_name}")
                    elif action["type"] == "rename_parent_folder":
                        old_name = os.path.basename(action["old_path"])
                        new_name = os.path.basename(action["new_path"])
                        col.label(text=f"Rename folder: {old_name} → {new_name}")
                    elif action["type"] == "rename_image_file":
                        old_name = os.path.basename(action["old_path"])
                        new_name = os.path.basename(action["new_path"])
                        col.label(text=f"Rename texture: {old_name} → {new_name}")
                    elif action["type"] == "rename_datablock":
                        datablock_type = action["datablock_type"]
                        old_name = action["old_name"]
                        new_name = action["new_name"]
                        col.label(text=f"Rename {datablock_type}: {old_name} → {new_name}")

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
        actions = change_texture_slug(current_slug, self.new_slug, dry_run=False)

        if actions:
            message = (
                f"Successfully changed slug from '{current_slug}' to "
                f"'{self.new_slug}' ({len(actions)} actions performed)"
            )
            self.report({"INFO"}, message)
        else:
            self.report({"WARNING"}, "No changes were necessary")

        return {"FINISHED"}
