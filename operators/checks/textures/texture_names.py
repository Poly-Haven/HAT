import bpy
from ...utils.fetch_textures import fetch_textures


def check(slug):
    """Texture file names should start with the asset slug and follow naming conventions"""
    result = "SUCCESS"
    messages = []

    allowed_characters = "qwertyuiopasdfghjklzxcvbnm_-0123456789."

    textures = fetch_textures()
    for image in textures:
        fn = bpy.path.basename(image.filepath)
        if not fn.startswith(slug):
            result = "WARNING"
            messages.append(fn + " does not start with slug")
        if fn.lower() != fn:
            result = "WARNING"
            messages.append(fn + " contains uppercase characters")
        illegal_characters = []
        for char in fn:
            if char.lower() not in allowed_characters:
                illegal_characters.append(char)
        if illegal_characters:
            result = "WARNING"
            messages.append(f'{fn} contains illegal characters ({"".join(illegal_characters)})')

    return result, messages
