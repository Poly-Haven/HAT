import bpy
from mathutils import Vector


def check(slug):
    """Texture preview plane has non-default dimensions"""
    result = "SUCCESS"
    messages = []

    if bpy.context.scene.hat_props.asset_type == "texture":
        expected_objects = ["Sphere", "Plane"]
        for obj_name in expected_objects:
            try:
                _ = bpy.data.objects[obj_name]
            except KeyError:
                result = "ERROR"
                messages.append(f"Expecting object named '{obj_name}'")
        if result == "SUCCESS":
            plane = bpy.data.objects["Plane"]
            default_dimensions = Vector((2, 2, 0))
            if plane.dimensions == default_dimensions:
                result = "QUESTION"
                messages = ["Plane has default dimensions (2 meters), confirm this is accurate."]

    return result, messages
