import bpy


class HAT_OT_clear_assets(bpy.types.Operator):
    bl_idname = "hat.clear_assets"
    bl_label = "Clear Assets"
    bl_description = "Clears all assets in the current file"
    bl_options = {"REGISTER"}

    def execute(self, context):
        for attr in dir(bpy.data):
            collection = getattr(bpy.data, attr)
            if hasattr(collection, "__iter__"):
                for block in collection:
                    if hasattr(block, "asset_data") and block.asset_data:
                        block.asset_clear()
        return {"FINISHED"}
