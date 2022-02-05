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
    bl_label = "添加骨骼"

    def execute(self,context):
        calcfun.add_phybones()
        return {"FINISHED"}

@register_list
class PhyBoneMask_OT_Add(bpy.types.Operator):
    bl_idname = "phybonemask.add"
    bl_label = "创建骨骼遮罩"

    origin = []

    @classmethod
    def poll(cls,context):
        return len(cls.origin) == 0

    def execute(self,context):
        self.obj = context.object
        PhyBoneMask_OT_Add.origin = calcfun.add_phybonemask(context)
        return {"FINISHED"}

@register_list
class PhyBoneMask_OT_Release(bpy.types.Operator):
    bl_idname = "phybonemask.release"
    bl_label = "释放骨骼遮罩"

    @classmethod
    def poll(cls,context):
        return len(PhyBoneMask_OT_Add.origin) > 0

    def execute(self,context):
        calcfun.release_phybonemask(PhyBoneMask_OT_Add.origin)
        PhyBoneMask_OT_Add.origin = []
        return {"FINISHED"}