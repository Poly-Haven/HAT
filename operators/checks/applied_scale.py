import bpy
from mathutils import Vector


def check(slug):
    result = "SUCCESS"
    messages = []

    one = Vector((1, 1, 1))
    ignored_types = [
        "CAMERA",
        "LIGHT",
    ]

    severity = "ERROR" if bpy.context.scene.hat_props.asset_type == "texture" else "WARNING"

    for obj in bpy.data.objects:
        if obj.scale != one and obj.type not in ignored_types:
            result = severity
            messages.append(obj.name + " scale not applied")

    return result, messages
