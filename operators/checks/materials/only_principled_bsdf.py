import bpy


def check(slug):
    """Only Principled BSDF shaders should be used"""
    result = "SUCCESS"
    messages = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                for o in node.outputs:
                    if o.type == "SHADER":
                        if node.type != "BSDF_PRINCIPLED":
                            result = (
                                "ERROR" if bpy.context.window_manager.hat_props.asset_type == "texture" else "WARNING"
                            )
                            messages.append(f"Material '{mat.name}' contains {node.type} shader")

    return result, messages
