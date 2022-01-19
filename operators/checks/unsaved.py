import bpy


def check():
    if bpy.data.is_dirty:
        return 'WARNING', ["File contains unsaved changes"]
    return 'SUCCESS', []
