import bpy
from math import radians

from_quickmenu = False

def menu_merge(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("mesh.select_face_by_sides",icon="UV_FACESEL")

def menu_uv(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("mesh.edges_select_sharp",icon="IPO_CONSTANT")
    for angle in [30,60,90]:
        op = layout.operator("mesh.edges_select_sharp",text=f'{angle}°',icon="IPO_CONSTANT")
        op.sharpness = radians(angle-1)

class QuickMenu(bpy.types.Menu):
    bl_label = "Quick Menu"
    bl_idname = "VIEW3D_MT_joat_quickmenu"

    def draw(self, context):
        layout = self.layout.menu_pie()
        obj = context.object
        layout.label(text="Hello World")
        layout.prop(obj, "name")
        global from_quickmenu
        from_quickmenu = True
        layout.operator("wm.call_menu_pie", text=ViewportDisplay.bl_label).name = ViewportDisplay.bl_idname
        
class ViewportDisplay(bpy.types.Menu):
    bl_label = "Viewport Display"
    bl_idname = "VIEW3D_MT_joat_display"

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.object
        # Return option
        global from_quickmenu
        if from_quickmenu:
            pie.operator("wm.call_menu_pie", text=QuickMenu.bl_label).name = QuickMenu.bl_idname
            from_quickmenu = False # Restore default state
        else:
            pie.separator()
        
        box = pie.box()
        box.label(text="Object",icon="OBJECT_DATA")
        box.prop(obj, "display_type")
        box.prop(obj, "color")
        box.prop(obj, "show_name")
        box.prop(obj, "show_in_front")
        box.prop(obj, "show_axes")
        box.prop(obj, "show_wire")

        if obj.type == "ARMATURE":
            box = pie.box()
            box.label(text="Armature",icon="ARMATURE_DATA")
            arm = obj.data
            props = [
                ["display_type",None],
                ["show_names","FILE_TEXT"],
                ["show_axes","EMPTY_ARROWS"],
                ["show_bone_custom_shapes","BONE_DATA"],
                ["show_bone_colors","COLOR"]
            ]
            for prop, icon in props:
                args = { "data": arm, "property": prop, "text": ' '.join([word.capitalize() for word in prop.split("_")]) }
                if icon: args["icon"] = icon
                box.prop(**args)


def register():
    bpy.types.VIEW3D_MT_edit_mesh_merge.append(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.append(menu_uv)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_merge.remove(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_uv)