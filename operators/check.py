import bpy
from ..utils import dpi_factor
from ..utils import filename_utils


def non_color_data(slug):
    result = "SUCCESS"
    messages = []

    linear_types = [
        "rough",
        "metal",
        "nor_gl",
        "disp",
    ]
    aliases = {
        'roughness': 'rough',
        'metallic': 'metal',
        'nor': 'nor_gl',
        'norm': 'nor_gl',
        'normal': 'nor_gl',
        'normals': 'nor_gl',
        'height': 'disp',
        'displacement': 'disp',
    }

    for img in bpy.data.images:
        if img.filepath:
            map_name = filename_utils.get_map_name(img.filepath, slug)
            if map_name in aliases:
                map_name = aliases[map_name]

            if map_name in linear_types:
                if img.colorspace_settings.name != 'Non-Color':
                    result = 'ERROR'
                    messages.append(bpy.path.basename(
                        img.filepath) + " isn't Non-Color")

    if result == "SUCCESS":
        messages = ["All data texture maps are Non-Color"]

    return result, messages


def unsaved():
    if bpy.data.is_dirty:
        return 'WARNING', ["File contains unsaved changes"]
    return 'SUCCESS', []


class HAT_OT_check(bpy.types.Operator):
    bl_idname = "hat.check"
    bl_label = "Check"
    bl_description = "Run all checks"
    bl_options = {'UNDO'}

    tests = []  # [["STATUS", [messages]]]

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def draw(self, context):
        status_icon = {
            'ERROR': 'CANCEL',
            'WARNING': 'ERROR',  # Blender's "error" icon is a warning triangle...?
            'SUCCESS': 'CHECKMARK',
        }
        col = self.layout.column(align=True)
        for status, messages in self.tests:
            for message in messages:
                col.label(text=message, icon=status_icon[status])

    def invoke(self, context, event):
        self.tests = []  # Reset after rerun

        slug = bpy.path.display_name_from_filepath(bpy.data.filepath)

        self.tests.append(non_color_data(slug))
        self.tests.append(unsaved())

        return context.window_manager.invoke_props_dialog(self, width=300 * dpi_factor.dpi_factor())

    def execute(self, context):
        return {'FINISHED'}
