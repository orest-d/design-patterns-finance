import numpy as np
import matplotlib.pyplot as plt

def electrostatic_force(position, charge):
    force = np.zeros(position.shape, np.float)

    for i in range(len(position)):
        for j in range(len(position)):
            if i==j:
                continue
            dr = position[i]-position[j]
            dr2= np.sum(dr*dr)

            force[i] += charge[i]*charge[j]*dr2**-(3/2)*dr
    return force

def evolve_euler(position, velocity, mass, force, dt=0.0001):
    position += dt*velocity
    velocity += ((dt/mass)*force.T).T

position = np.array([
    [-1.0,0.0,0.0],
    [1.0,0.0,0.0],
    [0.0,0.0,0.0]
    ])
velocity = np.array([
    [0.0,10.0,0.0],
    [0.0,-10.0, 0.0],
    [0.0, 0.0, 0.2]
    ])
mass = np.array([
    1.0,
    1.0,
    1.0
    ])
charge = np.array([
    -20.0,
    20.0,
    0.1
    ])


fig, ax = plt.subplots()
x1=[]
y1=[]
x2=[]
y2=[]
for t in range(10000):
    force = electrostatic_force(position, charge)
    #print (force)
    evolve_euler(position, velocity, mass, force) 
    x1.append(position[0][0])
    y1.append(position[0][1])
    x2.append(position[1][0])
    y2.append(position[1][1])
ax.plot(x1,y1)
ax.plot(x2,y2)
plt.show()
