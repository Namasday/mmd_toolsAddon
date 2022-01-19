bl_info = {
    "name": "mmd_tools物理扩展插件",
    "author": "Iyinpic",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > MMD Tools Physical Addon Panel",
    "description": "根据拓扑模型一键建立物理骨骼、物理刚体和Joint脚本",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
from mmd_toolsAddon import calcfun
from mmd_toolsAddon import check

class RigidBodies_Add(bpy.types.Operator):
    bl_idname = "rigidbodies.add"
    bl_label = "添加刚体群"

    def execute(self,context):
        pol_list = calcfun.get_polygons()
        calcfun.add_rigidbodies(pol_list)
        return {"FINISHED"}

class Joint_Add(bpy.types.Operator):
    bl_idname = "joint.add"
    bl_label = "添加Joint"

    def execute(self,context):
        return {"FINISHED"}

class PhyBone_Add(bpy.types.Operator):
    bl_idname = "phybone.add"
    bl_label = "添加物理骨骼"

    def execute(self,context):
        return {"FINISHED"}

class RB_PT_View3D(bpy.types.Panel):
    bl_idname = "MMDPA_RB"
    bl_label = "刚体"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMDPA"

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.operator("rigidbodies.add",text="添加刚体群",icon="CUBE")
        row.enabled = check.check_mode()

class Joint_PT_View3D(bpy.types.Panel):
    bl_idname = "MMDPA_Joint"
    bl_label = "Joint"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMDPA"

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.operator("joint.add",text="添加Joint",icon="EMPTY_AXIS")

class Bone_PT_View3D(bpy.types.Panel):
    bl_idname = "MMDPA_Bone"
    bl_label = "骨骼"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MMDPA"

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.operator("phybone.add",text="添加物理骨骼",icon="BONE_DATA")

list_cls = [RB_PT_View3D,
            RigidBodies_Add,
            Joint_PT_View3D,
            Joint_Add,
            Bone_PT_View3D,
            PhyBone_Add]

def register():
    for cls in list_cls:
        bpy.utils.register_class(cls)

def unregister():
    for cls in list_cls:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()