import importlib
import os
import sys
from ..utils import dpi_factor
from .. import icons

check_list = (os.path.splitext(f)[0] for f in os.listdir(
    os.path.join(os.path.dirname(__file__), 'checks')) if f.endswith('.py'))

checks = {}
for c in check_list:
    if "bpy" not in locals():
        m = importlib.import_module('.' + c, 'HAT.operators.checks')
    else:
        m = sys.modules['HAT.operators.checks.' + c]
        importlib.reload(m)
    checks[c] = m

import bpy


class HAT_OT_check(bpy.types.Operator):
    bl_idname = "hat.check"
    bl_label = "Test results:"
    bl_description = "Run all checks"

    tests = []  # [["STATUS", [messages]]]

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def draw(self, context):
        i = icons.get_icons()
        status_icon_custom = {
            'ERROR': 'x-circle-fill',
            'WARNING': 'exclamation-triangle',
        }
        status_icon = {
            'SUCCESS': 'CHECKMARK',
        }
        col = self.layout.column(align=True)
        for status, messages in self.tests:
            for message in messages:
                if status in status_icon_custom:
                    col.label(text=message,
                              icon_value=i[status_icon_custom[status]].icon_id)
                else:
                    col.label(text=message, icon=status_icon[status])

    def invoke(self, context, event):
        self.tests = []  # Reset after rerun

        slug = bpy.path.display_name_from_filepath(bpy.data.filepath)

        for c in checks.values():
            self.tests.append(c.check(slug))

        return context.window_manager.invoke_props_dialog(self, width=300 * dpi_factor.dpi_factor())

    def execute(self, context):
        return {'FINISHED'}
