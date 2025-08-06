import bpy
import requests
import logging

log = logging.getLogger(__name__)


def check(slug):
    """Blender version is the latest official release"""
    result = "SUCCESS"
    messages = []

    admin_blend_version_url = "https://admin.polyhaven.com/api/public/blenderVersion"

    try:
        response = requests.get(admin_blend_version_url)
        response.raise_for_status()
        data = response.json()
        server_version = data.get("version", "unknown")
    except requests.RequestException as e:
        result = "WARNING"
        messages.append("Failed to retrieve Blender version from PH Admin server: " + str(e))
        log.error("Error fetching Blender version: %s", e)
        return result, messages

    if server_version == "unknown":
        result = "WARNING"
        messages.append("Unknown Blender version from PH Admin server, please tell Greg :(")
        log.error("Unknown Blender version from PH Admin server; data: %s", data)
        return result, messages

    current_version = bpy.app.version_string
    major, minor, patch = map(int, current_version.split(" ")[0].split("."))
    server_major, server_minor, server_patch = map(int, server_version.split(" ")[0].split("."))

    if (major, minor) < (server_major, server_minor):
        result = "ERROR"
        messages.append("Blender version is outdated, please update to Blender " + server_version)

    return result, messages
