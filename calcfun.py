import bpy
import numpy as np

import mmd_tools

def get_polygons(context):
    pol_list = []
    obj_list = bpy.context.selected_objects

    if context.mode == 'OBJECT':
        for obj in obj_list:
            pol_list.append([obj,obj.data.polygons])
    if context.mode == 'EDIT_MESH':
        bpy.ops.object.editmode_toggle()    #从编辑模式切换回物体模式，确定其选择的面
        for obj in obj_list:
            pol_slist = []      #选择的面存入该列表
            for pol in obj.data.polygons:
                if pol.select:
                    pol_slist.append(pol)

            pol_list.append([obj, pol_slist])

    return pol_list

def add_rigidbodies(context,lst):
    obj_selected = []

    for obj in lst:
        #名称控制
        name0 = obj[0].name.split(sep='.')
        check = False
        obj1_lst = []
        rname = name0[0] + '.Rigid.'
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
            point_number = pol.vertices

            #提取每个面对应的刚体的中心
            loc = pol.center

            #读取面的法向存入faces_normal
            faces_normal = pol.normal

            #计算刚体旋转
            faces_normal = np.array(faces_normal)
            world_vector = np.array([0, 1, 0])
            faces_normal = -faces_normal

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
            name = name0[0] + '.Rigid.' + str(quantity)
            name_en = name0[0] + '.RigidE.' + str(quantity)
            quantity += 1

            if size_y < 0.005:
                size_y = 0.005

            size = [size_x * 0.2, size_y * 0.2, size_z * 0.2]

            bpy.ops.mmd_tools.rigid_body_add(name_j=name,
                                             name_e=name_en,
                                             rigid_type='1',
                                             rigid_shape='BOX',
                                             size=size)

            context.object.location = loc
            context.object.rotation_euler = [angel_x,angel_y,angel_z]

            obj_selected.append(context.object)

    for obj in obj_selected:
        obj.select = True

def mirror_rigidbodies(context):
    obj_lst = context.selected_objects
    obj_selected = []
    for obj in obj_lst:
        name = obj.mmd_rigid.name_j + "X"
        name_en = obj.mmd_rigid.name_e + "X"
        size = obj.mmd_rigid.size * 0.2
        type = obj.mmd_rigid.type
        shape = obj.mmd_rigid.shape
        bpy.ops.mmd_tools.rigid_body_add(name_j=name,
                                         name_e=name_en,
                                         rigid_type=type,
                                         rigid_shape=shape,
                                         size=size)
        context.object.location = [-obj.location[0],obj.location[1],obj.location[2]]
        context.object.rotation_euler = [obj.rotation_euler[0],-obj.rotation_euler[1],-obj.rotation_euler[2]]
        obj_selected.append(context.object)

    for obj in obj_selected:
        obj.select = True

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
        name0 = obj.name.split(sep='.')
        name0 = name0[0]
        check = False
        bon_lst = []
        for bon in arm.data.bones:
            if name0 in bon.name:
                check = True
                bon_lst.append(bon)

        if check:
            lenth = len(name0)
            lst1 = []
            for bon in bon_lst:
                lst = bon.name.split(sep='.')
                try:
                    index = int(lst[0][lenth:])
                except:
                    index = 0

                lst1.append(index)

            lst1.sort()
            i = lst1[-1] + 1
        else:
            i = 0

        #建立骨骼
        for point_index_list in edge_connect:
            #根据顺序建立骨骼
            bone = arm.data.edit_bones.new(name=name0 + str(i))
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