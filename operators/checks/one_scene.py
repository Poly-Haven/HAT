import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    if len(bpy.data.scenes) > 1:
        result = "ERROR"
        messages.append("Multiple scenes found in the file. Please ensure only one scene is present.")

    if len(bpy.context.scene.view_layers) > 1:
        result = "ERROR"
        messages.append("Multiple view layers found")

    return result, messages
