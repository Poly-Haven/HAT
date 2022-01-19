import importlib
import bpy
import os
from ..utils import dpi_factor

check_list = (os.path.splitext(f)[0] for f in os.listdir(
    os.path.join(os.path.dirname(__file__), 'checks')) if f.endswith('.py'))

checks = {}
for c in check_list:
    m = importlib.import_module('.' + c, 'HAT.operators.checks')
    # TODO: Not great reloading immediately after import
    importlib.reload(m)
    checks[c] = m


class HAT_OT_check(bpy.types.Operator):
    bl_idname = "hat.check"
    bl_label = "Test results:"
    bl_description = "Run all checks"

    tests = []  # [["STATUS", [messages]]]

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def draw(self, context):
        # TODO: Use custom icons to make errors stand out.
        status_icon = {
            'ERROR': 'CANCEL',
            'WARNING': 'ERROR',  # Blender's "error" icon is a warning triangle...?
            'SUCCESS': 'CHECKMARK',
        }
        col = self.layout.column(align=True)
        for status, messages in self.tests:
            for message in messages:
                col.label(text=message, icon=status_icon[status])

    def invoke(self, context, event):
        self.tests = []  # Reset after rerun

        slug = bpy.path.display_name_from_filepath(bpy.data.filepath)

        for c in checks.values():
            self.tests.append(c.check(slug))

        return context.window_manager.invoke_props_dialog(self, width=300 * dpi_factor.dpi_factor())

    def execute(self, context):
        return {'FINISHED'}
