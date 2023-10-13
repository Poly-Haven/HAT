import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    for img in bpy.data.images:
        if not img.filepath:
            continue
        if not bpy.path.exists(img.filepath):
            result = "ERROR"
            messages.append(f'\'{bpy.path.basename(img.filepath)}\' does not exist')

    return result, messages
