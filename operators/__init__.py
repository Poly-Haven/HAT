
if "bpy" not in locals():
    from . import check
else:
    import importlib
    importlib.reload(check)

import bpy

classes = [
    check.HAT_OT_check
]
