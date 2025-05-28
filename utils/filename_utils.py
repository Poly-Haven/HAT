import bpy
import os


def remove_extension(s):
    return os.path.splitext(s)[0]


def remove_num(s):
    if s[-1] == "k":
        *parts, num = s[:-1].split("_")
        if num.isdigit():
            return "_".join(parts)
    return s


def get_map_name(fp, slug, removeNum=True, strict=True):
    s = remove_extension(bpy.path.basename(fp))
    s = remove_num(s) if removeNum else s

    if strict and s.startswith(slug):
        # strict assumes slug_map.ext, otherwise slug_part_map.ext
        return s[len(slug) + 1 :].lower()

    if s.endswith("_nor_gl"):
        return "nor_gl"
    if s.endswith("_nor_dx"):
        return "nor_dx"

    return s.split("_")[-1]


def get_slug():
    slug = bpy.path.display_name_from_filepath(bpy.data.filepath)
    if slug.endswith(".export"):
        slug = slug[:-7]
    return slug
