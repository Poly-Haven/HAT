import bpy


def check(slug):
    """No other asset contamination in the file"""
    result = "SUCCESS"
    messages = []

    # There's currently no api call for listing local assets, so we need to iterate through all datablocks...
    for attr in dir(bpy.data):
        collection = getattr(bpy.data, attr)
        if hasattr(collection, "__iter__"):
            for block in collection:
                if hasattr(block, "asset_data") and block.asset_data:
                    result = "ERROR"
                    messages.append("Other asset datablocks found.")
    return result, messages
