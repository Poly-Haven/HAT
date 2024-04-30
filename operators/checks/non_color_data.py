import bpy
from ...utils import filename_utils


def check(slug):
    result = "SUCCESS"
    messages = []

    linear_types = [
        "rough",
        "metal",
        "nor_gl",
        "disp",
    ]
    sRGB_types = [
        "diff",
    ]
    aliases = {
        "roughness": "rough",
        "metallic": "metal",
        "nor": "nor_gl",
        "norm": "nor_gl",
        "normal": "nor_gl",
        "normals": "nor_gl",
        "height": "disp",
        "displacement": "disp",
        "color": "diff",
        "col": "diff",
        "diffuse": "diff",
        "diffuse_color": "diff",
        "albedo": "diff",
    }

    for img in bpy.data.images:
        if img.filepath:
            map_name = filename_utils.get_map_name(img.filepath, slug)
            if map_name in aliases:
                map_name = aliases[map_name]

            if map_name in linear_types:
                if img.colorspace_settings.name != "Non-Color":
                    result = "ERROR"
                    messages.append(bpy.path.basename(img.filepath) + " isn't Non-Color")

            if map_name in sRGB_types:
                if img.colorspace_settings.name != "sRGB":
                    result = "ERROR"
                    messages.append(bpy.path.basename(img.filepath) + " isn't sRGB")

    if result == "SUCCESS":
        messages = ["All data texture maps are in the correct color space"]

    return result, messages
