import bpy


class HAT_OT_delete_world(bpy.types.Operator):
    bl_idname = "hat.delete_world"
    bl_label = "Delete World"
    bl_description = "Deletes the current world"
    bl_options = {"REGISTER"}

    def execute(self, context):
        for world in bpy.data.worlds:
            bpy.data.worlds.remove(world, do_unlink=True)
        return {"FINISHED"}
