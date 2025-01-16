import bpy
from bpy.props import *

class WeightOperator():
	def get_objs(self, context):
		return [obj for obj in context.selected_objects if obj.type in ['ARMATURE','MESH']]
	
	def from_type(self, objs, type, single=False):
		return [obj for obj in objs if obj.type == type]
	
	@classmethod
	def poll(self, context):
		objs = context.selected_objects
		if context.mode not in ["PAINT_WEIGHT", "POSE"]: return False
		return True

class SelectionToVertexGroup(bpy.types.Operator, WeightOperator):
	bl_idname = "paint.joat_selection_to_vertex_group"
	bl_label = "Selection To Vertex Group"
	bl_options = {"REGISTER","UNDO"}

	group: StringProperty(name="Vertex Group Name",default="DEF-")
	weight: FloatProperty(name="Vertex Weight",min=0,max=1,default=1)

	@classmethod
	def poll(self, context):
		return context.mode == "EDIT_MESH"
	
	def execute(self, context):
		obj = context.active_object

		if self.group == "":
			self.report({"ERROR_INVALID_INPUT"}, "Vertex group name can't be empty")
			return {"CANCELLED"}

		# Creating Vertex Group if needed
		v_groups = obj.vertex_groups
		v_group = v_groups.get(self.group)
		if v_group is None:
			v_group = obj.vertex_groups.new(name=self.group)
		v_groups.active_index = v_group.index

		# Assigning selected vertices
		bpy.ops.object.vertex_group_assign()

		return {"FINISHED"}
	
class ToggleSkinMode(bpy.types.Operator, WeightOperator):
	bl_idname = "joat.toggle_skin_mode"
	bl_label = "Toggle Skin Mode"
	bl_options = {"UNDO"}
	
	def execute(self, context):
		objs = self.get_objs(context)
		
		armature = self.from_type(objs, "ARMATURE")[0]
		mesh = self.from_type(objs, "MESH")[0]

		mode = context.mode
		bpy.ops.object.mode_set(mode="OBJECT")
		if mode == "PAINT_WEIGHT":
			context.view_layer.objects.active = armature
			bpy.ops.object.mode_set(mode="POSE")
		elif mode == "POSE":
			context.view_layer.objects.active = mesh
			bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
		return {"FINISHED"}