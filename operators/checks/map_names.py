import bpy
from ...utils.fetch_textures import fetch_textures
from ...utils.filename_utils import get_map_name
from ...utils.standard_map_names import names as standard_map_names


def check(slug):
    result = "SUCCESS"
    messages = []

    textures = fetch_textures()
    for image in textures:
        map_name = get_map_name(image.filepath, slug)
        if map_name not in standard_map_names:
            fn = bpy.path.basename(image.filepath)
            result = 'WARNING'
            messages.append(f'{fn}: unrecognized map \'{map_name}\'')

    return result, messages
