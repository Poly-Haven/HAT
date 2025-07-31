import bpy


def check(slug):
    """SSS may have been accidentally enabled"""
    result = "SUCCESS"
    messages = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    if node.inputs.get("Subsurface Weight") and node.inputs["Subsurface Weight"].default_value > 0:
                        result = "WARNING"
                        messages.append(f"Material '{mat.name}' has SSS weight > 0")

    return result, messages
