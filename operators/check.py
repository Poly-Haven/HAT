import importlib
import json
import os
import sys
from ..utils import dpi_factor
from ..utils.filename_utils import get_slug
from ..utils.draw_message_label import draw_message_label

check_list = (
    os.path.splitext(f)[0] for f in os.listdir(os.path.join(os.path.dirname(__file__), "checks")) if f.endswith(".py")
)

checks = {}
for c in check_list:
    if "bpy" not in locals():
        m = importlib.import_module(".checks." + c, __package__)
    else:
        m = sys.modules["bl_ext.user_default.polyhaven_hat.operators.checks." + c]
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
        col = self.layout.column(align=True)
        for status, messages in self.tests:
            if status == "SUCCESS" and self.on_save:
                continue
            for message in messages:
                draw_message_label(col, message, status)
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

        slug = get_slug()

        for check_name, check in checks.items():
            if self.on_save and check_name == "unsaved":
                # No need to check for unsaved changes while we're busy saving.
                continue
            self.tests.append(check.check(slug))

        all_success = True
        for status, messages in self.tests:
            if status != "SUCCESS":
                for message in messages:
                    if message != "File contains unsaved changes":
                        all_success = False
                        break
        if all_success:
            self.tests.append(["SUCCESS", ["All checks passed!"]])

        # Store tests in scene prop
        context.scene.hat_props.latest_tests = json.dumps(self.tests)

        if self.on_save:
            failed_tests = list((t for t in self.tests if t[0] != "SUCCESS"))
            if len(failed_tests) == 0:
                # No problems, no popup.
                return {"FINISHED"}

        return context.window_manager.invoke_props_dialog(self, width=round(350 * dpi_factor.dpi_factor()))

    def execute(self, context):
        return {"FINISHED"}
