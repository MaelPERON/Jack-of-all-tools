import bpy
from .utils import placeOperator
from .operators import SummonBone

def SummonBoneOperator(self, context):
    layout = self.layout
    layout.separator()
    placeOperator(layout, SummonBone)

def register():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(SummonBoneOperator)
    bpy.types.VIEW3D_MT_mesh_add.append(SummonBoneOperator)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(SummonBoneOperator)
    bpy.types.VIEW3D_MT_mesh_add.remove(SummonBoneOperator)