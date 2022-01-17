import bpy
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

        #转Z
        cos_z = np.dot(world_vector, tr1) / len2
        if cos_z > 1:
            cos_z = 1
        if tr1[0] >= 0:
            angel_z = -np.arccos(cos_z)
        else:
            angel_z = np.arccos(cos_z)
        print(angel_z)

        #转X
        cos_x = np.dot(tr1, tr2) / len2
        if cos_x > 1:
            cos_x = 1
        if tr1[2] >= 0:
            angel_x = np.arccos(cos_x)
        else:
            angel_x = -np.arccos(cos_x)
        print(angel_x)

        #转Y
        if abs(tr1[2]) < 0.001:
            angel_y = 0
        else:
            poi1 = bpy.context.object.data.vertices[point_number[0]].co
            poi2 = bpy.context.object.data.vertices[point_number[1]].co

            poi1 = np.array(poi1)
            poi2 = np.array(poi2)
            loc_vec = np.array(loc)
            poi1 = poi1 - loc_vec
            poi2 = poi2 - loc_vec
            faces_normal_x0 = (poi1 + poi2) / 2
            faces_normal_z = np.cross(faces_normal_x0,tr1)
            faces_normal_x = np.cross(tr1,faces_normal_z)
            len_fx = np.linalg.norm(faces_normal_x)

            rm_x = np.asarray([[np.cos(angel_z),-np.sin(angel_z)],[np.sin(angel_z),np.cos(angel_z)]])
            new_x = np.dot(np.array([1,0]),rm_x)
            new_x = list(new_x)
            new_x.append(0)
            new_x = np.array(new_x)
            len_nx = np.linalg.norm(new_x)

            cos_y = np.dot(new_x,faces_normal_x) / (len_fx * len_nx)
            if cos_y > 1:
                cos_y = 1
            if faces_normal_x[2] >= 0:
                angel_y = np.arccos(cos_y)
            else:
                angel_y = -np.arccos(cos_y)

        #计算尺寸
        size_x = np.linalg.norm(faces_normal_x0)

        size_y = 0
        for qu in point_number:
            point_l = bpy.context.object.data.vertices[qu].co)
            point_v = np.array(point_l) - np.array(loc)
            lenth = np.dot(point_v,tr1)
            if size_y < lenth:
                size_y = lenth

        size_z