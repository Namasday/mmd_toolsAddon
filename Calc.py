import bpy
import numpy as np

def add_rigidbodies(coe_x=1,coe_y=1,coe_z=1):
    name_source = bpy.context.object.name
    quantity = 0

    for i in bpy.context.object.data.polygons:
        point_number = []

        #提取构成面的顶点编号存入point_number
        for j in bpy.context.object.data.polygons[i].vertices:
            point_number.append(j)

        #提取每个面对应的刚体的中心
        loc = bpy.context.object.data.polygons[i].center

        #读取面的法向存入faces_normal
        faces_normal = bpy.context.object.data.polygons[i].normal

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
        len_fz = np.linalg.norm(faces_normal_z)

        if abs(tr1[2]) < 0.001:
            angel_y = 0
        else:
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

        #计算尺寸x
        size_x = np.linalg.norm(faces_normal_x0)

        # 计算尺寸y
        size_y = 0
        sum = 0
        times = 0
        for qu in point_number:
            point_l = bpy.context.object.data.vertices[qu].co)
            point_v = np.array(point_l) - np.array(loc)
            lenth = abs(np.dot(point_v,tr1))
            if size_y < lenth:
                size_y = lenth

            director = np.dot(point_v,faces_normal_z)
            if director > 0:
                sum += director / len_fz    #求点对中心的向量在法向坐标系z轴的投影
                times += 1

        # 计算尺寸z
        size_z = sum / times

        #根据计算数据新建刚体并导入数据
        name = name_source + '.Rigid.' + str(quantity)
        name_en = name_source + '.RigidE.' + str(quantity)
        quantity += 1

        size_x = 0.2 * coe_x * size_x
        size_y = 0.2 * coe_y * size_y
        size_z = 0.2 * coe_z * size_z

        bpy.ops.mmd_tools.rigid_body_add(name_j=name, name_e=name_en, rigid_type='1', rigid_shape='BOX',size=(size_x,size_y,size_z))

        bpy.data.objects[name].location[0] = loc[0]
        bpy.data.objects[name].location[1] = loc[1]
        bpy.data.objects[name].location[2] = loc[2]
        bpy.data.objects[name].rotation_euler[2] = angel_z
        bpy.data.objects[name].rotation_euler[0] = angel_x
        bpy.data.objects[name].rotation_euler[1] = angel_y