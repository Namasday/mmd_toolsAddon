import numpy as np

angel_z = 0.5
a = np.asarray([[np.cos(angel_z),-np.sin(angel_z)],[np.sin(angel_z),np.cos(angel_z)]])
b = [1,1]
c = np.dot(b,a)
print(c)