def getIndex(list, index):
    return list[index] if index < len(list) else None

def placeOperator(layout, Operator):
    kwargs = {}
    if (icon := getattr(Operator, "bl_icon", None)):
        kwargs['icon'] = icon
    layout.operator(Operator.bl_idname, text=Operator.bl_label, **kwargs)

def isMetarig(obj):
    if not (obj and obj.data and obj.type == 'ARMATURE'):
        return False
    if 'rig_id' in obj.data:
        return False
    for b in obj.pose.bones:
        if b.rigify_type != "":
            return True
    return False