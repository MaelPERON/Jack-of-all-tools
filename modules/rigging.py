import bpy
from random import choices, seed

chs = "abcdefghijklmnopqrstuvxyz0123456789"

class GetBonesHierarchy(bpy.types.Operator):
    bl_idname = "armature.joat_get_hierarchy"
    bl_label = "Get Bones Hierarchy"

    @classmethod
    def poll(self, context):
        return context.mode in ["EDIT_ARMATURE","POSE"]
    
    def get_id(self, bone_name, n=5):
        global chs
        if n < 0: return "undefined"
        seed(bone_name)
        return ''.join(choices(chs, k=n))

    def execute(self, context):
        obj = context.active_object
        bones = context.selected_bones if context.mode == "EDIT_ARMATURE" else [bone.bone for bone in context.selected_pose_bones]
        bones = {bone.name: bone for bone in bones}
        output = ["flowchart BT"]

        for bone in bones.values():
            parent = getattr(bone, "parent", None)
            use_connect = getattr(bone, "use_connect", None)
            
            line = "\t" + self.get_id(bone.name) + f"[{bone.name}]" + " "
            if parent is not None:
                line += "==>" if bone.use_connect else "-->"
                line += f" {self.get_id(parent.name)}"
                if parent.name not in bones.keys():
                    line += f"[{parent.name}]"
            
            output.append(line)
            
            for constraint in obj.pose.bones.get(bone.name).constraints:
                if (target := getattr(constraint, "target", None)) is not None and obj == target:
                    if (subtarget := getattr(constraint, "subtarget", None)) is not None:
                        constraint_line = f"\t{self.get_id(bone.name)} -. {constraint.type} .-> {self.get_id(subtarget)}"
                        if subtarget not in bones.keys():
                            constraint_line += f"[{subtarget}]"
                        output.append(constraint_line)

        self.report({"INFO"}, '\n'.join(output))
        self.report({"INFO"}, f"Flowchart successfully generated for {len(bones)} bones. Click to see.")
        return {"FINISHED"}