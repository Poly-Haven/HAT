import bpy
from ...utils.fetch_textures import fetch_textures


def check(slug):
    result = "SUCCESS"
    messages = []

    textures = fetch_textures()
    for image in textures:
        fn = bpy.path.basename(image.filepath)
        if not fn.startswith(slug):
            result = 'WARNING'
            messages.append(fn + " does not start with slug")

    return result, messages
