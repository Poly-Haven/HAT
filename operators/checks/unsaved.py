import bpy


def check(slug):
    if bpy.data.is_dirty:
        return 'WARNING', ["File contains unsaved changes"]
    return 'SUCCESS', []
