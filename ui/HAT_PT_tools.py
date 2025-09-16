import bpy
from ..operators import change_slug
from ..operators import scrub_datablocks
from ..operators import fix_img_db_name
from ..operators import open_folder
from ..operators import export_gltf


class HAT_PT_tools(bpy.types.Panel):
    bl_label = "Tools"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    def draw(self, context):
        props = context.window_manager.hat_props
        col = self.layout.column()
        col.operator(change_slug.HAT_OT_change_slug.bl_idname, icon="OUTLINER_OB_FONT")

        col.separator()
        col.operator(scrub_datablocks.HAT_OT_scrub_datablocks.bl_idname, icon="TRASH")
        col.operator(fix_img_db_name.HAT_OT_fix_img_db_name.bl_idname, icon="COPY_ID")

        col.separator()
        col.operator(open_folder.HAT_OT_open_folder.bl_idname, icon="FILE_FOLDER")

        col.separator()

        col.operator(
            export_gltf.HAT_OT_export_gltf.bl_idname,
            text=f"Export {props.asset_type} GLTF",
            icon="FILE",
        )
