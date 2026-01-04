import bpy

class OBJECT_OT_create_sculpt_path_shape(bpy.types.Operator):
	bl_idname = "object.create_sculpt_path_shape"
	bl_label = "Create Sculpt Path Shape"
	bl_description = "Creates a Nurbs path and Bézier circle for sculpting"
	bl_options = {'REGISTER', 'UNDO'}

	name: bpy.props.StringProperty( # type: ignore
		name="Nurbs Path Name",
		description="Name for the created Nurbs Path",
		default="default"
	)

	store_in_collection: bpy.props.BoolProperty(  # type: ignore
		name="Store in Collection",
		description="Store the created objects in a new collection",
		default=False
	)

	def execute(self, context):
		# Add Nurbs Path
		bpy.ops.curve.primitive_nurbs_path_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
		nurbs_path = context.active_object
		nurbs_path.name = f"{self.name}_path"

		# Rotate Nurbs Path 90 deg on X
		bpy.ops.transform.rotate(
			value=1.5708,
			orient_axis='X',
			orient_type='GLOBAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='GLOBAL',
			constraint_axis=(True, False, False),
			mirror=False,
			use_proportional_edit=False,
			proportional_edit_falloff='SMOOTH',
			proportional_size=1,
			use_proportional_connected=False,
			use_proportional_projected=False,
			snap=False,
			snap_elements={'INCREMENT'},
			use_snap_project=False,
			snap_target='CLOSEST',
			use_snap_self=True,
			use_snap_edit=True,
			use_snap_nonedit=True,
			use_snap_selectable=False
		)
		# Rotate Nurbs Path 90 deg on Y
		bpy.ops.transform.rotate(
			value=1.5708,
			orient_axis='Y',
			orient_type='GLOBAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='GLOBAL',
			constraint_axis=(False, True, False),
			mirror=False,
			use_proportional_edit=False,
			proportional_edit_falloff='SMOOTH',
			proportional_size=1,
			use_proportional_connected=False,
			use_proportional_projected=False,
			snap=False,
			snap_elements={'INCREMENT'},
			use_snap_project=False,
			snap_target='CLOSEST',
			use_snap_self=True,
			use_snap_edit=True,
			use_snap_nonedit=True,
			use_snap_selectable=False
		)
		# Resize Nurbs Path to 0.04
		bpy.ops.transform.resize(
			value=(0.04, 0.04, 0.04),
			orient_type='GLOBAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='GLOBAL',
			mirror=False,
			use_proportional_edit=False,
			proportional_edit_falloff='SMOOTH',
			proportional_size=1,
			use_proportional_connected=False,
			use_proportional_projected=False,
			snap=False,
			snap_elements={'INCREMENT'},
			use_snap_project=False,
			snap_target='CLOSEST',
			use_snap_self=True,
			use_snap_edit=True,
			use_snap_nonedit=True,
			use_snap_selectable=False
		)
		# Apply scale to Nurbs Path
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		# Set aside the shape
		bpy.ops.transform.translate(
			value=(0.05, 0, 0),
			orient_type='GLOBAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='GLOBAL',
			constraint_axis=(True, False, False),
			mirror=False,
			use_proportional_edit=False,
			proportional_edit_falloff='SMOOTH',
			proportional_size=1,
			use_proportional_connected=False,
			use_proportional_projected=False,
			snap=False,
			snap_elements={'INCREMENT'},
			use_snap_project=False,
			snap_target='CLOSEST',
			use_snap_self=True,
			use_snap_edit=True,
			use_snap_nonedit=True,
			use_snap_selectable=False
		)


		# Set all control points' radius to 1
		for spline in nurbs_path.data.splines:
			for point in spline.points:
				point.radius = 1.0

		# Add Bézier Circle
		bpy.ops.curve.primitive_bezier_circle_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
		bezier_circle = context.active_object
		bezier_circle.name = f"{self.name}_shape"

		# Rotate Bézier Circle 90 deg on X
		bpy.ops.transform.rotate(
			value=1.5708,
			orient_axis='X',
			orient_type='GLOBAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='GLOBAL',
			constraint_axis=(True, False, False),
			mirror=False,
			use_proportional_edit=False,
			proportional_edit_falloff='SMOOTH',
			proportional_size=1,
			use_proportional_connected=False,
			use_proportional_projected=False,
			snap=False,
			snap_elements={'INCREMENT'},
			use_snap_project=False,
			snap_target='CLOSEST',
			use_snap_self=True,
			use_snap_edit=True,
			use_snap_nonedit=True,
			use_snap_selectable=False
		)
		# Resize Bézier Circle to 0.02
		bpy.ops.transform.resize(
			value=(0.02, 0.02, 0.02),
			orient_type='GLOBAL',
			orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
			orient_matrix_type='GLOBAL',
			mirror=False,
			use_proportional_edit=False,
			proportional_edit_falloff='SMOOTH',
			proportional_size=1,
			use_proportional_connected=False,
			use_proportional_projected=False,
			snap=False,
			snap_elements={'INCREMENT'},
			use_snap_project=False,
			snap_target='CLOSEST',
			use_snap_self=True,
			use_snap_edit=True,
			use_snap_nonedit=True,
			use_snap_selectable=False
		)
		# Apply scale to Bézier Circle
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		# Deselect all (simulate outliner.item_activate)
		bpy.ops.object.select_all(action='DESELECT')
		nurbs_path.select_set(True)
		context.view_layer.objects.active = nurbs_path

		# Set bevel mode and object for NurbsPath
		nurbs_path.data.bevel_mode = 'OBJECT'
		nurbs_path.data.bevel_object = bezier_circle

		bezier_circle.select_set(True)
		nurbs_path.select_set(True)

		if self.store_in_collection:
			new_collection = bpy.data.collections.new(f"{self.name}_collection")
			context.scene.collection.children.link(new_collection)

			new_collection.objects.link(bezier_circle)
			new_collection.objects.link(nurbs_path)

		return {'FINISHED'}
	
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "name")

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)