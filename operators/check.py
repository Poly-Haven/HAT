import bpy
from ..utils import dpi_factor


class HAT_OT_check(bpy.types.Operator):
    bl_idname = "hat.check"
    bl_label = "Check"
    bl_description = "Run all checks"
    bl_options = {'UNDO'}

    tests = {}  # "test name": "status"

    def draw(self, context):
        status_icon = {
            'ERROR': 'CANCEL',
            'WARNING': 'ERROR',  # Blender's "error" icon is a warning triangle...?
            'SUCCESS': 'CHECKMARK',
        }
        col = self.layout.column(align=True)
        for label, status in self.tests.items():
            col.label(text=label, icon=status_icon[status])

    def invoke(self, context, event):
        print("INVOKE!")
        return context.window_manager.invoke_props_dialog(self, width=300 * dpi_factor.dpi_factor())

    def execute(self, context):
        return {'FINISHED'}
