from ....utils.fetch_textures import fetch_textures


def check(slug):
    """All texture resolutions should match within the asset"""
    result = "SUCCESS"
    messages = []

    resolutions = {}

    textures = fetch_textures()
    for image in textures:
        res_str = f"{image.size[0]}x{image.size[1]}"
        resolutions[res_str] = resolutions.get(res_str, []) + [image]

    if len(resolutions) > 1:
        result = "ERROR"
        for res_str, images in resolutions.items():
            messages.append(f"Resolution {res_str} has {len(images)} images")

    return result, messages
