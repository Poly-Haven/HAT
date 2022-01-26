import bpy
from .. import addon_updater_ops
from ..operators import check
from ..operators import export_gltf
from ..operators import fix_img_db_name
from .. import icons


class HAT_PT_main (bpy.types.Panel):

    bl_label = " "
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'
    bl_options = {'HEADER_LAYOUT_EXPAND', 'DEFAULT_CLOSED'}

    def draw_header(self, context):
        i = icons.get_icons()
        props = context.scene.hat_props

        layout = self.layout
        row = layout.row()
        row.label(text="HAT", icon_value=i['polyhaven'].icon_id)
        sub = row.row(align=True)
        sub.alignment = 'RIGHT'
        sub.prop(props, "asset_type", text='')
        sub.operator(check.HAT_OT_check.bl_idname,
                     text="Check", icon="CHECKMARK").on_save = False
        row.separator()

    def draw(self, context):
        props = context.scene.hat_props
        i = icons.get_icons()

        col = self.layout.column(align=True)
        row = col.row()
        row.label(text="Click 'Check' above to run tests.")
        sub = row.row()
        sub.alignment = 'RIGHT'
        sub.prop(props, "test_on_save",
                 icon='CHECKBOX_HLT' if props.test_on_save else 'CHECKBOX_DEHLT',
                 toggle=True)

        col.separator()
        box = col.box()
        sub = box.column(align=True)
        sub.scale_y = 0.9
        row = sub.row()
        row.label(text="Understanding test results:")
        row.prop(props, 'expand_result_docs', text='', toggle=True, emboss=False,
                 icon='DOWNARROW_HLT' if props.expand_result_docs else 'RIGHTARROW')
        if props.expand_result_docs:
            sub.label(text="Successful test", icon='CHECKMARK')
            sub.label(text="Question - something suspicious, but could be fine",
                      icon_value=i['question'].icon_id)
            sub.label(text="Warning - possible issue, needs investigation",
                      icon_value=i['exclamation-triangle'].icon_id)
            sub.label(text="Error - definite issue that needs to be fixed",
                      icon_value=i['x-circle-fill'].icon_id)
        col.operator(
            fix_img_db_name.HAT_OT_fix_img_db_name.bl_idname, icon="COPY_ID")

        col.separator()

        col = self.layout.column()
        col.operator(
            export_gltf.HAT_OT_export_gltf.bl_idname,
            text=f'Export {props.asset_type} GLTF',
            icon="FILE",
        )

        addon_updater_ops.check_for_update_background()
        addon_updater_ops.update_notice_box_ui(self, context)
