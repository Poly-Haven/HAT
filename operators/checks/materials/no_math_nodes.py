import bpy


def check(slug):
    """Materials should not contain math nodes, which mess with exporters"""
    result = "SUCCESS"
    messages = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == "MATH":
                    result = "ERROR" if bpy.context.window_manager.hat_props.asset_type == "texture" else "WARNING"
                    messages.append(f"Material '{mat.name}' contains math node '{node.name}'")

    return result, messages
