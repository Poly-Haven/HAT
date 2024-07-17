import importlib
import os
import sys
from ..utils import dpi_factor
from .. import icons

check_list = (
    os.path.splitext(f)[0] for f in os.listdir(os.path.join(os.path.dirname(__file__), "checks")) if f.endswith(".py")
)

checks = {}
for c in check_list:
    if "bpy" not in locals():
        m = importlib.import_module("." + c, "HAT.operators.checks")
    else:
        m = sys.modules["HAT.operators.checks." + c]
        importlib.reload(m)
    checks[c] = m

import bpy


class HAT_OT_check(bpy.types.Operator):
    bl_idname = "hat.check"
    bl_label = "Test results:"
    bl_description = "Run all checks"

    on_save: bpy.props.BoolProperty(default=False)

    tests = []  # [["STATUS", [messages]]]

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def draw(self, context):
        i = icons.get_icons()
        status_icon_custom = {
            "ERROR": "x-circle-fill",
            "WARNING": "exclamation-triangle",
            "QUESTION": "question",
        }
        status_icon = {
            "SUCCESS": "CHECKMARK",
        }
        col = self.layout.column(align=True)
        for status, messages in self.tests:
            if status == "SUCCESS" and self.on_save:
                continue
            for message in messages:
                if status in status_icon_custom:
                    col.label(text=message, icon_value=i[status_icon_custom[status]].icon_id)
                else:
                    col.label(text=message, icon=status_icon[status])
        if self.on_save:
            row = col.row()
            row.alignment = "RIGHT"
            row.prop(
                context.scene.hat_props,
                "test_on_save",
                icon="CHECKBOX_HLT" if context.scene.hat_props.test_on_save else "CHECKBOX_DEHLT",
                toggle=True,
            )

    def invoke(self, context, event):
        self.tests = []  # Reset after rerun
        context.scene.hat_props.test_on_save = True

        slug = bpy.path.display_name_from_filepath(bpy.data.filepath)

        for check_name, check in checks.items():
            if self.on_save and check_name == "unsaved":
                # No need to check for unsaved changes while we're busy saving.
                continue
            self.tests.append(check.check(slug))

        if self.on_save:
            failed_tests = list((t for t in self.tests if t[0] != "SUCCESS"))
            if len(failed_tests) == 0:
                # No problems, no popup.
                return {"FINISHED"}

        return context.window_manager.invoke_props_dialog(self, width=round(350 * dpi_factor.dpi_factor()))

    def execute(self, context):
        return {"FINISHED"}
