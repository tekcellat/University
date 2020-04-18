from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

x, y = map(float, input('Введите координаты первой точки: ').split())
A = (x, y)
x, y = map(float, input('Введите координаты второй точки: ').split())
B = (x, y)
x, y = map(float, input('Введите координаты третьей точки: ').split())
C = (x, y)
dots = (A, B, C)

ab = sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
ac = sqrt((A[0]-C[0])**2 + (A[1]-C[1])**2)
bc = sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)

per = ab + ac+ bc
Ox = (bc * A[0] + ac * B[0] + ab * C[0])/(per)
Oy = (bc * A[1] + ac * B[1] + ab * C[1])/(per)
O = (Ox, Oy)

p = per / 2
r = sqrt((p - ab)*(p - ac)*(p - bc)/p)

fig, ax = plt.subplots()

for dot in dots:
    plt.scatter(dot[0], dot[1])
plt.scatter(O[0], O[1])

plt.plot([A[0], B[0]], [A[1], B[1]])
plt.plot([C[0], B[0]], [C[1], B[1]])
plt.plot([A[0], C[0]], [A[1], C[1]])

circle = Circle((Ox, Oy), r)
patches = [circle]
p = PatchCollection(patches, alpha=0.4)
ax.add_collection(p)

plt.grid(True)
plt.show()

            
            
        
