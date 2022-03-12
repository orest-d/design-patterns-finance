import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

State = namedtuple('State',["position", "velocity", "mass", "charge"])

def electrostatic_force(state):
    force = np.zeros(state.position.shape, np.float)

    for i in range(len(state.position)):
        for j in range(len(state.position)):
            if i==j:
                continue
            dr = state.position[i]-state.position[j]
            dr2= np.sum(dr*dr)

            force[i] += state.charge[i]*state.charge[j]*dr2**-(3/2)*dr
    return force

def evolve_euler(state, force_calculator, dt=0.0001):
    force = force_calculator(state)
    position = state.position + dt*state.velocity
    velocity = state.velocity + ((dt/state.mass)*force.T).T
    return State(position, velocity, mass=state.mass, charge=state.charge)

def evolve_leap_frog(state, force_calculator, dt=0.0001):
    force = force_calculator(state)
    position = state.position + dt*state.velocity
    velocity = state.velocity + ((dt/state.mass)*force.T).T
    return State(position, velocity, mass=state.mass, charge=state.charge)


state = State( 
    position = np.array([
        [-1.0,0.0,0.0],
        [1.0,0.0,0.0],
        [0.0,0.0,0.0]
        ]),
    velocity = np.array([
        [0.0,10.0,0.0],
        [0.0,-10.0, 0.0],
        [0.0, 0.0, 0.2]
        ]),
    mass = np.array([
        1.0,
        1.0,
        1.0
        ]),
    charge = np.array([
        -20.0,
        20.0,
        0.1
        ])
)


def evaluate_coordinates(state, evolve, force_calculator, steps=10000):
    x=[[] for i in range(len(state.position))]
    y=[[] for i in range(len(state.position))]
    z=[[] for i in range(len(state.position))]

    for t in range(steps):
        for i in range(len(state.position)):
            x[i].append(state.position[i][0])
            y[i].append(state.position[i][1])
            z[i].append(state.position[i][2])
        state = evolve(state, force_calculator)
    return x,y,z


fig, ax = plt.subplots()
x,y,z = evaluate_coordinates(state, evolve_euler, electrostatic_force)
ax.plot(x[0],y[0])
ax.plot(x[1],y[1])
plt.show()