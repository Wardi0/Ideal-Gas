import numpy as np
from Velocity import Velocity
from Position import Position
from Vector import Vector
from errors import *
class Particle:
    """
    Class that represents the state of an individual gas molecule

    Has the following attributes:
    self.position -> The particle's position (Position)
    self.velocity -> The particle's velocity (Velocity)
    self.mass -> The particle's mass (float)
    self.radius - > The particle's radius (float)
    """

    def __init__(self, initial_position, initial_velocity, mass, radius):
        """
        Initialisation arguments:
        
        initial_position - Position- or array-like type object representing the particle's initial position
        initial_velocity - Velocity- or array-like type object representing the particle's initial velocity 
        mass - float or int type value representing the particle's mass
        radius - float or int type value representing the particle's radius
        """
        if type(initial_position) == Position:
            self.position = initial_position
        else:
            self.position = Position(initial_position)
        if type(initial_velocity) == Velocity:
            self.velocity = initial_velocity
        else:
            self.velocity = Velocity(initial_velocity)
        self.mass = mass
        self.radius = radius

    def __repr__(self):
        return '<Position: {}, Velocity: {}, Mass: {}, Radius: {}>'.format(self.position.components, 
        self.velocity.components, self.mass, self.radius)

    def update(self, time_step):
        """
        Updates the particle's position over a given time step

        time_step - float or int value representing the time over which to propagate the particle
        """
        self.position.propagate(self.velocity, time_step)

    def overlap(self, other):
        """ 
        Returns True if the particles are overlapping in space, otherwise returns False

        other - Particle type object to check for overlap with
        """
        return (self.position - other.position).magnitude() < self.radius + other.radius

    def kinetic_energy(self):
        """
        Returns the kinetic energy of the particle
        """
        return 0.5*self.mass*(self.velocity@self.velocity)
