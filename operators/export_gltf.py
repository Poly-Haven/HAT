import bpy


class HAT_OT_export_gltf(bpy.types.Operator):
    bl_idname = "hat.export_gltf"
    bl_label = "Export GLTF"
    bl_description = "Export this file as a GLTF file as standard for uploading to polyhaven.com"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def execute(self, context):
        slug = bpy.path.display_name_from_filepath(bpy.data.filepath)

        # First check for ARM texture, since we'll need this anyway.
        return {'FINISHED'}
