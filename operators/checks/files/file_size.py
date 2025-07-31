import bpy
import os


def check(slug):
    """File size is within acceptable limits for the asset type"""
    result = "SUCCESS"
    messages = []

    if bpy.data.filepath:
        file_size = os.path.getsize(bpy.data.filepath)

        if bpy.context.window_manager.hat_props.asset_type == "texture":
            warn_file_size = 300  # kB
            max_file_size = 500
        else:
            warn_file_size = 10 * 1024
            max_file_size = 100 * 1024

        if file_size > max_file_size * 1024:
            result = "ERROR"
            messages.append(f"File size >{max_file_size}kB, unnecessary data present?")
            return result, messages
        elif file_size > warn_file_size * 1024:
            result = "WARNING"
            messages.append(f"File size >{warn_file_size}kB")

    return result, messages
