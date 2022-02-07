import bpy
import numpy as np

import mmd_tools

def get_polygons():
    pol_list = []
    obj_list = bpy.context.selected_objects

    if bpy.context.mode == 'OBJECT':
        for obj in obj_list:
            pol_list.append([obj,obj.data.polygons])
    if bpy.context.mode == 'EDIT_MESH':
        bpy.ops.object.editmode_toggle()    #从编辑模式切换回物体模式，确定其选择的面
        for obj in obj_list:
            pol_slist = []      #选择的面存入该列表
            for pol in obj.data.polygons:
                if pol.select:
                    pol_slist.append(pol)

            pol_list.append([obj, pol_slist])

    return pol_list

def add_rigidbodies(lst):
    obj_selected = []

    for obj in lst:
        #名称控制
        check = False
        obj1_lst = []
        rname = obj[0].name + '.Rigid.'
        for obj1 in bpy.data.objects:
            if rname in obj1.name:
                check = True
                obj1_lst.append(obj1)

        if check:
            lst1 = []
            for obj1 in obj1_lst:
                lst = obj1.name.split(sep='.')
                index = int(lst[2])
                lst1.append(index)

            lst1.sort()
            quantity = lst1[-1] + 1
        else:
            quantity = 0

        for pol in obj[1]:
            #提取构成面的顶点编号存入point_number
            point_number = list(pol.vertices)

            #提取每个面对应的刚体的中心
            loc = pol.center

            #读取面的法向存入faces_normal
            faces_normal = pol.normal

            #计算刚体旋转
            faces_normal = np.array(faces_normal)
            world_vector = np.array([0, 1, 0])
            for i in range(3):
                faces_normal[i] = -faces_normal[i]

            tr1 = np.array(faces_normal)
            faces_normal[2] = 0
            tr2 = np.array(faces_normal)
            len2 = np.linalg.norm(tr2)

            if tr1[0] == 0 and tr1[1] == 0:
                angel_z = 0
                if tr1[2] > 0:
                    angel_x = np.pi / 2
                else:
                    angel_x = -np.pi / 2
            else:
                #转Z
                cos_z = np.dot(world_vector, tr1) / len2
                if cos_z > 1:
                    cos_z = 1
                if tr1[0] >= 0:
                    angel_z = -np.arccos(cos_z)
                else:
                    angel_z = np.arccos(cos_z)

                #转X
                cos_x = np.dot(tr1, tr2) / len2
                if cos_x > 1:
                    cos_x = 1
                if tr1[2] >= 0:
                    angel_x = np.arccos(cos_x)
                else:
                    angel_x = -np.arccos(cos_x)

            #转Y
            poi1 = obj[0].data.vertices[point_number[0]].co
            poi2 = obj[0].data.vertices[point_number[1]].co

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
                new_x = [np.cos(angel_z),np.sin(angel_z),0]
                new_x = np.array(new_x)

                cos_y = np.dot(new_x,faces_normal_x) / len_fx
                if cos_y > 1:
                    cos_y = 1
                if faces_normal_x0[2] >= 0:
                    angel_y = -np.arccos(cos_y)
                else:
                    angel_y = np.arccos(cos_y)

            #计算尺寸x
            size_x = np.linalg.norm(faces_normal_x0)

            # 计算尺寸y
            size_y = 0
            sum = 0
            times = 0
            for qu in point_number:
                point_l = obj[0].data.vertices[qu].co
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
            name = obj[0].name + '.Rigid.' + str(quantity)
            name_en = obj[0].name + '.RigidE.' + str(quantity)
            quantity += 1

            if size_y < 0.005:
                size_y = 0.005

            size_x = 0.2 * size_x
            size_y = 0.2 * size_y
            size_z = 0.2 * size_z

            bpy.ops.mmd_tools.rigid_body_add(name_j=name,
                                             name_e=name_en,
                                             rigid_type='1',
                                             rigid_shape='BOX',
                                             size=(size_x,size_y,size_z))

            bpy.data.objects[name].location[0] = loc[0]
            bpy.data.objects[name].location[1] = loc[1]
            bpy.data.objects[name].location[2] = loc[2]
            bpy.data.objects[name].rotation_euler[2] = angel_z
            bpy.data.objects[name].rotation_euler[0] = angel_x
            bpy.data.objects[name].rotation_euler[1] = angel_y

            obj_selected.append(name)
            bpy.data.objects[name].select = False

    for name in obj_selected:
        bpy.data.objects[name].select = True

def rbbone_connect(context):
    bone_list = []

    #切换骨骼的编辑模式确定骨骼中心坐标
    rb_list = context.selected_objects
    try:
        arm = context.object.constraints["mmd_tools_rigid_parent"].target
        active = context.object
    except:
        arm = rb_list[0].constraints["mmd_tools_rigid_parent"].target
        active = rb_list[0]

    context.view_layer.objects.active = arm
    bpy.ops.object.editmode_toggle()

    for bone in arm.data.edit_bones:
        if bone.use_deform:
            bone_list.append(bone)

    for rb in context.selected_objects:
        dis_list = []
        for bone in bone_list:
            vec = np.array(rb.location - bone.center)
            distance = np.linalg.norm(vec)
            dis_list.append(distance)

        i = dis_list.index(min(dis_list))
        rb.mmd_rigid.bone = bone_list[i].name

    #切回选择
    bpy.ops.object.editmode_toggle()
    context.view_layer.objects.active = active

def add_phybones():
    if bpy.context.mode == 'EDIT_MESH':
        bpy.ops.object.editmode_toggle()    #从编辑模式切换回物体模式，确定其选择的边

    obj_list = bpy.context.selected_objects
    bpy.ops.object.select_hierarchy(direction='PARENT',extend=False)
    arm = bpy.context.object

    #取消选择
    for bon in arm.data.bones:
        bon.select = False
        bon.select_head = False
        bon.select_tail = False

    bpy.ops.object.editmode_toggle()

    for obj in obj_list:
        edge_list = []      #选择的边存入该列表
        for edge in obj.data.edges:
            if edge.select:
                edge_list.append(edge)

        #将选择边列表分成连接边列表的列表
        edge_connect = []
        for edge in edge_list:
            edge_list.remove(edge)
            front = edge.vertices[0]
            behind = edge.vertices[1]
            point_index_list = [front,behind]

            while True:
                for edge1 in edge_list:
                    if behind == edge1.vertices[0]:
                        behind = edge1.vertices[1]
                        point_index_list.append(behind)
                        edge_list.remove(edge1)
                        break

                    elif behind == edge1.vertices[1]:
                        behind = edge1.vertices[0]
                        point_index_list.append(behind)
                        edge_list.remove(edge1)
                        break
                else:
                    break

            while True:
                for edge1 in edge_list:
                    if front == edge1.vertices[0]:
                        front = edge1.vertices[1]
                        point_index_list.insert(0,front)
                        edge_list.remove(edge1)
                        break

                    elif front == edge1.vertices[1]:
                        front = edge1.vertices[0]
                        point_index_list.insert(0,front)
                        edge_list.remove(edge1)
                        break
                else:
                    break

            edge_connect.append(point_index_list)

        #名称控制
        check = False
        bon_lst = []
        for bon in arm.data.bones:
            if obj.name in bon.name:
                check = True
                bon_lst.append(bon)

        if check:
            lenth = len(obj.name)
            lst1 = []
            for bon in bon_lst:
                lst = bon.name.split(sep='.')
                index = int(lst[0][lenth:])
                lst1.append(index)

            lst1.sort()
            i = lst1[-1] + 1
        else:
            i = 0

        #建立骨骼
        for point_index_list in edge_connect:
            #根据顺序建立骨骼
            bone = arm.data.edit_bones.new(name=obj.name + str(i))
            bone.head = obj.data.vertices[point_index_list[0]].co
            bone.tail = obj.data.vertices[point_index_list[1]].co
            for index,value in enumerate(point_index_list):
                if index < 2:
                    continue
                else:
                    vector_miner = obj.data.vertices[value].co - obj.data.vertices[point_index_list[index-1]].co

                bpy.ops.armature.extrude_move(TRANSFORM_OT_translate={"value": vector_miner})

            # 取消选择
            bpy.ops.object.editmode_toggle()
            for bon in arm.data.bones:
                bon.select_tail = False
            bpy.ops.object.editmode_toggle()

            i += 1

def add_phybonemask(context):
    if bpy.context.mode == 'EDIT_ARMATURE':
        bpy.ops.object.editmode_toggle()    #切换物体模式确定选择的骨骼

    mask = []
    origin = []
    for bone in context.object.data.bones:
        if bone.use_deform:
            origin.append(bone)
            bone.use_deform = False

        if bone.select:
            mask.append(bone)

    for bone in mask:
        bone.use_deform = True

    return origin

def release_phybonemask(origin):
    if bpy.context.mode == 'EDIT_ARMATURE':
        bpy.ops.object.editmode_toggle()

    for bone in origin:
        bone.use_deform = True