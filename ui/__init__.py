import imp

from . import main_panel

imp.reload(main_panel)

classes = [main_panel.HAT_PT_main, main_panel.HAT_PT_results, main_panel.HAT_PT_info, main_panel.HAT_PT_tools]
