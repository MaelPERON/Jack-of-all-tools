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

def register():
    bpy.types.VIEW3D_MT_edit_mesh_merge.append(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.append(menu_uv)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_merge.remove(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_uv)