import bpy


def check(slug):
    """No orphaned data blocks (unused data) should be present"""
    result = "SUCCESS"
    messages = []

    for data_type in dir(bpy.data):
        if hasattr(getattr(bpy.data, data_type), "__iter__"):
            l = list(getattr(bpy.data, data_type))
            for item in l:
                if not hasattr(item, "users"):
                    continue
                if item.users == 0:
                    if data_type == "images" and item.name == "Render Result":
                        continue
                    dt_name = data_type.replace("_", " ")
                    result = "ERROR"
                    messages.append(f"Unused {dt_name}: {item.name}")

    return result, messages
