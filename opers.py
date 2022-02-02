import bpy

from . import register_list

from . import calcfun

import mmd_tools

@register_list
class RigidBodies_OT_Add(bpy.types.Operator):
    bl_idname = "rigidbodies.add"
    bl_label = "添加刚体群"

    def execute(self,context):
        pol_list = calcfun.get_polygons()
        calcfun.add_rigidbodies(pol_list)
        return {"FINISHED"}

@register_list
class AdjustRBSize(bpy.types.Operator):
    bl_idname = "adjust.size"
    bl_label = "adjust all selected rigidbodies size"
    bl_options = {"REGISTER"}

    coe : bpy.props.FloatVectorProperty(name="size",subtype="XYZ",default=[0,0,0])

    def execute(self, context):
        # 赋值给刚体属性
        for obj in bpy.context.selected_objects:
            for i in range(3):
                obj.mmd_rigid.size[i] += self.coe[i]

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