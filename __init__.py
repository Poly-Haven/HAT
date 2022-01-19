if "bpy" not in locals():
    from . import addon_updater_ops
    from . import ui
    from . import operators
    from . import icons
else:
    import imp
    imp.reload(addon_updater_ops)
    imp.reload(ui)
    imp.reload(operators)
    imp.reload(icons)

import bpy

bl_info = {
    "name": "HAT: Haven Asset Tester",
    "description": "Internal quality control tool for polyhaven.com",
    "author": "Greg Zaal, Poly Haven",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "Properties > Output",
    "warning": "",
    "wiki_url": "https://github.com/Poly-Haven/HAT",
    "tracker_url": "https://github.com/Poly-Haven/HAT/issues",
    "category": "Scene",
}


class HatPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Add-on Updater Prefs
    auto_check_update: bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months: bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days: bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=1,
        min=0,
    )
    updater_intrval_hours: bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes: bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )
    updater_expand_prefs: bpy.props.BoolProperty(default=False)

    def draw(self, context):
        addon_updater_ops.update_settings_ui(self, context)


classes = [
    HatPreferences,
] + ui.classes + operators.classes


def register():
    addon_updater_ops.register(bl_info)

    icons.previews_register()

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    addon_updater_ops.unregister()

    icons.previews_unregister()

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
