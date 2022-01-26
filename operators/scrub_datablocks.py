import bpy


class HAT_OT_scrub_datablocks(bpy.types.Operator):
    bl_idname = "hat.scrub_datablocks"
    bl_label = "Scrub Unused Datablocks"
    bl_description = "Cleans the file of all unused datablocks, including those that are protected by a fake user"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        for data_type in dir(bpy.data):
            if hasattr(getattr(bpy.data, data_type), '__iter__'):
                l = list(getattr(bpy.data, data_type))
                for item in l:
                    if hasattr(item, 'use_fake_user'):
                        if item.use_fake_user:
                            item.use_fake_user = False
        purge_result = bpy.ops.outliner.orphans_purge(
            'INVOKE_DEFAULT', do_recursive=True)
        self.report({'INFO'},
                    "Removed some datablocks"
                    if purge_result != {'CANCELLED'}
                    else "No data to remove")
        return {'FINISHED'}
