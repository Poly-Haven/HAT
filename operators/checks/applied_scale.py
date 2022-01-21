import bpy
from mathutils import Vector


def check(slug):
    result = "SUCCESS"
    messages = []

    one = Vector((1, 1, 1))
    ignored_types = [
        'CAMERA',
        'LIGHT',
    ]

    for obj in bpy.data.objects:
        if obj.scale != one and obj.type not in ignored_types:
            result = 'WARNING'
            messages.append(obj.name + " has non-uniform scale")

    return result, messages
