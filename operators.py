import bpy, bmesh
import mathutils
from random import random
from .utils import isMetarig

def selectedMeshObjects(context):
    return [obj for obj in context.selected_objects if obj.type == "MESH"]

def setAttributeColor(context, obj, attribute, color):
    # Selecting this object only
    attribute = obj.data.color_attributes[attribute]
    if not attribute:
        return False
    obj.data.attributes.active_color = attribute
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(state=True)
    context.view_layer.objects.active = obj

    # Selecting all the mesh
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode="VERTEX_PAINT")
    use_paint_mask = bpy.context.object.data.use_paint_mask
    bpy.context.object.data.use_paint_mask = True
    bpy.context.tool_settings.vertex_paint.brush.color = mathutils.Color(color)
    bpy.ops.paint.vertex_color_set()
    bpy.context.object.data.use_paint_mask = use_paint_mask

    return True

class CleanColorAttributes(bpy.types.Operator):
    bl_idname = "object.clean_color_attributes"
    bl_label = "Clean Color Attributes"

    @classmethod
    def poll(self, context):
        objs = context.selected_objects
        l = 0
        for obj in objs:
            if obj.type == "MESH": l+=1
        return l > 0
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event, title="Are you sure to continue ?", message="This will remove ALL color attributes from your selected objects",icon="WARNING")

    def execute(self, context):
        objs = [obj for obj in context.selected_objects if obj.type == "MESH"]

        curr_mode = context.object.mode
        for obj in objs:
            for attr in obj.data.vertex_colors:
                obj.data.vertex_colors.remove(attr)
            for attr in obj.data.color_attributes:
                obj.data.color_attributes.remove(attr)

        return {"FINISHED"}
    
class AddColorAttribute(bpy.types.Operator):
    bl_idname = "object.add_color_attribute"
    bl_label = "Add Color Attribute"

    attribute_name: bpy.props.StringProperty(name="Attribute Name",default="Attribute")
    random_color: bpy.props.BoolProperty(default=False,name="Use random color")
    default_color: bpy.props.FloatVectorProperty(name="Default Color",subtype="COLOR")

    @classmethod
    def poll(self, context): return True

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "attribute_name")
        layout.prop(self, "random_color")

        row = layout.row()
        row.enabled = not getattr(self, "random_color")
        row.prop(self, "default_color")

    def execute(self, context):
        if len(self.objs) < 1:
            self.report({"ERROR_INVALID_CONTEXT"}, "No mesh objects selected. Cancelling Operator.")
            return {"CANCELLED"}
        
        already_exist = []
        curr_mode = context.object.mode
        for obj in self.objs:
            if not(obj.data.vertex_colors.get(self.attribute_name) or obj.data.color_attributes.get(self.attribute_name)):
                # Creating the attribute
                obj.data.color_attributes.new(name=self.attribute_name, type="FLOAT_COLOR", domain="POINT")
                color = (random() for _ in range(3)) if getattr(self, "random_color") else getattr(self, "default_color")
                setAttributeColor(context, obj, self.attribute_name, color)
            else:
                already_exist.append(obj.name)

        bpy.ops.object.mode_set(mode=curr_mode)
        
        if len(already_exist)>0 : self.report({"WARNING"}, f'Attribute "{self.attribute_name}" already exist for {", ".join(already_exist)}. Colors have been replaced.')
        return {"FINISHED"}
    
    def invoke(self, context, event):
        self.objs = selectedMeshObjects(context)
        return context.window_manager.invoke_props_dialog(self)

class GenerateRig(bpy.types.Operator):
    bl_idname = "armature.regerenate_rig"
    bl_label = "(Re)generate rig"
    bl_options = {"REGISTER", "UNDO"}

    hide_metarig: bpy.props.BoolProperty(name="Hide Metarig",default=True)

    @classmethod
    def poll(self, context):
        if not context.preferences.addons.get("rigify"): return False
        return isMetarig(context.object)

    def execute(self, context):
        obj = context.object
        bpy.ops.pose.rigify_generate()
        obj.hide_set(self.hide_metarig)
        return {"FINISHED"}
    
class EditMetarig(bpy.types.Operator):
    bl_idname = "armature.get_metarig"
    bl_label = "Edit Metarig"

    hide_rig: bpy.props.BoolProperty(name="Hide rig",description="If enabled, hide the rig after selecting metarig",default=True)
    enter_edit_mode : bpy.props.BoolProperty(name="Enter Edit Mode",description="When enabled, enter edit mode",default=True)

    @classmethod
    def poll(self, context):
        obj = context.object
        return obj.type == "ARMATURE"
    
    def execute(self, context):
        obj = context.object
        metarig = None
        rig = getattr(obj.data, "rigify_target_rig")
        if rig: # The attribute exists, it returns the rig
            metarig = obj
        else: # It doesnt exist. Need to fetch the metarig. 
            rig = obj
            armatures = [obj for obj in context.scene.objects if obj.type == "ARMATURE"]
            for armature in armatures:
                target_rig = getattr(armature.data, "rigify_target_rig", None)
                if target_rig:
                    if target_rig.name == rig.name:
                        metarig = armature
                        pass
            if metarig is None:
                self.report({"ERROR"}, "No (meta)rig found.")
                return {"CANCELLED"}

        metarig.hide_set(False) # Un-hiding the metarig
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        context.view_layer.objects.active = metarig
        rig.hide_set(True)
        metarig.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}
    
class SummonBone(bpy.types.Operator):
    bl_idname = "armature.summon_bone"
    bl_label = "Summon Bone"
    bl_options = {"REGISTER","UNDO"}

    bone_name: bpy.props.StringProperty(name="Bone Name",default="Bone")

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        armatures = [arm for arm in context.selected_objects if arm.type == "ARMATURE"]
        if context.object is not None and context.object.type != "MESH":
            self.report({"ERROR_INVALID_CONTEXT"}, "No active mesh object found. Please, select one.")
            return {"CANCELLED"}
        if len(armatures) != 1:
            self.report({"ERROR_INVALID_INPUT"}, "Please, select only ONE armature object.")
            return {"CANCELLED"}
        
        armature = armatures[0]
        obj = context.object
        selected_objs = context.selected_objects

        # Retrieving the coordinates for the bone's tail and head
        def true_coordinates(co):
            co = obj.matrix_world @ co
            return mathutils.Vector((a-armature.location[i] for i, a in enumerate(co)))

        with bpy.context.temp_override(selected_objects=obj):
            bpy.ops.object.mode_set(mode="EDIT")
            mesh = bmesh.from_edit_mesh(obj.data)
            verts = [elem for elem in mesh.select_history if isinstance(elem, bmesh.types.BMVert)]
            if len(verts) < 2:
                return self.report({"ERROR"}, f"Please, select at least two vertices.")
            coordinates = [true_coordinates(p.co) for p in verts[-2:]]

        # Creating and positioning the new bone
            # Editing selected armature
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")
        context.view_layer.objects.active = armature
        armature.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
            # Adding the bone
        edit_bones = armature.data.edit_bones
        bone = edit_bones.new(self.bone_name)
        bone.head = coordinates[0]
        bone.tail = coordinates[1]

        # Restoring selection and mode context
        bpy.ops.object.mode_set(mode="OBJECT")
        for o in selected_objs: o.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}

class ModifierPropertyGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    identifier: bpy.props.StringProperty()
    value: bpy.props.BoolProperty()

class SelectObjectWithModifiers(bpy.types.Operator):
    bl_idname = "object.select_with_modifier"
    bl_label = "Select Object With Modifiers"
    bl_options = {"REGISTER","UNDO"}
    main = ["SUBSURF", "MIRROR", "BEVEL", "SOLIDIFY", "ARRAY"]


    modifiers : bpy.props.CollectionProperty(type=ModifierPropertyGroup)
    mode : bpy.props.EnumProperty(items=[
        ("exclusive","Exclusive","Ignore selected modifiers"),
        ("inclusive","Inclusive","Ignore non-selected modifiers")
    ],name="Selection Mode",default="exclusive")
    show_only_main : bpy.props.BoolProperty(name="Filter Important Modifiers",description="Show most frequent modifiers. Hide and disable the rest.")

    @classmethod
    def poll(self, context):
        return context.mode == "OBJECT"

    def invoke(self, context, event):
        all_modifiers = [mod for mod in bpy.types.Modifier.bl_rna.properties["type"].enum_items if mod.identifier.startswith("GREASE") != True]
        all_modifiers.sort(key=lambda o: o.identifier)
        main_modifiers = [mod for mod in all_modifiers if mod.identifier.lower() in self.main]
        self.modifiers.clear()
        for modifier in all_modifiers:
            prop = self.modifiers.add()
            prop.name = modifier.name
            prop.identifier = modifier.identifier
            prop.value = False
        
        return self.execute(context)

    def draw(self, context):
        layout = self.layout

        # Modifiers
        row = layout.row()
        col = None
        for i, item in enumerate([mod for mod in self.modifiers if (mod.identifier in self.main) or not self.show_only_main]): # List all modifiers, and filter if needed (only_main)
            if i%20 == 0:
                col = row.column()
            col.box().prop(item, "value", text=item.name)

        # Operator behavior
        row = layout.row()
        icon = "SELECT_" + ("EXTEND" if self.mode == "inclusive" else "SUBTRACT") # Change icon to show selection type
        row.prop(self, "mode", icon=icon)

        icon = "SOLO_" + ("ON" if (only_main := getattr(self, "show_only_main")) else "OFF") # Change icon depending on attribute (ON/OFF)
        row.prop(self, "show_only_main", icon=icon)

    def execute(self, context):
        selected_objects = context.selected_objects
        mode = self.mode == "inclusive"
        sorting_modifiers = [item.identifier for item in self.modifiers if (item.value if not self.show_only_main else item.value and (item.identifier in self.main))] # List all checked modifiers, remove everyone except frequent one if needed (only_main)
        print(sorting_modifiers)
        bpy.ops.object.select_all(action="DESELECT")
        for obj in context.view_layer.objects:
            if obj.type == "MESH":
                for modifier in obj.modifiers:
                    if (modifier.type in sorting_modifiers) == mode:
                        obj.select_set(True)

        return {"FINISHED"}