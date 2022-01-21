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
                fn = bpy.path.basename(node.image.filepath)
                if not fn.startswith(slug):
                    result = 'WARNING'
                    messages.append(fn + " does not start with slug")

    return result, messages
