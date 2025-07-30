import bpy
from ....utils.fetch_textures import fetch_textures


def check(slug):
    """All texture paths should be relative and point to the textures folder"""
    result = "SUCCESS"
    messages = []

    textures = fetch_textures()
    for image in textures:
        if not image.filepath.replace("\\", "/").startswith("//textures/"):
            result = "ERROR"
            messages.append(f"{bpy.path.basename(image.filepath)} is not in the textures folder")

    return result, messages
