import bpy
from bpy.types import Panel

class Pannel_MMDPA(object):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' if bpy.app.version < (2, 80, 0) else 'UI'
    bl_category = 'MMDPA'

class RigidBodies_Add(Pannel_MMDPA, Panel):
    bl_idname = "RBA"
    bl_label = "转换为刚体群"

    def execute(self,context):
        pass

class PhysicalBone_Add:
    pass

class Joint_Add:
    pass

def register():
    bpy.bpy.utils.register_class(Pannel_MMDPA)

def unregister():
    bpy.bpy.utils.unregister_class(Pannel_MMDPA)

if __name__ == "__main__":
    register()