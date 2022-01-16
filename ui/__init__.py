import imp

from . import main_panel
imp.reload(main_panel)

ui_classes = [
    main_panel.HAT_PT_main
]
