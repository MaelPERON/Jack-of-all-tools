import bpy
import bmesh
from mathutils import Vector, Matrix

class OBJECT_OT_cursor_align_to_selection(bpy.types.Operator):
	# TODO: FIX THE OPERATOR
	"""Rotate 3D Cursor to face selection (align Z axis to average normal)"""
	bl_idname = "view3d.cursor_align_to_selection"
	bl_label = "Align 3D Cursor to Selection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj and obj.mode == 'EDIT' and obj.type == 'MESH'

	def execute(self, context):
		obj = context.active_object
		bm = bmesh.from_edit_mesh(obj.data)
		selected_faces = [f for f in bm.faces if f.select]
		if not selected_faces:
			self.report({'WARNING'}, "No faces selected")
			return {'CANCELLED'}

		# Calculate average normal
		avg_normal = Vector()
		for f in selected_faces:
			avg_normal += f.normal
		avg_normal.normalize()

		# Create a rotation matrix that aligns Z to avg_normal
		up = Vector((0, 0, 1))
		if abs(avg_normal.dot(up)) > 0.999:
			# avg_normal is nearly up, use X as fallback
			tangent = Vector((1, 0, 0))
		else:
			tangent = up.cross(avg_normal).normalized()
		bitangent = avg_normal.cross(tangent).normalized()
		rot_matrix = Matrix((tangent, bitangent, avg_normal)).transposed().to_4x4()

		# Set the cursor rotation
		context.scene.cursor.rotation_mode = 'QUATERNION'
		context.scene.cursor.rotation_quaternion = rot_matrix.to_quaternion()

		self.report({'INFO'}, "3D Cursor aligned to selection normal")
		return {'FINISHED'}

