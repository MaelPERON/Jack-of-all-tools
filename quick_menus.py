import bpy
from math import radians
from .operators import AddColorAttribute

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

def draw_return_button(pie):
    global from_quickmenu
    if from_quickmenu:
        pie.operator("wm.call_menu_pie", text=QuickMenu.bl_label, icon="EVENT_RETURN").name = QuickMenu.bl_idname
        from_quickmenu = False # Restore default state
    else:
        pie.separator()

class QuickMenu(bpy.types.Menu):
    bl_label = "Quick Menu"
    bl_idname = "VIEW3D_MT_joat_quickmenu"

    def draw(self, context):
        layout = self.layout.menu_pie()
        obj = context.object
        box = layout.box()
        box.label(text="")
        box.prop(obj, "name")
        global from_quickmenu
        from_quickmenu = True
        layout.operator("wm.call_menu_pie", text=ViewportDisplay.bl_label, icon=ViewportDisplay.bl_icon).name = ViewportDisplay.bl_idname
        layout.operator("wm.call_menu_pie", text=RigifyShortcuts.bl_label, icon=RigifyShortcuts.bl_icon).name = RigifyShortcuts.bl_idname
        # layout.operator(AddColorAttribute.bl_idname)

class ViewportDisplay(bpy.types.Menu):
    bl_label = "Viewport Display"
    bl_idname = "VIEW3D_MT_joat_display"
    bl_icon = "OVERLAY"

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.object
        # Return option
        draw_return_button(pie)
        
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
        else:
            pie.separator()

        box = pie.box()
        row = box.row()
        box = row.box()
        box.label(text="Visibility")
        box.prop(obj, "hide_select")
        box.prop(obj, "hide_viewport")
        box.prop(obj, "hide_render")
        box.prop(obj, "is_shadow_catcher")
        box.prop(obj, "is_holdout")

        box = row.box()
        box.label(text="Ray Visibility")
        box.prop(obj, "visible_camera")
        box.prop(obj, "visible_diffuse")
        box.prop(obj, "visible_glossy")
        box.prop(obj, "visible_transmission")
        box.prop(obj, "visible_volume_scatter")
        box.prop(obj, "visible_shadow")


class ViewportOverlay(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_joat_viewport_overlay"
    bl_label = "Viewport Overlays"
    bl_icon = "OVERLAY"

    def draw(self, context):
        pie = self.layout.menu_pie()
        draw_return_button(pie)

class RigifyShortcuts(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_joat_rigify"
    bl_label = "Rigify Shortcuts"
    bl_icon = "OUTLINER_OB_ARMATURE"

    def draw(self, context):
        pie = self.layout.menu_pie()
        draw_return_button(pie)

def register():
    bpy.types.VIEW3D_MT_edit_mesh_merge.append(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.append(menu_uv)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_merge.remove(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_uv)