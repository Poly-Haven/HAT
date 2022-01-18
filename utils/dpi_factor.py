import bpy


def dpi_factor():
    prefs = bpy.context.preferences.system
    # python access to this was only added recently, assume non-retina display is used if using older blender
    if hasattr(prefs, 'pixel_size'):
        retinafac = bpy.context.preferences.system.pixel_size
    else:
        retinafac = 1
    return bpy.context.preferences.system.dpi / (72 / retinafac)
