import numpy as np

world_vector = np.array([0,1,0])     #世界坐标系的y轴
faces_normal = [0.816,-0.561,-0.142]      #变换后的坐标系的y轴
for i in range(3):
    faces_normal[i] = -faces_normal[i]

print(faces_normal)
tr1 = np.array(faces_normal)
faces_normal[2] = 0
tr2 = np.array(faces_normal)
len2 = np.linalg.norm(tr2)

#转Z
cos_z = np.dot(world_vector,tr1) / len2
if tr1[0] >= 0:
    angel_z = -np.arccos(cos_z)
else:
    angel_z = np.arccos(cos_z)
print(angel_z)

#转X
cos_x = np.dot(tr1,tr2) / len2
if tr1[2] >= 0:
    angel_x = np.arccos(cos_x)
else:
    angel_x = -np.arccos(cos_x)
print(angel_x)

#转Y
world_z = np.array([0,0,1])
tr1_x0 = np.cross(tr1,world_z)
tr1_z = np.cross(tr1_x0,tr1)