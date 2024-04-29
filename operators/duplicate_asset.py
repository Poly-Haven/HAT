import bpy
from pathlib import Path


def btn_draw(self, context):
    lib_ref = getattr(context.space_data.params, "asset_library_reference", "")
    if lib_ref == "LOCAL":
        layout = self.layout
        layout.separator()
        layout.operator("hat.duplicate_asset", icon="DUPLICATE")


class HAT_OT_duplicate_asset(bpy.types.Operator):
    bl_idname = "hat.duplicate_asset"
    bl_label = "Duplicate this Asset"
    bl_description = (
        "Copies the current asset and makes an identical duplicate, mainly to help with adding to multiple catalogs"
    )
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        slug = context.space_data.params.filename
        slug = slug.split("\\")[-1]  # Starts with Object\\slug
        slug = slug.split(".")[0]  # Remove .001, .002, etc if it exists
        if slug not in bpy.data.objects:
            self.report({"ERROR"}, f"Object {slug} not found")
        obj = bpy.data.objects[slug]
        new_obj = obj.copy()
        bpy.context.collection.objects.link(new_obj)
        new_obj.asset_mark()

        # Set thumbnail
        override = bpy.context.copy()
        override["id"] = new_obj
        with bpy.context.temp_override(**override):
            thumbnail_file = Path("C:/Users/gregz/Poly Haven Dropbox/Work/Greg/recategorize models/thumbs") / (
                slug + ".webp"
            )
            bpy.ops.ed.lib_id_load_custom_preview(filepath=str(thumbnail_file))

        # Copy tags
        for t in obj.asset_data.tags:
            new_obj.asset_data.tags.new(t.name, skip_if_exists=True)

        # Copy catalog
        cat_id = obj.asset_data.catalog_id
        new_obj.asset_data.catalog_id = cat_id

        self.report({"INFO"}, f"Duplicated {slug}")
        return {"FINISHED"}
