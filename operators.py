import bpy


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