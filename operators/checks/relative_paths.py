from ...utils.fetch_textures import fetch_textures


def check(slug):
    result = "SUCCESS"
    messages = []

    textures = fetch_textures()
    for image in textures:
        if not image.filepath.startswith("//textures"):
            result = "ERROR"
            messages.append(f"{image.name} path doesn't start with //textures")

    return result, messages
