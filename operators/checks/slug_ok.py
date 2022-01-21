import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    allowed_characters = "qwertyuiopasdfghjklzxcvbnm_-0123456789"

    if slug.lower() != slug:
        return 'ERROR', ["Slug contains uppercase characters"]

    for char in slug:
        if char not in allowed_characters:
            return 'ERROR', ["Slug contains illegal characters"]

    return result, messages
