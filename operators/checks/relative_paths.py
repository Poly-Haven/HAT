import bpy
from ...utils.fetch_textures import fetch_textures


def check(slug):
    result = "SUCCESS"
    messages = []

    textures = fetch_textures()
    for image in textures:
        if not image.filepath.replace("\\", "/").startswith("//textures/"):
            result = "ERROR"
            messages.append(f"{bpy.path.basename(image.filepath)} is not in the textures folder")

    return result, messages
