import bpy
from ...utils.fetch_textures import fetch_textures
from ...utils.filename_utils import get_map_name
from ...utils.standard_map_names import names as standard_map_names


def check(slug):
    """Texture map names follow standardized naming conventions"""
    result = "SUCCESS"
    messages = []

    strict = bpy.context.scene.hat_props.asset_type == "texture"

    textures = fetch_textures()
    for image in textures:
        map_name = get_map_name(image.filepath, slug, strict=strict)
        if map_name not in standard_map_names:
            fn = bpy.path.basename(image.filepath)
            result = "WARNING" if strict else "QUESTION"
            messages.append(f"{fn}: unrecognized map '{map_name}'")

    return result, messages
