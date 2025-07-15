import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    if f"{slug}_geometry_nodes" in bpy.data.collections:
        messages.append("Geometry nodes collection found")

        if f"{slug}_LOD0" not in bpy.data.collections and f"{slug}_static" not in bpy.data.collections:
            return "ERROR", ["LOD0 or static collection not found"]

    return result, messages
