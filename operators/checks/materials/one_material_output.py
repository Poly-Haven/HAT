import bpy


def check(slug):
    """Materials should have exactly one output node"""
    result = "SUCCESS"
    messages = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            output_nodes = [node for node in mat.node_tree.nodes if node.type == "OUTPUT_MATERIAL"]
            if len(output_nodes) != 1:
                result = "ERROR"
                messages.append(f"Material '{mat.name}' has {len(output_nodes)} output nodes")

    return result, messages
