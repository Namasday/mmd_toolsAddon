bl_info = {
    "name": "mmd_tools物理扩展插件",
    "author": "Iyinpic",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > MMD Tools Physical Addon Panel",
    "description": "根据拓扑模型一键建立物理骨骼、物理刚体和Joint脚本",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

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
        # '''创建MMD刚体（物理类型，方块形状）'''
        # bpy.ops.mmd_tools.rigid_body_add(rigid_type='1',rigid_shape='BOX')
        #
        # '''移动到每个刚体到对应面的位置'''
        # for i in range(3):  #按世界坐标X,Y,Z分别把计算出来的变换代入到刚体的位置与旋转三维
        #     bpy.context.object.location[i] = 0
        #     bpy.context.object.rotation_euler[i] = 0    #计算出来的0处的旋转数据是弧度

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