from .. import icons


def draw_message_label(layout, message, status):
    """
    Draw a message label with appropriate icon based on status.

    Args:
        layout: Blender UI layout object
        message: Text message to display
        status: Status type ("ERROR", "WARNING", "QUESTION", "SUCCESS")
    """
    i = icons.get_icons()
    status_icon_custom = {
        "ERROR": "x-circle-fill",
        "WARNING": "exclamation-triangle",
        "QUESTION": "question",
    }
    status_icon = {
        "SUCCESS": "CHECKMARK",
    }

    fix_buttons = {
        "HDRI or world present.": "HAT_OT_delete_world",
    }

    if message in fix_buttons:
        layout = layout.row(align=True)
        layout.alignment = "LEFT"

    if status in status_icon_custom:
        layout.label(text=message, icon_value=i[status_icon_custom[status]].icon_id)
    else:
        layout.label(text=message, icon=status_icon[status])

    if message in fix_buttons:
        layout.operator(fix_buttons[message], text="Fix")
