import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            if len(obj.data.vertex_colors) != 0:
                result = 'WARNING'
                messages.append(
                    obj.name + " has vertex colors, this may break GLTF export.")

    return result, messages
