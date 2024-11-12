import bpy
import mathutils
from random import random

def selectedMeshObjects(context):
    return [obj for obj in context.selected_objects if obj.type == "MESH"]

class CleanColorAttributes(bpy.types.Operator):
    bl_idname = "object.clean_color_attributes"
    bl_label = "Clean Color Attributes"

    @classmethod
    def poll(self, context):
        objs = context.selected_objects
        l = 0
        for obj in objs:
            if obj.type == "MESH": l+=1
        return l > 0
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event, title="Are you sure to continue ?", message="This will remove ALL color attributes from your selected objects",icon="WARNING")

    def execute(self, context):
        objs = [obj for obj in context.selected_objects if obj.type == "MESH"]

        curr_mode = context.object.mode
        for obj in objs:
            for attr in obj.data.vertex_colors:
                obj.data.vertex_colors.remove(attr)
            for attr in obj.data.color_attributes:
                obj.data.color_attributes.remove(attr)

        return {"FINISHED"}
    
class AddColorAttribute(bpy.types.Operator):
    bl_idname = "object.add_color_attribute"
    bl_label = "Add Color Attribute"

    attribute_name: bpy.props.StringProperty(name="Attribute Name",default="Attribute")
    random_color: bpy.props.BoolProperty(default=False,name="Use random color")
    default_color: bpy.props.FloatVectorProperty(name="Default Color",subtype="COLOR")

    @classmethod
    def poll(self, context): return True

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "attribute_name")
        layout.prop(self, "random_color")

        row = layout.row()
        row.enabled = not getattr(self, "random_color")
        row.prop(self, "default_color")

    def execute(self, context):
        if len(self.objs) < 1:
            self.report({"ERROR_INVALID_CONTEXT"}, "No mesh objects selected. Cancelling Operator.")
            return {"CANCELLED"}
        
        already_exist = []
        curr_mode = context.object.mode
        for obj in self.objs:
            if not(obj.data.vertex_colors.get(self.attribute_name) or obj.data.color_attributes.get(self.attribute_name)):
                # Creating the attribute
                obj.data.color_attributes.new(name=self.attribute_name, type="FLOAT_COLOR", domain="POINT")

            else:
                already_exist.append(obj.name)

            # Selecting this object only
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

            # Selecting all the mesh
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.mode_set(mode="VERTEX_PAINT")
            use_paint_mask = bpy.context.object.data.use_paint_mask
            bpy.context.object.data.use_paint_mask = True
            color = (random() for _ in range(3)) if getattr(self, "random_color") else getattr(self, "default_color")
            bpy.context.tool_settings.vertex_paint.brush.color = mathutils.Color(color)
            bpy.ops.paint.vertex_color_set()
            bpy.context.object.data.use_paint_mask = use_paint_mask

        # Returning to default status
        bpy.ops.object.mode_set(mode=curr_mode)
        
        if len(already_exist)>0 : self.report({"WARNING"}, f'Attribute "{self.attribute_name}" already exist for {", ".join(already_exist)}. Colors have been replaced.')
        return {"FINISHED"}
    
    def invoke(self, context, event):
        self.objs = selectedMeshObjects(context)
        return context.window_manager.invoke_props_dialog(self)