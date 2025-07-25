if "bpy" not in locals():
    from . import check
    from . import export_gltf
    from . import fix_img_db_name
    from . import refresh
    from . import scrub_datablocks
else:
    import importlib

    importlib.reload(check)
    importlib.reload(export_gltf)
    importlib.reload(fix_img_db_name)
    importlib.reload(refresh)
    importlib.reload(scrub_datablocks)

import bpy

classes = [
    check.HAT_OT_check,
    export_gltf.HAT_OT_export_gltf,
    fix_img_db_name.HAT_OT_fix_img_db_name,
    refresh.HAT_OT_refresh,
    scrub_datablocks.HAT_OT_scrub_datablocks,
]
