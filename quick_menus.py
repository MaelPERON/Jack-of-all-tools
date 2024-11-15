import bpy
from math import radians
from .operators import AddColorAttribute, EditMetarig
from .utils import getIndex

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

def draw_props(layout, data, props):
    for args in props:
        prop = args[0]
        icon = getIndex(args, 1)
        showText = getIndex(args, 2)
        showText = showText if showText is not None else True
        text = ' '.join([word.capitalize() for word in prop.split("_")]) 
        args = { "data": data, "property": prop, "text": text }
        if icon:
            args["icon"] = icon
            args["icon_only"] = showText
        layout.prop(**args)

def draw_return_button(pie, menu):
    pie.operator("wm.call_menu_pie", text=menu.bl_label, icon="EVENT_RETURN").name = menu.bl_idname

def draw_subpie_menu(layout, menu):
    layout.operator("wm.call_menu_pie", text=menu.bl_label, icon=menu.bl_icon).name = menu.bl_idname

class QuickMenu(bpy.types.Menu):
    bl_label = "Quick Menu"
    bl_idname = "VIEW3D_MT_joat_quickmenu"

    def draw(self, context):
        layout = self.layout.menu_pie()
        obj = context.object
        box = layout.box()
        box.label(text="Main Shortcuts",icon="SCRIPTPLUGINS")
        box.prop(obj, "name")
        draw_subpie_menu(layout, ViewportDisplay)
        draw_subpie_menu(layout, RigifyShortcuts)

class ViewportDisplay(bpy.types.Menu):
    bl_label = "Viewport Display"
    bl_idname = "VIEW3D_MT_joat_display"
    bl_icon = "OVERLAY"

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.object
        # Return option
        draw_return_button(pie, QuickMenu)
        
        box = pie.box()
        box.label(text="Object",icon="OBJECT_DATA")
        box.prop(obj, "display_type")
        box.prop(obj, "color")
        box.prop(obj, "show_name")
        box.prop(obj, "show_in_front")
        box.prop(obj, "show_axis")
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
            draw_props(box, arm, props)
        else:
            pie.separator()

        draw_subpie_menu(pie, ObjectVisibility)

class ViewportOverlay(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_joat_viewport_overlay"
    bl_label = "Viewport Overlays"
    bl_icon = "OVERLAY"

    def draw(self, context):
        pie = self.layout.menu_pie()
        draw_return_button(pie, ViewportDisplay)

class ObjectVisibility(bpy.types.Menu):
    bl_label = "Object Visibility"
    bl_idname = "VIEW3D_MT_joat_display_visibility"
    bl_icon = "HIDE_OFF"

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.object
        draw_return_button(pie, ViewportDisplay)
        box = pie.box()
        box.label(text="Visibility")
        props = [
            ["hide_select", "RESTRICT_SELECT_OFF", False],
            ["hide_viewport", "RESTRICT_VIEW_OFF", False],
            ["hide_render", "RESTRICT_RENDER_OFF", False],
            ["is_shadow_catcher", "INDIRECT_ONLY_ON", False],
            ["is_holdout", "HOLDOUT_ON", False]
        ]
        draw_props(box, obj, props)

        box = pie.box()
        box.label(text="Ray Visibility")
        props = [
            ["visible_camera", None, False],
            ["visible_diffuse", None, False],
            ["visible_glossy", None, False],
            ["visible_transmission", None, False],
            ["visible_volume_scatter", None, False],
            ["visible_shadow", None, False]
        ]
        draw_props(box, obj, props)
    

class RigifyShortcuts(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_joat_rigify"
    bl_label = "Rigify Shortcuts"
    bl_icon = "OUTLINER_OB_ARMATURE"

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.object
        draw_return_button(pie, QuickMenu)

        pie.operator(EditMetarig.bl_idname, QuickMenu)

def register():
    bpy.types.VIEW3D_MT_edit_mesh_merge.append(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.append(menu_uv)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_merge.remove(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_uv)