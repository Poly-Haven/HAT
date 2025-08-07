import bpy
from mathutils import Vector


def check(slug):
    """Objects should be at the origin"""
    result = "SUCCESS"
    messages = []

    zero = Vector((0, 0, 0))

    objects = []

    for obj in bpy.data.objects:
        if obj.type == "MESH":
            if obj.location != zero:
                result = "WARNING" if bpy.context.window_manager.hat_props.asset_type == "texture" else "QUESTION"
                objects.append(obj)

    if not objects:
        return result, messages

    if len(objects) <= 5:
        for obj in objects:
            messages.append(f"{obj.name} is not at origin")
    else:
        messages.append(f"{len(objects)} objects are not at origin")

    return result, messages
