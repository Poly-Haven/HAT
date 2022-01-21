import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    checked_files = []
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                if node.image.filepath in checked_files:
                    continue
                checked_files.append(node.image.filepath)
                if not node.image.filepath.startswith('//textures'):
                    result = 'ERROR'
                    messages.append(
                        f'{node.image.name} path doesn\'t start with //textures')

    if result == "SUCCESS":
        messages = ["Texture paths are relative"]

    return result, messages
