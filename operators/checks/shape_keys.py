import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    for obj in bpy.data.objects:
        if hasattr(obj, "data") and hasattr(obj.data, "shape_keys") and obj.data.shape_keys:
            result = "WARNING"
            messages.append(f"Object '{obj.name}' has shape keys")

    return result, messages
