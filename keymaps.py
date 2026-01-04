import bpy

from .quick_menus import QuickMenu

shortcuts = []

def register():
	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	if kc:
		km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
		kmi = km.keymap_items.new('wm.call_menu_pie', 'V', 'PRESS')
		kmi.properties.name = QuickMenu.bl_idname
		shortcuts.append((km, kmi))

def unregister():
	for km, kmi in shortcuts:
		km: bpy.types.KeyMap
		km.keymap_items.remove(kmi)
	shortcuts.clear()