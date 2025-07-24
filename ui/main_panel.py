import bpy
import json
from ..operators import check
from ..operators import export_gltf
from ..operators import fix_img_db_name
from ..operators import scrub_datablocks
from ..utils.filename_utils import get_slug
from ..utils.draw_message_label import draw_message_label
from .. import icons


class HAT_PT_main(bpy.types.Panel):

    bl_label = " "
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {"HEADER_LAYOUT_EXPAND", "DEFAULT_CLOSED"}

    def draw_header(self, context):
        i = icons.get_icons()
        props = context.scene.hat_props

        layout = self.layout
        row = layout.row()
        row.label(text="HAT", icon_value=i["polyhaven"].icon_id)
        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.prop(props, "asset_type", text="")
        sub.operator(check.HAT_OT_check.bl_idname, text="Check", icon="CHECKMARK").on_save = False
        row.separator()

    def draw(self, context):
        props = context.scene.hat_props

        col = self.layout.column(align=True)
        row = col.row()
        row.label(text="Click 'Check' above to run tests.")
        sub = row.row()
        sub.alignment = "RIGHT"
        sub.prop(props, "test_on_save", icon="CHECKBOX_HLT" if props.test_on_save else "CHECKBOX_DEHLT", toggle=True)


class HAT_PT_results(bpy.types.Panel):
    bl_label = "Test Results"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    @classmethod
    def poll(self, context):
        return context.scene.hat_props.latest_tests != ""

    def draw(self, context):
        props = context.scene.hat_props
        col = self.layout.column()
        if props.latest_tests:
            try:
                tests = json.loads(props.latest_tests)
                for status, messages in tests:
                    for message in messages:
                        if message != "File contains unsaved changes":
                            draw_message_label(col, message, status)
            except json.JSONDecodeError:
                col.label(text="Failed to decode latest tests JSON.", icon="ERROR")


class HAT_PT_info(bpy.types.Panel):
    bl_label = "Info"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    def draw(self, context):
        col = self.layout.column()
        col.label(text=f"Detected Slug: {get_slug()}")


class HAT_PT_tools(bpy.types.Panel):
    bl_label = "Tools"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    def draw(self, context):
        props = context.scene.hat_props
        col = self.layout.column()
        col.operator(scrub_datablocks.HAT_OT_scrub_datablocks.bl_idname, icon="TRASH")
        col.operator(fix_img_db_name.HAT_OT_fix_img_db_name.bl_idname, icon="COPY_ID")

        col.separator()

        col = self.layout.column()
        col.operator(
            export_gltf.HAT_OT_export_gltf.bl_idname,
            text=f"Export {props.asset_type} GLTF",
            icon="FILE",
        )
