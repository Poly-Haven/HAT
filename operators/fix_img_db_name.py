import bpy
from ..utils import dpi_factor


class HAT_OT_fix_img_db_name(bpy.types.Operator):
    bl_idname = "hat.fix_img_db_name"
    bl_label = "Match Image Names to File Paths"
    bl_description = "Forces image datablock names to match their file name"
    bl_options = {'REGISTER', 'UNDO'}

    on_save: bpy.props.BoolProperty(default=False)

    fixed = []

    def draw(self, context):
        col = self.layout.column(align=True)
        for fn in self.fixed:
            col.label(text="Fixed: " + fn)
        if not self.fixed:
            col.label(text="No image names needed fixing :)")

    def invoke(self, context, event):
        self.fixed = []  # Reset after rerun
        for image in bpy.data.images:
            if image.filepath:
                fn = bpy.path.basename(image.filepath)
                if image.name != fn:
                    image.name = fn
                    self.fixed.append(fn)

        if self.fixed:
            return context.window_manager.invoke_props_dialog(self, width=350 * dpi_factor.dpi_factor())
        else:
            return context.window_manager.invoke_props_popup(self, event)

    def execute(self, context):
        return {'FINISHED'}
