import bpy

def set_light_group(view_layer, objs, name):
    for obj in objs:
        obj.lightgroup = name

    if view_layer.lightgroups.get(name) is None:
        view_layer.lightgroups.add(name=name)

    for area in bpy.context.screen.areas:
        if area.type == "PROPERTIES":
            area.tag_redraw()