import bpy
from .. import addon_updater_ops


class HAT_PT_main (bpy.types.Panel):

    bl_label = "HAT"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'output'

    def draw(self, context):
        addon_updater_ops.check_for_update_background()
        addon_updater_ops.update_notice_box_ui(self, context)

        layout = self.layout

        layout.label(text="Yes")
