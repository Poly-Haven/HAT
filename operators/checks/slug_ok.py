import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    allowed_characters = "qwertyuiopasdfghjklzxcvbnm_-0123456789"

    if slug.lower() != slug:
        return 'ERROR', ["Slug contains uppercase characters"]

    illegal_characters = []
    for char in slug:
        if char not in allowed_characters:
            illegal_characters.append(char)
    if illegal_characters:
        return 'ERROR', [f'Slug contains illegal characters ({"".join(illegal_characters)})']

    return result, messages
