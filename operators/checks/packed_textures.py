import bpy


def check(slug):
    """No texture files should be packed into the blend file"""
    result = "SUCCESS"
    messages = []

    for image in bpy.data.images:
        if image.packed_file:
            result = "ERROR"
            messages.append(image.name + " is packed")

    return result, messages
