import bpy

from . import register_list

from . import calcfun

@register_list
class RigidBodies_OT_Add(bpy.types.Operator):
    bl_idname = "rigidbodies.add"
    bl_label = "添加刚体群"

    def execute(self,context):
        pol_list = calcfun.get_polygons()
        calcfun.add_rigidbodies(pol_list)
        return {"FINISHED"}

@register_list
class Joint_OT_Add(bpy.types.Operator):
    bl_idname = "joint.add"
    bl_label = "添加Joint"

    def execute(self,context):
        return {"FINISHED"}

@register_list
class PhyBone_OT_Add(bpy.types.Operator):
    bl_idname = "phybone.add"
    bl_label = "添加物理骨骼"

    def execute(self,context):
        return {"FINISHED"}