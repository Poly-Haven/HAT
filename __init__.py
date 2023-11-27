if "bpy" not in locals():
    from . import ui
    from . import operators
    from . import icons
else:
    import imp

    imp.reload(ui)
    imp.reload(operators)
    imp.reload(icons)

import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "HAT: Haven Asset Tester",
    "description": "Internal quality control tool for polyhaven.com",
    "author": "Poly Haven: Greg Zaal, James Cock",
    "version": (1, 0, 14),
    "blender": (3, 2, 0),
    "location": "Properties > Scene",
    "warning": "",
    "wiki_url": "https://github.com/Poly-Haven/HAT",
    "tracker_url": "https://github.com/Poly-Haven/HAT/issues",
    "category": "Scene",
}


class HATProperties(bpy.types.PropertyGroup):
    asset_type: bpy.props.EnumProperty(
        name="Asset Type",
        description="What type of asset is this?",
        default="model",
        items=(
            ("model", "Model", "A 3D model to be published on polyhaven.com"),
            ("texture", "Texture", "A texture to be published on polyhaven.com"),
        ),
    )
    test_on_save: bpy.props.BoolProperty(
        name="Test on save",
        description=(
            "Automatically run tests when saving this file. Enables magically after running tests manually once"
        ),
        default=False,
    )
    expand_result_docs: bpy.props.BoolProperty(
        name="Toggle", description="Show/hide info explaining the type test results you may see", default=False
    )


# Remember what shading type each space used to restore after saving
space_shading_types = {}


@persistent
def pre_save_handler(dummy):
    """Set shading mode to solid so that it's quicker to open next time."""
    global space_shading_types
    space_shading_types = {}
    for area in (a for a in bpy.context.screen.areas if a.type == "VIEW_3D"):
        for space in (s for s in area.spaces if s.type == "VIEW_3D"):
            if space.shading.type not in space_shading_types:
                space_shading_types[space.shading.type] = []
            space_shading_types[space.shading.type].append(space)
            if space.shading.type == "MATERIAL":
                space.shading.type = "SOLID"


@persistent
def post_save_handler(dummy):
    """Run tests"""
    if bpy.context.scene.hat_props.test_on_save:
        bpy.ops.hat.check("INVOKE_DEFAULT", on_save=True)

    for t, spaces in space_shading_types.items():
        for s in spaces:
            if s.shading.type != t:
                s.shading.type = t


classes = (
    [
        HATProperties,
    ]
    + ui.classes
    + operators.classes
)


def register():
    icons.previews_register()

    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.hat_props = bpy.props.PointerProperty(type=HATProperties)
    bpy.app.handlers.save_pre.append(pre_save_handler)
    bpy.app.handlers.save_post.append(post_save_handler)


def unregister():
    bpy.app.handlers.save_pre.remove(pre_save_handler)
    bpy.app.handlers.save_post.remove(post_save_handler)

    icons.previews_unregister()

    del bpy.types.Scene.hat_props

    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
