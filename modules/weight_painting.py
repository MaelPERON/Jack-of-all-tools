import bpy
from bpy.props import *

def enum_collections(scene, context):
	items = []

	armatures = [obj for obj in context.selected_objects if obj.type == "ARMATURE"]
	if len(armatures) > 0:
		armature = bpy.data.armatures.get(armatures[0].name)
		for collection in armature.collections:
			items.append((collection.name, collection.name, f"Select {collection.name} collection"))
	return items

class WeightOperator():
	def get_objs(self, context):
		return [obj for obj in context.selected_objects if obj.type in ['ARMATURE','MESH']]
	
	def get_armature(self, context):
		return self.from_type(self.get_objs, "ARMATURE")[0]

	def from_type(self, objs, type):
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
	
class ToggleSoloCollection(bpy.types.Operator, WeightOperator):
	bl_idname = "joat.toggle_soll_collection"
	bl_label = "Toggle Solo Collection"
	bl_options = {"REGISTER","UNDO"}

	# collec_name: bpy.props.StringProperty(name="Collection Name",default="DEF")
	collec_name: bpy.props.EnumProperty(name="Collection Name",items=enum_collections) # TODO: no collections --> return error, set the new poll

	def execute(self, context):
		objs = self.get_objs(context)

		armature = self.from_type(objs, "ARMATURE")[0]
		armature = bpy.data.armatures.get(armature.name)
		collection = armature.collections.get(self.collec_name)
		if collection is None:
			self.report({"ERROR_INVALID_INPUT"}, f"{self.collec_name} doesn't exist.")
			return {"CANCELLED"}

		collection.is_solo = not collection.is_solo
		return {"FINISHED"}