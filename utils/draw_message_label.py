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

    if status in status_icon_custom:
        layout.label(text=message, icon_value=i[status_icon_custom[status]].icon_id)
    else:
        layout.label(text=message, icon=status_icon[status])
