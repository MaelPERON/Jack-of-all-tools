import bpy
from .utils import placeOperator
from .operators import SummonBone, SelectObjectWithModifiers

def SummonBoneOperator(self, context):
    layout = self.layout
    layout.separator()
    placeOperator(layout, SummonBone)

def SelectObjectWithModifiersOperator(self, context):
    layout = self.layout
    layout.separator()
    placeOperator(layout, SelectObjectWithModifiers)

def register():
    # Context Menu
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(SummonBoneOperator)
    bpy.types.VIEW3D_MT_mesh_add.append(SummonBoneOperator)
    # Select object menu
    bpy.types.VIEW3D_MT_select_object.append(SelectObjectWithModifiersOperator)

def unregister():
    # Context Menu
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(SummonBoneOperator)
    bpy.types.VIEW3D_MT_mesh_add.remove(SummonBoneOperator)
    # Select object menu
    bpy.types.VIEW3D_MT_select_object.remove(SelectObjectWithModifiersOperator)