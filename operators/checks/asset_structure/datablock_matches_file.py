import bpy


def check(slug):
    """Texture datablock names should match their file names"""
    result = "SUCCESS"
    messages = []

    for img in bpy.data.images:
        if not img.filepath:
            continue
        fn = bpy.path.basename(img.filepath)
        if fn != img.name:
            result = "WARNING"
            messages.append(f"Image '{img.name}' has different filename")

    return result, messages
