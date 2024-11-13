from bpy.utils import previews
import os

custom_icons = None

def register():
    global custom_icons
    custom_icons = previews.new()
    curr_folder = os.path.join(os.path.dirname(__file__), "icons")
    if os.path.exists(curr_folder):
        for icon in [file for file in os.listdir(curr_folder) if file.endswith(".png")]:
            icon_id = os.path.splitext(icon)[0]
            icon_path = os.path.join(curr_folder, icon)
            custom_icons.load(f'joat_{icon_id}', icon_path, "IMAGE")
    else:
        from warnings import warn
        warn("Could not find icons folder")


def unregister():
    global custom_icons
    if custom_icons is not None:
        previews.remove(custom_icons)