import bpy
from ..operators import check
from .. import icons


class HAT_PT_main(bpy.types.Panel):

    bl_label = " "
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {"HEADER_LAYOUT_EXPAND", "DEFAULT_CLOSED"}

    def draw_header(self, context):
        i = icons.get_icons()
        props = context.window_manager.hat_props

        layout = self.layout
        row = layout.row()
        row.label(text="HAT", icon_value=i["polyhaven"].icon_id)
        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.prop(props, "asset_type", text="")
        sub.operator(check.HAT_OT_check.bl_idname, text="Check", icon="CHECKMARK").on_save = False
        row.separator()

    def draw(self, context):
        props = context.window_manager.hat_props

        col = self.layout.column(align=True)
        row = col.row()
        row.label(text="Click 'Check' above to run tests.")
        sub = row.row()
        sub.alignment = "RIGHT"
        sub.prop(props, "test_on_save", icon="CHECKBOX_HLT" if props.test_on_save else "CHECKBOX_DEHLT", toggle=True)
