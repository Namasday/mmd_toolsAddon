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

list_cls = []
def register_list(cls):
    list_cls.append(cls)
    return cls

from . import (
    opers,
    panel,
    properties
    )

def register():
    properties.props()

    for cls in list_cls:
        bpy.utils.register_class(cls)

def unregister():
    for cls in list_cls:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()