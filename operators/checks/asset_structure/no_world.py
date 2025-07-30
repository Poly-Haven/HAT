import bpy


def check(slug):
    """No world or HDRI data blocks should be present in the asset"""
    result = "SUCCESS"
    messages = []

    if bpy.data.worlds:
        result = "WARNING"
        messages.append("HDRI or world present.")

    return result, messages
