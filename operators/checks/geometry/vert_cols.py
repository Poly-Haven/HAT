import bpy


def check(slug):
    """Objects should not have vertex colors which may break GLTF export"""
    result = "SUCCESS"
    messages = []

    for obj in bpy.data.objects:
        if obj.type == "MESH":
            if len(obj.data.vertex_colors) != 0:
                result = "WARNING"
                messages.append(obj.name + " has vertex colors, this may break GLTF export.")

    return result, messages
