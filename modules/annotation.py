import bpy

class SetStrokePlacement(bpy.types.Operator):
    bl_idname = "annotation.joat_set_stroke_placement"
    bl_label = "Set Stroke Placement Mode"

    mode: bpy.props.EnumProperty(items=[
        ("CURSOR","Cursor",""),
        ("VIEW","View",""),
        ("SURFACE","Surface","")
    ],default="CURSOR")

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"
    
    def execute(self, context):
        context.scene.tool_settings.annotation_stroke_placement_view3d = self.mode
        self.report({"INFO"}, f"Set annotation placement mode to {self.mode}")