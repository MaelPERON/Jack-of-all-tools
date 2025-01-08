import bpy
from math import radians
from .operators import AddColorAttribute, EditMetarig, GenerateRig, ToggleSkinMode
from .utils import getIndex, placeOperator

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
        if obj is None:
            layout.alert = True
            layout.separator()
            layout.separator()
            layout.separator()
            layout.box().label(text="Select an object first.", icon="ERROR")
            return
        box = layout.box()
        box.label(text="Main Shortcuts",icon="SCRIPTPLUGINS")
        box.prop(obj, "name")
        draw_subpie_menu(layout, ViewportDisplay)
        draw_subpie_menu(layout, RigShortcuts)
        draw_subpie_menu(layout, ObjectVisibility)
        draw_subpie_menu(layout, SceneUtility)
        draw_subpie_menu(layout, WeightShortcuts)

class ViewportDisplay(bpy.types.Menu):
    bl_label = "Viewport Display"
    bl_idname = "VIEW3D_MT_joat_display"
    bl_icon = "OVERLAY"

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.object
        # Return option
        # WEST
        draw_return_button(pie, QuickMenu)

        # EAST
        draw_subpie_menu(pie, ObjectVisibility)

        # SOUTH
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
        elif obj.type == "CAMERA":
            box = pie.box()
            box.label(text="Camera", icon="CAMERA_DATA")
            cam = obj.data
            row = box.row(align=True)
            col = row.column()
            props = [
                ["lens",None],
                ["lens_unit",None],
                ["show_passepartout",None]
            ]
            draw_props(col, cam, props)
            row.separator()
            col = row.column()
            props = [
                ["passepartout_alpha", None],
                ["show_limits", None],
                ["show_mist", None],
                ["show_sensor", None],
                ["show_name", None]
            ]
            draw_props(col, cam, props)
        else:
            pie.separator()

        # NORTH
        box = pie.box()
        row = box.row()
        col = row.column()
        col.label(text="Object",icon="OBJECT_DATA")
        col.prop(obj, "display_type")
        col.prop(obj, "color")
        col = row.column()
        col.prop(obj, "show_name")
        col.prop(obj, "show_in_front")
        col.prop(obj, "show_axis")
        col.prop(obj, "show_wire")

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
        draw_return_button(pie, QuickMenu)
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

class SceneUtility(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_joat_scene"
    bl_label = "Scene Utility"
    bl_icon = "SCENE_DATA"

    def draw(self, context):
        pie = self.layout.menu_pie()
        draw_return_button(pie, QuickMenu)
        box = pie.box()
        box.prop(context.scene, "joat_reference_opacity")
        pie.operator("object.link_image_opacity")

class RigShortcuts(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_joat_rigify"
    bl_label = "Rig Shortcuts"
    bl_icon = "OUTLINER_OB_ARMATURE"

    def draw(self, context):
        pie = self.layout.menu_pie()
        obj = context.object
        draw_return_button(pie, QuickMenu)

        placeOperator(pie, EditMetarig)
        if context.preferences.addons.get("rigify"):
            pie.operator_context = "INVOKE_DEFAULT"
            placeOperator(pie, GenerateRig)

class WeightShortcuts(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_joat_skining"
    bl_label = "Weight Painting Shortcuts"
    bl_icon = "OUTLINER_OB_ARMATURE"

    def draw(self, context):
        pie = self.layout.menu_pie()
        draw_return_button(pie, QuickMenu)

        if context.selected_pose_bones is not None and len(context.selected_pose_bones) > 0:
            box = pie.box()
            box.label(text="Lock/Unlock/Toggle")
            col = box.column()
            for action in ["LOCK","UNLOCK","TOGGLE"]:
                icon = (action+"ED") if action != "TOGGLE" else "UV_SYNC_SELECT"
                op = col.operator("object.vertex_group_lock", icon=icon, text="")
                op.action = action
                op.mask = "SELECTED"
        else:
            pie.separator()

        pie.separator()
        placeOperator(pie, ToggleSkinMode)

def register():
    bpy.types.VIEW3D_MT_edit_mesh_merge.append(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.append(menu_uv)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_merge.remove(menu_merge)
    bpy.types.VIEW3D_MT_uv_map.remove(menu_uv)