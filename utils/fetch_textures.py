import bpy


def fetch_textures():
    '''Returns an array of images in use by material nodes'''
    checked_files = []
    textures = []
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                if node.image.filepath in checked_files:
                    continue
                checked_files.append(node.image.filepath)
                textures.append(node.image)
    return textures
