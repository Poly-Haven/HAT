import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    if bpy.context.scene.hat_props.asset_type == 'model':
        try:
            col = bpy.data.collections[slug]
        except KeyError:
            result = 'ERROR'
            messages = ["No collection with slug name"]
        else:
            messages = ["Collection named as slug"]

    return result, messages
