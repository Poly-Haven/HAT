import bpy
from .. import addon_updater_ops
from ..operators import check
from .. import icons


class HAT_PT_main (bpy.types.Panel):

    bl_label = " "
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'output'
    bl_options = {'HEADER_LAYOUT_EXPAND', 'DEFAULT_CLOSED'}

    def draw_header(self, context):
        i = icons.get_icons()
        layout = self.layout
        row = layout.row()
        row.label(text="HAT", icon_value=i['polyhaven'].icon_id)
        sub = row.row()
        sub.alignment = 'RIGHT'
        sub.operator(check.HAT_OT_check.bl_idname,
                     text="Check", icon="CHECKMARK")
        row.separator()

    def draw(self, context):
        col = self.layout.column(align=True)
        col.label(text="Click 'Check' above to run tests.")
        col.separator()
        col.label(text="Check here occasionally for updates,")
        col.label(text="otherwise feel free to close this panel.")

        addon_updater_ops.check_for_update_background()
        addon_updater_ops.update_notice_box_ui(self, context)
