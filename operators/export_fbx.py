import bpy
import os
from ..utils.filename_utils import get_slug


class HAT_OT_export_fbx(bpy.types.Operator):
    bl_idname = "hat.export_fbx"
    bl_label = "Export FBX"
    bl_description = "Export this asset as a FBX file as standard for uploading to polyhaven.com"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved and context.window_manager.hat_props.asset_type == "model"

    def execute(cls, context):
        slug = get_slug()
        to_file = os.path.join(os.path.dirname(bpy.data.filepath), slug + ".fbx")

        try:
            collection = bpy.data.collections[slug]
        except KeyError:
            cls.report({"ERROR"}, "No collection named " + slug)
            return {"CANCELLED"}

        for o in bpy.data.objects:
            o.select_set(o in list(collection.objects))

        # Correct and collect image file paths
        for img in bpy.data.images:
            if img.filepath.lower().startswith("//textures"):
                print("INCLUDE_FILE:", img.filepath[2:].replace("\\", "/"))
                img.filepath = os.path.join(os.path.dirname(to_file), img.filepath[len("//") :]).replace("\\", "/")

        # Export FBX
        bpy.ops.export_scene.fbx(
            filepath=to_file,
            path_mode="RELATIVE",
            check_existing=False,
            use_selection=True,
        )

        return {"FINISHED"}
