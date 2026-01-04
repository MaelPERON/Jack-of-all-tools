import bpy
import re

pattern = r"(.*?)_\d+(\.\d+)?$"

def format_material(mat: bpy.types.Material) -> str:
	name = mat.name
	match = re.match(pattern, name)
	if match:
		return match.group(1)
	return name

class OBJECT_OT_io_marvelous_conform(bpy.types.Operator):
    bl_idname = "object.io_marvelous_conform"
    bl_label = "IO Marvelous Conform"
    bl_description = "Remove unused material slots and conform materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = context.selected_objects
        active = context.view_layer.objects.active
        

        for obj in selection:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.material_slot_remove_unused()

        bpy.ops.object.select_all(action='DESELECT')
        for obj in selection:
            obj.select_set(True)

        context.view_layer.objects.active = active

        material_registry = {}

        for obj in context.scene.objects:
            for slot in obj.material_slots:
                if slot.material:
                    material = slot.material
                    key = format_material(material)

                    if key not in material_registry:
                        material_registry[key] = material
                        # bpy.data.materials.get(material.name).name = key
                    else:
                        idx = obj.material_slots.find(material.name)
                        if idx != -1:
                            obj.material_slots[idx].material = material_registry[key]

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_io_marvelous_conform.bl_idname)

def register():
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
