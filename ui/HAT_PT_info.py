import bpy
from ..utils.filename_utils import get_slug
from .. import icons


class HAT_PT_info(bpy.types.Panel):
    bl_label = "Info"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "HAT_PT_main"

    def draw(self, context):
        i = icons.get_icons()
        props = context.window_manager.hat_props
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

        # Model info
        if props.asset_type == "model":
            geo_nodes = bpy.data.node_groups.get(f"{slug}_scatter") or bpy.data.node_groups.get(slug)
            if geo_nodes:
                col.label(text="Geometry nodes default values:")
                for key, value in geo_nodes.interface.items_tree.items():
                    if value.in_out == "INPUT":
                        if hasattr(value, "default_value"):
                            col.label(text=f"{key}: {value.default_value}", icon="BLANK1")
