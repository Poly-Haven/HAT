import bpy
import os


def remove_extension(s):
    return os.path.splitext(s)[0]


def remove_num(s):
    if s[-1] == 'k':
        *parts, num = s[:-1].split('_')
        if num.isdigit():
            return '_'.join(parts)
    return s


def get_map_name(fp, slug, removeNum=True):
    s = remove_extension(bpy.path.basename(fp))
    s = remove_num(s) if removeNum else s

    if s.startswith(slug):
        return s[len(slug) + 1:].lower()

    s = s.lower()
    if s.endswith('nor_gl'):
        return 'nor_gl'
    if s.endswith('nor_dx'):
        return 'nor_dx'

    return s.split('_')[-1]  # Fallback
