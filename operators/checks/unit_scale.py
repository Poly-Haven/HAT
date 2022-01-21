import bpy


def check(slug):
    if bpy.context.scene.unit_settings.scale_length != 1:
        return 'ERROR', ["Scene Unit Scale is not 1.0"]
    return 'SUCCESS', []
