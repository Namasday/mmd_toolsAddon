import bpy

from . import register_list
from . import calcfun

import mmd_tools

@register_list
class RB_PT_View3D(bpy.types.Panel):
    bl_idname = "MMDPA_PT_RB"
    bl_label = "刚体"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMDPA"

    def draw(self,context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.operator("rigidbodies.add",text="添加刚体群",icon="CUBE")

        col = layout.column()
        col.prop(scene,'Coe',text="调整刚体尺寸")

        row = layout.row()
        row.operator("rigidbodies.mirror",text="添加镜像刚体",icon="CUBE")
        row.operator("rbbone.connect", text="刚体附着骨骼", icon="BONE_DATA")

@register_list
class Joint_PT_View3D(bpy.types.Panel):
    bl_idname = "MMDPA_PT_Joint"
    bl_label = "Joint"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMDPA"

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.operator("joint.add",text="添加Joint",icon="EMPTY_AXIS")
        row.enabled = False

@register_list
class Bone_PT_View3D(bpy.types.Panel):
    bl_idname = "MMDPA_PT_Bone"
    bl_label = "骨骼"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMDPA"

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.operator("phybone.add",text="添加骨骼",icon="BONE_DATA")

        row = layout.row(align=True)
        row.operator("phybonemask.add",text="创建骨骼遮罩",icon="CLIPUV_DEHLT")
        row.operator("phybonemask.release", text="释放骨骼遮罩", icon="CLIPUV_HLT")