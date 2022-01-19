import bpy

def check_mode():
    if bpy.context.mode == 'OBJECT':
        if bpy.context.selected_objects:
            return True
        else:
            return False
    else:
        return False