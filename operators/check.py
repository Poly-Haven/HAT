import importlib
import json
import os
import sys
from ..utils import dpi_factor
from ..utils.filename_utils import get_slug
from ..utils.draw_message_label import draw_message_label


def discover_checks():
    """Discover all check modules in the checks directory and its subfolders"""
    checks_dir = os.path.join(os.path.dirname(__file__), "checks")
    check_modules = {}

    # Walk through all subdirectories in checks
    for root, dirs, files in os.walk(checks_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Get relative path from checks directory
                rel_path = os.path.relpath(root, checks_dir)
                if rel_path == ".":
                    # File is in the root checks directory
                    module_path = file[:-3]  # Remove .py extension
                else:
                    # File is in a subdirectory
                    module_path = rel_path.replace(os.sep, ".") + "." + file[:-3]

                check_name = file[:-3]  # Use just the filename as the check name

                try:
                    if "bpy" not in locals():
                        m = importlib.import_module(".checks." + module_path, __package__)
                    else:
                        full_module_name = "bl_ext.user_default.polyhaven_hat.operators.checks." + module_path
                        m = sys.modules[full_module_name]
                        importlib.reload(m)
                    check_modules[check_name] = m
                except (ImportError, KeyError) as e:
                    print(f"Failed to load check module {module_path}: {e}")

    return check_modules


checks = discover_checks()

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
