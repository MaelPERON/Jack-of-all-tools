import bpy

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

    mode: bpy.props.EnumProperty(items=[
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