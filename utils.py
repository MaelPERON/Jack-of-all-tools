def getIndex(list, index):
    return list[index] if index < len(list) else None

def placeOperator(layout, Operator):
    kwargs = {}
    if (icon := getattr(Operator, "bl_icon", None)):
        kwargs['icon'] = icon
    layout.operator(Operator.bl_idname, text=Operator.bl_label, **kwargs)