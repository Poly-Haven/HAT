import bpy
import os
from bpy.props import StringProperty
from bpy.types import Operator
from ..utils.filename_utils import get_slug
from ..utils.fetch_textures import fetch_textures


def find_datablocks_with_slug(slug, max_depth=3):
    """Recursively find all datablocks that start with the slug"""
    affected_datablocks = []

    def search_datablock_container(container, container_name, depth=0):
        if depth > max_depth:
            return

        try:
            for item in container:
                if hasattr(item, "name") and item.name.startswith(slug):
                    affected_datablocks.append({"type": container_name, "name": item.name, "object": item})

                # Search nested containers
                if depth < max_depth:
                    for attr_name in dir(item):
                        if not attr_name.startswith("_"):
                            try:
                                attr = getattr(item, attr_name)
                                if hasattr(attr, "__iter__") and not isinstance(attr, (str, bytes)):
                                    search_datablock_container(attr, f"{container_name}.{attr_name}", depth + 1)
                            except Exception:
                                continue
        except Exception:
            pass

    # Search main data containers
    for data_type in dir(bpy.data):
        if not data_type.startswith("_"):
            try:
                container = getattr(bpy.data, data_type)
                if hasattr(container, "__iter__"):
                    search_datablock_container(container, data_type)
            except Exception:
                continue

    return affected_datablocks


def find_texture_files_with_slug(slug):
    """Find all texture files used in materials that start with the slug"""
    affected_files = []

    textures = fetch_textures()
    for texture in textures:
        if texture.filepath:
            # Get absolute path from Blender's filepath
            abs_filepath = bpy.path.abspath(texture.filepath)
            filename = os.path.basename(abs_filepath)

            if filename.startswith(slug):
                affected_files.append(abs_filepath)

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
    if not old_slug or not new_slug:
        return []

    actions = []

    # 1. Find blend file rename action
    blend_filepath = bpy.data.filepath
    if blend_filepath:
        blend_dir = os.path.dirname(blend_filepath)
        blend_filename = bpy.path.basename(blend_filepath)

        if blend_filename.startswith(old_slug):
            new_filename = new_slug + blend_filename[len(old_slug) :]
            new_blend_filepath = os.path.join(blend_dir, new_filename)
            actions.append({"type": "rename_blend_file", "old_path": blend_filepath, "new_path": new_blend_filepath})

    # 2. Find texture files to rename
    texture_files = find_texture_files_with_slug(old_slug)
    for filepath in texture_files:
        old_path, new_path = rename_image_file(filepath, old_slug, new_slug)
        if old_path != new_path:
            actions.append({"type": "rename_image_file", "old_path": old_path, "new_path": new_path})

    # 3. Find datablocks to rename
    datablocks = find_datablocks_with_slug(old_slug)
    for datablock_info in datablocks:
        old_name, new_name = rename_datablock(datablock_info, old_slug, new_slug)
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
                    bpy.ops.wm.save_as_mainfile(filepath=action["new_path"])
                elif action["type"] == "rename_image_file":
                    os.rename(action["old_path"], action["new_path"])
                    # Update image datablocks that reference this file
                    for img in bpy.data.images:
                        if img.filepath:
                            old_abs_path = os.path.abspath(bpy.path.abspath(img.filepath))
                            action_abs_path = os.path.abspath(action["old_path"])
                            if old_abs_path == action_abs_path:
                                img.filepath = action["new_path"]
                elif action["type"] == "rename_datablock":
                    # Already renamed in the preview phase
                    pass
            except Exception as e:
                print(f"Error executing action {action}: {e}")

    return actions


class HAT_OT_change_slug(Operator):
    bl_idname = "hat.change_slug"
    bl_label = "Change Asset Slug"
    bl_description = "Change the slug of the current asset (renames file, textures, and datablocks)"
    bl_options = {"REGISTER", "UNDO"}

    new_slug: StringProperty(name="New Slug", description="The new slug to use for this asset", default="")

    def invoke(self, context, event):
        # Get current slug from filename
        current_slug = get_slug()
        if current_slug:
            self.new_slug = current_slug

        # Show dialog to enter new slug
        return context.window_manager.invoke_props_dialog(self, width=400)

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
                for action in actions[:10]:  # Limit display to avoid UI overflow
                    if action["type"] == "rename_blend_file":
                        old_name = os.path.basename(action["old_path"])
                        new_name = os.path.basename(action["new_path"])
                        box.label(text=f"Rename file: {old_name} → {new_name}")
                    elif action["type"] == "rename_image_file":
                        old_name = os.path.basename(action["old_path"])
                        new_name = os.path.basename(action["new_path"])
                        box.label(text=f"Rename texture: {old_name} → {new_name}")
                    elif action["type"] == "rename_datablock":
                        datablock_type = action["datablock_type"]
                        old_name = action["old_name"]
                        new_name = action["new_name"]
                        box.label(text=f"Rename {datablock_type}: {old_name} → {new_name}")

                if len(actions) > 10:
                    box.label(text=f"... and {len(actions) - 10} more actions")

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
