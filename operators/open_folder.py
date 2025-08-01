import bpy
import os
import sys
import subprocess


class HAT_OT_open_folder(bpy.types.Operator):
    bl_idname = "hat.open_folder"
    bl_label = "Open Folder"
    bl_description = "Open the folder containing the current blend file"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return bool(bpy.data.filepath)

    def execute(self, context):
        blend_filepath = bpy.data.filepath
        folder_path = os.path.dirname(blend_filepath)

        try:
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", folder_path])
            else:  # Linux and other Unix-like systems
                subprocess.call(["xdg-open", folder_path])
        except Exception as e:
            self.report({"ERROR"}, f"Failed to open folder: {str(e)}")
            return {"CANCELLED"}

        return {"FINISHED"}
