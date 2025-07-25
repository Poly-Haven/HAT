import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    if bpy.data.worlds:
        result = "WARNING"
        messages.append("HDRI or world present.")

    return result, messages
