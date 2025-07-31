import bpy


def check(slug):
    """No unused nodes in materials"""
    result = "SUCCESS"
    messages = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.outputs:
                    node_is_connected = False
                    for output in node.outputs:
                        if output.is_linked:
                            node_is_connected = True
                            break
                    if not node_is_connected:
                        result = "ERROR"
                        messages.append(f"Material '{mat.name}' has unused node '{node.name}'")

    return result, messages
