from math import sqrt
import matplotlib.pyplot as plt

class Vector:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)
    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)
    def __rmul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

class Particle:
    def __init__(self, position, velocity, charge=1.0, mass=1.0):
        self.position=position
        self.velocity=velocity
        self.charge=charge
        self.mass = mass

    def evolve(self, dt=0.01):
        self.position += dt*self.velocity

    def apply_force(self, force, dt=0.0001):
        self.velocity += (dt/self.mass)*force

    def interact_with(self, particle, dt=0.0001):
        dr = self.position-particle.position
        force = (self.charge*particle.charge/dr.length()**3)*dr
        self.apply_force(force)

    def __str__(self):
        return f"Particle({self.position}, {self.velocity}, charge={self.charge}, mass={self.mass})"

class Model:
    def __init__(self, particles):
        self.particles = particles
    def evolve(self, dt=0.0001):
        for i in range(len(self.particles)):
            for i in range(len(self.particles)):
                if i==j:
                    continue
                self.particles[i].interact_with(self.particles[j], dt=dt)
        for i in range(len(self.particles)):
            self.particles[i].evolve(dt)
            
    
particle1 = Particle(Vector(-1.0,0.0,0.0), Vector(0.0,1.0,0.0), mass=1.0, charge =-20.0)
particle2 = Particle(Vector(1.0,0.0,0.0), Vector(0.0,-1.0, 0.0), charge=20.0)
particle3 = Particle(Vector(0.0,0.0,0.0), Vector(0.0, 0.0, 0.2), charge=0.1)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
x1=[]
y1=[]
x2=[]
y2=[]

for t in range(10000):
    x1.append(particle1.position.x)
    y1.append(particle1.position.y)
    x2.append(particle2.position.x)
    y2.append(particle2.position.y)
    particle1.interact_with(particle2)
    particle1.interact_with(particle3)
    particle2.interact_with(particle1)
    particle2.interact_with(particle3)
    particle3.interact_with(particle1)
    particle3.interact_with(particle2)
    particle1.evolve()
    particle2.evolve()
    particle3.evolve()
    #print(particle1, particle2)

ax.plot(x1,y1)
ax.plot(x2,y2)
plt.show()