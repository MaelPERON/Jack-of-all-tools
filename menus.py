import bpy
from .utils import placeOperator
from .operators import SummonBone, SelectObjectWithModifiers, CopyLightGroup

def SummonBoneOperator(self, context):
    layout = self.layout
    layout.separator()
    placeOperator(layout, SummonBone)

def SelectObjectWithModifiersOperator(self, context):
    layout = self.layout
    layout.separator()
    placeOperator(layout, SelectObjectWithModifiers)

def Lightgroup(self, context):
    layout = self.layout
    layout.separator()
    placeOperator(layout, CopyLightGroup)

def register():
    # Context Menu
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(SummonBoneOperator)
    bpy.types.VIEW3D_MT_mesh_add.append(SummonBoneOperator)
    # Select object menu
    bpy.types.VIEW3D_MT_select_object.append(SelectObjectWithModifiersOperator)
    # Link / Transfer menu
    bpy.types.VIEW3D_MT_make_links.append(Lightgroup)

def unregister():
    # Context Menu
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(SummonBoneOperator)
    bpy.types.VIEW3D_MT_mesh_add.remove(SummonBoneOperator)
    # Select object menu
    bpy.types.VIEW3D_MT_select_object.remove(SelectObjectWithModifiersOperator)
    # Link / Transfer menu
    bpy.types.VIEW3D_MT_make_links.remove(Lightgroup)