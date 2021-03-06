import bpy
from mathutils import Vector


def check(slug):
    result = "SUCCESS"
    messages = []

    zero = Vector((0, 0, 0))

    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            if obj.location != zero:
                result = 'WARNING' if bpy.context.scene.hat_props.asset_type == 'texture' else 'QUESTION'
                messages.append(
                    obj.name + " is not at origin")

    return result, messages
