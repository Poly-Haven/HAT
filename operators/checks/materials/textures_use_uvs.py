import bpy


def check(slug):
    """All textures should use UVs for mapping"""
    result = "SUCCESS"
    messages = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == "TEX_COORD":
                    # Only 'UV' output should be connected
                    for o in node.outputs:
                        if o.name != "UV" and o.is_linked:
                            result = "ERROR"
                            messages.append(f"'{node.name}' in material '{mat.name}' has linked {o.name} output")
                elif node.type.startswith("TEX_"):
                    if node.inputs:
                        for i in node.inputs:
                            if i.type == "VECTOR":
                                if not i.is_linked:
                                    result = "ERROR"
                                    messages.append(f"'{node.name}' in material '{mat.name}' has unlinked UV input")

    return result, messages
