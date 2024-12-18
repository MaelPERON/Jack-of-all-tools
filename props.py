from bpy.props import *
import bpy

def register():
    bpy.types.Scene.joat_reference_opacity = FloatProperty(name="Image References Opacity",min=0,max=1,precision=2,default=1)