import bpy

class OBJECT_OT_create_offset(bpy.types.Operator):
	bl_idname = "object.create_offset"
	bl_label = "Create Offset"
	bl_description = "Create an offset empty at the cursor and parent to selected object(s)"

	name: bpy.props.StringProperty( # type: ignore
		name="Offset Name",
		description="Name for the created Offset Empty",
		default="offset"
	)

	display_size: bpy.props.FloatProperty(  # type: ignore
		name="Display Size",
		description="Display size of the empty",
		default=0.25,
		min=0.01,
		max=10.0
	)

	constraint: bpy.props.BoolProperty(  # type: ignore
		name="Add Constraint",
		description="Add a Copy Transforms constraint to the offset empty targeting the target empty",
		default=False
	)

	constraint_enabled: bpy.props.BoolProperty(  # type: ignore
		name="Constraint Enabled",
		description="Enable the constraint on creation",
		default=False
	)

	constraint_snap_to_world: bpy.props.BoolProperty(  # type: ignore
		name="Snap Target to World",
		description="Snap the target empty to world origin instead of cursor location",
		default=False
	)

	def execute(self, context):
		# Selected objects
		selected_objs = context.selected_objects

		# Snap cursor to selected
		stored_location = context.scene.cursor.location.copy()
		bpy.ops.view3d.snap_cursor_to_selected()
		bpy.ops.object.empty_add(
			type='PLAIN_AXES',
			radius=1,
			align='WORLD',
			location=context.scene.cursor.location,
			scale=(1, 1, 1)
		)
		empty_obj = context.object
		empty_obj.empty_display_size = self.display_size
		empty_obj.name = f"grp_{self.name}"

		if self.constraint: # Creating target empty and constraint
			bpy.ops.object.empty_add(
				type='SPHERE',
				radius=1,
				align='WORLD',
				location=context.scene.cursor.location,
				scale=(1, 1, 1)
			)
			target_obj = context.object
			target_obj.empty_display_size = self.display_size * 0.5
			target_obj.name = f"tgt_{self.name}"

			constraint = empty_obj.constraints.new(type="COPY_TRANSFORMS")
			constraint.target = target_obj
			constraint.name = f"{self.name} offset target constraint".title()
			constraint.enabled = False

		context.scene.cursor.location = stored_location
		
		# Parent empty to selected objects
		bpy.ops.object.select_all(action='DESELECT')
		for obj in selected_objs:
			obj.select_set(True)
		empty_obj.select_set(True)
		bpy.context.view_layer.objects.active = empty_obj
		bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

		if self.constraint:
			if self.constraint_enabled:
				constraint.enabled = True

			if self.constraint_snap_to_world:
				target_obj.location = (0, 0, 0)

		return {'FINISHED'}
	
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "name")
		layout.prop(self, "display_size")

		layout.prop(self, "constraint")
		if self.constraint:
			box = layout.box()
			box.label(text="Constraint Settings:")
			row = box.row(align=True)
			row.prop(self, "constraint_enabled", toggle=True)
			row.prop(self, "constraint_snap_to_world", toggle=True)

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)