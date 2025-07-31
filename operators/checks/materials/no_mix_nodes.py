import bpy


def check(slug):
    """Materials should not contain mix nodes"""
    result = "SUCCESS"
    messages = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                mix_types = ["MIX", "MIX_RGB", "MIX_SHADER"]
                if node.type in mix_types:
                    result = "ERROR" if bpy.context.window_manager.hat_props.asset_type == "texture" else "WARNING"
                    messages.append(f"Material '{mat.name}' contains mix node '{node.name}'")

    return result, messages
