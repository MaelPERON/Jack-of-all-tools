import bpy

class ExposureGainOperator(bpy.types.Operator):
	bl_idname = "object.exposure_gain"
	bl_label = "Exposure Gain"
	bl_description = "Apply exposure gain to selected lights"
	bl_options = {'REGISTER', 'UNDO'}

	gain: bpy.props.FloatProperty( # type: ignore
		name="Gain",
		description="Gain factor to apply to the exposure",
		default=1.0,
		min=0.0,
	)

	@staticmethod
	def has_lights(context):
		return any(obj.type == 'LIGHT' for obj in context.selected_objects)

	@classmethod
	def poll(cls, context):
		return cls.has_lights(context)
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "gain")

	def execute(self, context):
		if not self.has_lights(context):
			self.report({'WARNING'}, "No lights in selection.")
			return {'CANCELLED'}

		ignored_drivers = []
		lights = [obj for obj in context.selected_objects if obj.type == 'LIGHT']
		for light in lights:
			if light.data.animation_data and light.data.animation_data.drivers:
				exposure_driver = next(
					(d for d in light.data.animation_data.drivers if d.data_path == "exposure"), None
				)
				if exposure_driver:
					ignored_drivers.append(exposure_driver)
					continue

			light.data.exposure += self.gain

		if ignored_drivers:
			self.report({'WARNING'}, f"Ignored {len(ignored_drivers)} light(s) with exposure drivers.")
		self.report({'INFO'}, f"Applied gain of {self.gain} to {len(lights) - len(ignored_drivers)} light(s).")
		return {'FINISHED'}