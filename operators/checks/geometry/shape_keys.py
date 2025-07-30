import bpy


def check(slug):
    """Objects should not have shape keys which may cause issues for GLTF export"""
    result = "SUCCESS"
    messages = []

    for obj in bpy.data.objects:
        if hasattr(obj, "data") and hasattr(obj.data, "shape_keys") and obj.data.shape_keys:
            result = "WARNING"
            messages.append(f"Object '{obj.name}' has shape keys")

    return result, messages
