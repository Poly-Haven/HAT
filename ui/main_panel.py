import bpy
import json
from ..operators import check
from ..operators import export_gltf
from ..operators import fix_img_db_name
from ..operators import scrub_datablocks
from ..utils.filename_utils import get_slug
from ..utils.draw_message_label import draw_message_label
from .. import icons


class HAT_PT_main(bpy.types.Panel):

    bl_label = " "
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {"HEADER_LAYOUT_EXPAND", "DEFAULT_CLOSED"}

    def draw_header(self, context):
        i = icons.get_icons()
        props = context.scene.hat_props

        layout = self.layout
        row = layout.row()
        row.label(text="HAT", icon_value=i["polyhaven"].icon_id)
        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.prop(props, "asset_type", text="")
        sub.operator(check.HAT_OT_check.bl_idname, text="Check", icon="CHECKMARK").on_save = False
        row.separator()

    def draw(self, context):
        props = context.scene.hat_props

        col = self.layout.column(align=True)
        row = col.row()
        row.label(text="Click 'Check' above to run tests.")
        sub = row.row()
        sub.alignment = "RIGHT"
        sub.prop(props, "test_on_save", icon="CHECKBOX_HLT" if props.test_on_save else "CHECKBOX_DEHLT", toggle=True)


class HAT_PT_results(bpy.types.Panel):
    bl_label = "Test Results"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    @classmethod
    def poll(self, context):
        return context.scene.hat_props.latest_tests != ""

    def draw(self, context):
        props = context.scene.hat_props
        col = self.layout.column()
        if props.latest_tests:
            try:
                tests = json.loads(props.latest_tests)
                for status, messages in tests:
                    for message in messages:
                        if message != "File contains unsaved changes":
                            draw_message_label(col, message, status)
            except json.JSONDecodeError:
                col.label(text="Failed to decode latest tests JSON.", icon="ERROR")


class HAT_PT_info(bpy.types.Panel):
    bl_label = "Info"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    def draw(self, context):
        i = icons.get_icons()
        props = context.scene.hat_props
        slug = get_slug()
        col = self.layout.column(align=True)

        # Slug
        row = col.row()
        row.alignment = "LEFT"
        row.label(text=f"Detected Slug: {slug}")
        row.operator("wm.url_open", text="", icon="VIEWZOOM").url = f"https://polyhaven.com/tools/slug-check?s={slug}"

        # Texture info
        if props.asset_type == "texture":
            plane = bpy.data.objects.get("Plane")
            if plane:
                min_dimension = 1.8
                row = col.row()
                row.alignment = "LEFT"
                row.label(
                    text=f"Dimensions: {plane.dimensions.x:.1f}m x {plane.dimensions.y:.1f}m",
                    icon_value=(
                        i["exclamation-triangle"].icon_id
                        if plane.dimensions.x < min_dimension or plane.dimensions.y < min_dimension
                        else 0
                    ),
                )
                row.operator("hat.refresh", text="", icon="FILE_REFRESH", emboss=False)
            else:
                col.label(text='No "Plane" found in the scene.', icon="ERROR")
            material = bpy.data.materials.get(slug)
            if material:
                try:
                    disp_node = material.node_tree.nodes["Displacement"]
                    col.label(text=f"Displacement Scale: {disp_node.inputs['Scale'].default_value * 1000:.0f}mm")
                except KeyError:
                    col.label(text="No displacement node found", icon="ERROR")
                except AttributeError:
                    col.label(text="Material does not have a node tree.", icon="ERROR")
            else:
                col.label(text=f'No material named "{slug}" found.', icon="ERROR")


class HAT_PT_tools(bpy.types.Panel):
    bl_label = "Tools"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    def draw(self, context):
        props = context.scene.hat_props
        col = self.layout.column()
        col.operator(scrub_datablocks.HAT_OT_scrub_datablocks.bl_idname, icon="TRASH")
        col.operator(fix_img_db_name.HAT_OT_fix_img_db_name.bl_idname, icon="COPY_ID")

        col.separator()

        col = self.layout.column()
        col.operator(
            export_gltf.HAT_OT_export_gltf.bl_idname,
            text=f"Export {props.asset_type} GLTF",
            icon="FILE",
        )
