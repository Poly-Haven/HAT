import bpy


def check(slug):
    """LOD (Level of Detail) collections and objects are properly structured"""
    result = "SUCCESS"
    messages = []

    collection_lod_exists = f"{slug}_LOD0" in bpy.data.collections

    for obj in bpy.data.objects:
        if obj.name.endswith("_LOD0") and not collection_lod_exists:
            return "ERROR", ["LOD0 collection not found for slug: " + slug]

    if collection_lod_exists:
        main_collection = bpy.data.collections[slug]
        if bpy.data.collections[f"{slug}_LOD0"] not in main_collection.children.values():
            return "ERROR", ["LOD0 collection is not a child of the main collection"]
        messages = ["LOD0 collection exists"]

    return result, messages
