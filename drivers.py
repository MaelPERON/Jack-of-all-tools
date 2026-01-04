import bpy
import functools

def on_view_layer_change():
	vl = bpy.context.view_layer
	vl.update() 
	print(f"View layer changed to: {vl.name}")

bpy.msgbus.subscribe_rna(
	key=(bpy.types.Window, "view_layer"),
	owner=__name__,
	args=(),
	notify=on_view_layer_change
)

def view_layer(name: str = "", depsgraph=None) -> bool | int:
	vl = bpy.context.view_layer
	# Optionally use depsgraph if needed in future
	print(vl)
	if not name: return False
	return vl.name == name if vl else False

def view_layer_index(depsgraph=None) -> int:
	vl = bpy.context.view_layer
	return list(bpy.context.scene.view_layers).index(vl) if vl else -1

@bpy.app.handlers.persistent
def load_drivers(dummy):
	print("Loading drivers into driver namespace...")
	bpy.app.driver_namespace["view_layer"] = functools.partial(view_layer, depsgraph=bpy.context.evaluated_depsgraph_get())
	bpy.app.driver_namespace["vl"] = functools.partial(view_layer, depsgraph=bpy.context.evaluated_depsgraph_get())
	bpy.app.driver_namespace["view_layer_index"] = functools.partial(view_layer_index, depsgraph=bpy.context.evaluated_depsgraph_get())
	bpy.app.driver_namespace["vli"] = functools.partial(view_layer_index, depsgraph=bpy.context.evaluated_depsgraph_get())

def register():
	print("Register")
	if load_drivers not in bpy.app.handlers.load_post:
		bpy.app.handlers.load_post.append(load_drivers)

def unregister():
	print("Unregister")
	if load_drivers in bpy.app.handlers.load_post:
		bpy.app.handlers.load_post.remove(load_drivers)
	# del bpy.app.driver_namespace["curr_view_layer_index"]
	# del bpy.app.driver_namespace["cvli"]
	# del bpy.app.driver_namespace["match_view_layer_name"]
	# del bpy.app.driver_namespace["mvln"]