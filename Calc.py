import bpy
import math
import numpy as np

def exchange_axis(normal,x,y,z):
    pass
    #return [normal_x,normal_y,normal_z]

def angel_vector(normal):
    pass
    #return [angel_x,angel_y,angel_z]

def calc_rigidbodies():
    for i in bpy.context.object.data.polygons:
        point_number = []

        #提取构成面的顶点编号存入point_number
        for j in bpy.context.object.data.polygons[i].vertices:
            point_number.append(j)

        #提取每个面对应的刚体的中心
        loc_x = bpy.context.object.data.polygons[i].center[0]
        loc_y = bpy.context.object.data.polygons[i].center[1]
        loc_z = bpy.context.object.data.polygons[i].center[2]

        #读取面的法向存入faces_normal
        faces_normal = list(bpy.context.object.data.polygons[i].normal)

        point_normal = []
        #坐标系变换
        for k in point_number:
            point_x = bpy.context.object.data.vertices[k].co[0]
            point_y = bpy.context.object.data.vertices[k].co[1]
            point_z = bpy.context.object.data.vertices[k].co[2]
            point_normal.append(exchange_axis(faces_normal,point_x,point_y,point_z))

        #计算刚体尺寸
        list_nx = []
        list_ny = []
        list_nz = []

        for m in point_normal:
            list_nx.append(m[0])
            list_ny.append(m[1])
            list_nz.append(m[2])

        list_nx = sorted(list_nx)
        list_ny = sorted(list_ny)
        list_nz = sorted(list_nz)

        max_middle_x = (list_nx[-2] + list_nx[-1]) / 2
        min_middle_x = (list_nx[0] + list_nx[1]) / 2
        max_middle_y = (list_ny[-2] + list_ny[-1]) / 2
        min_middle_y = (list_ny[0] + list_ny[1]) / 2
        max_middle_z = (list_nz[-2] + list_nz[-1]) / 2
        min_middle_z = (list_nz[0] + list_nz[1]) / 2

        size_x = (max_middle_x + min_middle_x) / 2
        size_y = (max_middle_z + min_middle_z) / 2
        size_z = (max_middle_y + min_middle_y) / 2

        #计算刚体旋转
        faces_normal = np.array(faces_normal)
        world_vector = np.array([0, 1, 0])
        for i in range(3):
            faces_normal[i] = -faces_normal[i]

        print(faces_normal)
        tr1 = np.array(faces_normal)
        faces_normal[2] = 0
        tr2 = np.array(faces_normal)
        len2 = np.linalg.norm(tr2)

        # 转Z
        cos_z = np.dot(world_vector, tr1) / len2
        if tr1[0] >= 0:
            angel_z = -np.arccos(cos_z)
        else:
            angel_z = np.arccos(cos_z)
        print(angel_z)

        # 转X
        cos_x = np.dot(tr1, tr2) / len2
        if tr1[2] >= 0:
            angel_x = np.arccos(cos_x)
        else:
            angel_x = -np.arccos(cos_x)
        print(angel_x)

        # 转Y
        world_z = np.array([0, 0, 1])
        tr1_x0 = np.cross(tr1, world_z)
        tr1_z = np.cross(tr1_x0, tr1)