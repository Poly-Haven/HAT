import bpy


def check(slug):
    """Material IOR (Index of Refraction) values are within expected range"""
    result = "SUCCESS"
    messages = []

    materials = list((m for m in bpy.data.materials if m.users > 0 and m.use_nodes))

    for mat in materials:
        for node in mat.node_tree.nodes:
            if node.type == "BSDF_PRINCIPLED":
                i = node.inputs["Specular IOR Level"]
                if len(i.links) == 0 and not (0.4 <= i.default_value <= 0.6):
                    result = "WARNING"
                    messages.append(
                        f"Material '{mat.name}' Specular IOR value on node '{node.name}' is {i.default_value}"
                    )

    return result, messages
