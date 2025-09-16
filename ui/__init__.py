if "bpy" not in locals():
    from . import HAT_PT_main
    from . import HAT_PT_results
    from . import HAT_PT_info
    from . import HAT_PT_folder_structure
    from . import HAT_PT_tools
else:
    import importlib

    importlib.reload(HAT_PT_main)
    importlib.reload(HAT_PT_results)
    importlib.reload(HAT_PT_info)
    importlib.reload(HAT_PT_folder_structure)
    importlib.reload(HAT_PT_tools)

classes = [
    HAT_PT_main.HAT_PT_main,
    HAT_PT_results.HAT_PT_results,
    HAT_PT_info.HAT_PT_info,
    HAT_PT_folder_structure.HAT_PT_folder_structure,
    HAT_PT_tools.HAT_PT_tools,
]
