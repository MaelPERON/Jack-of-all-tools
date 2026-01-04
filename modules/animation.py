import bpy
from bpy.app.handlers import persistent
import os
from ..utils import open_directory_in_explorer

class QuickDopesheetSwitch(bpy.types.Menu):
    bl_idname = "DOPESHEET_MT_joat_switchdopesheet"
    bl_label = "Switch Dopesheet Mode"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "EXEC_DEFAULT"
        pie = layout.menu_pie()
        modes = [
            ("Dopesheet","action"),
            ("Action","object_data"),
            ("Shapekey","shapekey_data"),
            ("Gpencil","greasepencil"),
            ("Mask","mod_mask"),
            ("Cachefile","file")
        ]
        for mode, icon in modes:
            op = pie.operator(operator="area.switch_dopesheet", text=mode, icon=icon.upper())
            op.mode = mode.upper()


class SwitchDopesheet(bpy.types.Operator):
    bl_idname = "area.switch_dopesheet"
    bl_label = "Switch Dopesheet"

    mode: bpy.props.EnumProperty(items=[ # type: ignore
        ("DOPESHEET", "Dopesheet", ""),
        ("ACTION", "Action", ""),
        ("SHAPEKEY", "Shapekey", ""),
        ("GPENCIL", "Gpencil", ""),
        ("MASK", "Mask", ""),
        ("CACHEFILE", "Cachefile", "")
    ],default="ACTION")

    @classmethod
    def poll(self, context):
        return (space := context.space_data) is not None and space.type == "DOPESHEET_EDITOR"

    def execute(self, context):
        if (space := context.space_data) is None:
            return {"CANCELLED"}
        
        space.ui_mode = self.mode
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class ExportPlayblast(bpy.types.Operator):
    bl_idname = "animation.joat_export_playblast"
    bl_label = "Export Playblast"
    bl_options = {"REGISTER","UNDO"}
    has_loom = False

    version: bpy.props.IntProperty() # type: ignore

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"
    
    def execute(self, context):
        if self.has_loom : context.scene.loom.output_render_version = self.version
        bpy.ops.render.opengl("INVOKE_DEFAULT", animation=True)
        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Exporting playblast ?")
        if self.has_loom : layout.prop(self, "version")
        layout.separator()
        box = layout.box()
        box.label(text=context.scene.render.filepath,icon="FOLDER_REDIRECT")

    def invoke(self, context, event):
        scene = context.scene
        self.has_loom = hasattr(scene, "loom")
        if version := scene.loom.output_render_version if self.has_loom else None:
            self.version = version+1
        return context.window_manager.invoke_props_dialog(self)
    
class OpenPlayblastFolder(bpy.types.Operator):
    bl_idname = "animation.joat_open_playblast_folder"
    bl_label = "Open Playblast Folder"

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        filepath = context.scene.render.filepath
        folder = os.path.dirname(filepath)
        if os.path.exists(folder):
            open_directory_in_explorer(folder)
        else:
            self.report({"WARN"}, f'"{folder}" doest not exist.')
            return {"CANCELLED"}
        return {"FINISHED"}