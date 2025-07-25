import bpy


class HAT_OT_refresh(bpy.types.Operator):
    bl_idname = "hat.refresh"
    bl_label = "Refresh"
    bl_description = "Hovering over this icon refreshes the UI, since Blender does not update the Dimensions reliably"
    bl_options = {"REGISTER"}

    def execute(self, context):
        # Actually a dummy operator that does nothing, just used to refresh the UI.
        return {"FINISHED"}
