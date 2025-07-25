import bpy
import os


def check(slug):
    """All referenced texture files exist on disk"""
    result = "SUCCESS"
    messages = []

    for img in bpy.data.images:
        if not img.filepath:
            continue
        if not os.path.exists(bpy.path.abspath(img.filepath)):
            result = "ERROR"
            messages.append(f"'{bpy.path.basename(img.filepath)}' does not exist")

    return result, messages
