import bpy


def check(slug):
    """Model collection name should match the asset slug"""
    result = "SUCCESS"
    messages = []

    if bpy.context.scene.hat_props.asset_type == "model":
        try:
            _ = bpy.data.collections[slug]
        except KeyError:
            result = "ERROR"
            messages = ["No collection with slug name"]

    return result, messages
