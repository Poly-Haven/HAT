import bpy


def check(slug):
    """Texture assets should only have "Plane" and "Sphere" objects"""
    result = "SUCCESS"
    messages = []

    if bpy.context.window_manager.hat_props.asset_type == "texture":
        for obj in bpy.context.scene.objects:
            if obj.type == "MESH":
                if obj.name not in ["Plane", "Sphere"]:
                    result = "ERROR"
                    messages.append(f"Unexpected object found: {obj.name}")

    return result, messages
