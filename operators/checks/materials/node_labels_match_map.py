import bpy
from ....utils.filename_utils import get_map_name
from ....utils import standard_map_names


def check(slug):
    """Image node labels (if set) should match map names"""
    result = "SUCCESS"
    messages = []

    for mat in bpy.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == "TEX_IMAGE" and node.label:
                    if not node.image:
                        result = "ERROR"
                        messages.append(f"Material '{mat.name}' has unused image node")
                    elif not node.image.filepath:
                        result = "ERROR"
                        messages.append(f"'{node.image.name}' has no filepath")
                    else:
                        map_name = get_map_name(node.image.filepath, slug)
                        if node.label.lower() in standard_map_names.aliases:
                            label_map_name = standard_map_names.aliases[node.label.lower()]
                        else:
                            label_map_name = node.label.lower()
                        print(f"{node.label}\n\tmap_name: {map_name}\n\tlabel_map_name: {label_map_name}")
                        if map_name != label_map_name:
                            result = (
                                "ERROR" if bpy.context.window_manager.hat_props.asset_type == "texture" else "WARNING"
                            )
                            messages.append(f"{mat.name}'s image label '{node.label}' != map name '{map_name}'")

    return result, messages
