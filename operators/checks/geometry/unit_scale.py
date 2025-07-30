import bpy


def check(slug):
    """Scene unit scale is set to 1.0 meters"""
    result = "SUCCESS"
    messages = []

    if bpy.context.scene.unit_settings.scale_length != 1:
        result = "ERROR"
        messages.append("Scene Unit Scale is not 1.0")

    if bpy.context.scene.unit_settings.length_unit != "METERS":
        result = "ERROR"
        messages.append("Scene Unit Length is not Meters")

    if bpy.context.scene.unit_settings.system != "METRIC":
        result = "ERROR"
        messages.append("Scene Unit System is not Metric")

    return result, messages
