import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    materials = list((m for m in bpy.data.materials if m.users > 0 and not m.is_grease_pencil))

    if bpy.context.scene.hat_props.asset_type == "model":
        for mat in materials:
            if not mat.name.startswith(slug):
                result = "WARNING"
                messages.append(f"Material '{mat.name}' doesn't start with slug")
    else:
        if len(materials) == 0:
            return "ERROR", ["No material found"]
        if len(materials) > 1:
            return "ERROR", ["More than one material present"]
        if materials[0].name != slug:
            return "ERROR", ["Material name not the same as slug"]

    return result, messages
