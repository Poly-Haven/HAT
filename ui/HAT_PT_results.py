import bpy
import json
from ..utils.draw_message_label import draw_message_label


class HAT_PT_results(bpy.types.Panel):
    bl_label = "Test Results"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    @classmethod
    def poll(self, context):
        return context.window_manager.hat_props.latest_tests != ""

    def draw(self, context):
        props = context.window_manager.hat_props
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
