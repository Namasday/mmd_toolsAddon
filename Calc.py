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
        loc = bpy.context.object.data.polygons[i].center

        #读取面的法向存入faces_normal
        faces_normal = list(bpy.context.object.data.polygons[i].normal)

        point_normal = []
        #坐标系变换
        for k in point_number:
            point_loc = bpy.context.object.data.vertices[k].co
            point_normal.append(exchange_axis(faces_normal,point_loc)

        #计算刚体尺寸


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
        if cos_z > 1:
            cos_z = 1
        if tr1[0] >= 0:
            angel_z = -np.arccos(cos_z)
        else:
            angel_z = np.arccos(cos_z)
        print(angel_z)

        # 转X
        cos_x = np.dot(tr1, tr2) / len2
        if cos_x > 1:
            cos_x = 1
        if tr1[2] >= 0:
            angel_x = np.arccos(cos_x)
        else:
            angel_x = -np.arccos(cos_x)
        print(angel_x)

        # 转Y
        poi1 = bpy.context.object.data.vertices[point_number[-1]].co
        poi2 = bpy.context.object.data.vertices[point_number[-2]].co

        poi1 = np.array(poi1)
        poi2 = np.array(poi2)

