import bpy
import mathutils
from random import random

def selectedMeshObjects(context):
    return [obj for obj in context.selected_objects if obj.type == "MESH"]

def setAttributeColor(context, obj, attribute, color):
    # Selecting this object only
    attribute = obj.data.color_attributes[attribute]
    if not attribute:
        return False
    obj.data.attributes.active_color = attribute
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
    bpy.context.tool_settings.vertex_paint.brush.color = mathutils.Color(color)
    bpy.ops.paint.vertex_color_set()
    bpy.context.object.data.use_paint_mask = use_paint_mask

    return True

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
                color = (random() for _ in range(3)) if getattr(self, "random_color") else getattr(self, "default_color")
                setAttributeColor(context, obj, self.attribute_name, color)
            else:
                already_exist.append(obj.name)

        bpy.ops.object.mode_set(mode=curr_mode)
        
        if len(already_exist)>0 : self.report({"WARNING"}, f'Attribute "{self.attribute_name}" already exist for {", ".join(already_exist)}. Colors have been replaced.')
        return {"FINISHED"}
    
    def invoke(self, context, event):
        self.objs = selectedMeshObjects(context)
        return context.window_manager.invoke_props_dialog(self)
    
class EditMetarig(bpy.types.Operator):
    bl_idname = "armature.get_metarig"
    bl_label = "Edit Metarig"

    hide_rig: bpy.props.BoolProperty(name="Hide rig",description="If enabled, hide the rig after selecting metarig",default=True)
    enter_edit_mode : bpy.props.BoolProperty(name="Enter Edit Mode",description="When enabled, enter edit mode",default=True)

    @classmethod
    def poll(self, context):
        obj = context.object
        return obj.type == "ARMATURE"
    
    def execute(self, context):
        obj = context.object
        metarig = None
        rig = getattr(obj.data, "rigify_target_rig")
        if rig: # The attribute exists, it returns the rig
            metarig = obj
        else: # It doesnt exist. Need to fetch the metarig. 
            rig = obj
            armatures = [obj for obj in context.scene.objects if obj.type == "ARMATURE"]
            for armature in armatures:
                target_rig = getattr(armature.data, "rigify_target_rig", None)
                if target_rig:
                    if target_rig.name == rig.name:
                        metarig = armature
                        pass
            if metarig is None:
                self.report({"ERROR"}, "No (meta)rig found.")
                return {"CANCELLED"}

        metarig.hide_set(False) # Un-hiding the metarig
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        context.view_layer.objects.active = metarig
        rig.hide_set(True)
        metarig.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}