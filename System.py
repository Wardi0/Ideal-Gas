from Particle import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import time as tm

class System:
    """
    Class responsible for initialising and progressing the simulation 

    Has the following attributes:
    self.dimensions -> Number of spatial dimensions of the system (int)
    self.box -> Contains the length of the container in each spatial dimension (np.array)
    self.global_time -> The time of the system since initialisation (float)
    self.no_collisions -> The total number of collisions that have occured at the current global_time (int)
    self.event_series - > Contains the time values of the next collision between the 2 objects in the 
                          corresponding tuple index (pd.Series)
    self.no_particles -> The number of particles to initialise the System with (int)
    self.particles -> List containing all Particle-objects in the system (list of Particle objects)
    self.net_impulse -> The total impulse delivered to the container walls over the whole simulation (float)
    """

    def __init__(self, no_particles, mass, radius, dimensions, starting_speed):
        """
        Initialisation arguments:
        
        no_particles - Int type value for the number of particles to initialise the System with
        mass - Float type value for the mass of the initial particles
        radius - Float type value for the radius of the initial particles
        dimensions - List of floats containing the lengths of the box in each spatial dimension
        starting_speed - Float type value for the speed of the initial particles
        """
        self.dimensions = len(dimensions)
        self.box = np.array(dimensions, dtype='float')
        self.no_particles = no_particles
        self.global_time = 0
        self.no_collisions = 0
        self.net_impulse = 0

        # Randomly select the initial position of each particle, making sure it is 
        # within the system and not overlapping with any other particles
        self.particles = []
        for i in range(no_particles):    
            searching = True
            while searching:
                available_space = self.box - 2*radius
                initial_position = Position(np.random.rand(self.dimensions)*available_space + radius)
                # Give each particle a velocity of magnitude starting_speed and random direction
                initial_velocity = (Velocity([0]*self.dimensions).random_unit_vector()) * starting_speed
                new_particle = Particle(initial_position, initial_velocity, mass, radius)
                # Check for overlap with all current particles
                overlap = False
                for particle in self.particles:
                    if new_particle.overlap(particle):
                        overlap = True
                        break
                if not overlap:
                    searching = False
                    self.particles.append(new_particle)
        
        self.initialise_event_series()
  
    def initialise_event_series(self):
        """
        Calculate and organise all collisions in the system into a Pandas Series
        """
        # In case particles have been added manually after initialisation
        self.no_particles = len(self.particles)

        event_timings = []
        event_index = []
        for particle_i in range(self.no_particles):
            for D in range(1, self.dimensions+1):
                event_timings.append(self.time_of_collision(particle_i, str(D)+'.Min'))
                event_index.append((particle_i,str(D)+'.Min'))
                event_timings.append(self.time_of_collision(particle_i, str(D)+'.Max'))
                event_index.append((particle_i,str(D)+'.Max'))
            for particle_j in range(particle_i+1, self.no_particles):
                event_timings.append(self.time_of_collision(particle_i, particle_j))
                event_index.append((particle_i,particle_j))
        
        # Sort the entries by the time values
        self.event_series = pd.Series(event_timings, event_index, dtype=np.float64)
        self.event_series = self.event_series.sort_values()  

    def within_box(self, particle):
        """
        Returns True if the given particle is within the box, otherwise returns False

        particle - Particle type object to check is within the box
        """
        available_space = self.box - 2*particle.radius
        for dimension in range(self.dimensions):
            if not 0 <= particle.position[dimension] - particle.radius <= available_space[dimension]:
                return False
        return True

    def time_of_collision(self, object_1, object_2):
        """
        Returns the time after which these objects will collide next, returning np.infty if they will not collide
        on their current trajectories

        object_1 - int type value representing the index of the colliding particle in self.particles
        object_2 - int or str type value representing the index of the colliding particle in self.particles or the
                   dimension of the constraining wall
        """
        particle_1 = self.particles[object_1]
        
        # Check if object_2 is one of the container walls
        if type(object_2) == str:
            dimension, side = object_2.split('.')
            dimension = int(dimension) - 1
            if side == 'Min':
                coordinate = particle_1.radius
            else:
                coordinate = self.box[dimension] - particle_1.radius
            # In case the particle is already touching the wall and has 0 velocity
            if coordinate == particle_1.position[dimension]:
                return 0
            # To avoid division by zero errors
            elif particle_1.velocity[dimension] == 0:
                return np.infty
            
            else:
                time = (coordinate - particle_1.position[dimension])/particle_1.velocity[dimension]
            if time > 0:
                return time
            else:
                return np.infty

        else:
            particle_2 = self.particles[object_2]

            # Check if both particles have 0 velocity
            if particle_1.velocity.magnitude() == 0 and particle_2.velocity.magnitude() == 0:
                return np.infty

            velocity_difference = particle_2.velocity - particle_1.velocity
            position_difference = particle_2.position - particle_1.position

            # Define the quadratic coefficients to find the collision time
            a = 0
            b = 0
            c = - (particle_1.radius + particle_2.radius)**2
            for D in range(self.dimensions):
                a += velocity_difference[D]**2
                b += 2*velocity_difference[D]*position_difference[D]
                c += position_difference[D]**2
            roots = np.roots([a,b,c])

            # Find the smallest positive and real root if applicable 
            if type(roots[0]) == np.float64:
                if (roots[0] < 0) != (roots[1] < 0):
                    return max(roots)
                elif (roots[0] > 0) and (roots[1] > 0):
                    return min(roots)
            return np.infty

    def update_event_series(self, object_1, object_2):
        """
        Calculate the event timings for any particles involved in a collision and simultaneously update event_series

        object_1 - int type value representing the index of the colliding particle in self.particles
        object_2 - int or str type value representing the index of the colliding particle in self.particles or the
                   dimension of the constraining wall
        """
        # Check if either object is a wall
        to_update = [object_i for object_i in [object_1, object_2] if type(object_i) != str]

        # Update all event_series entries corresponding to the particle(s)
        for particle_index in to_update:
            for D in range(1, self.dimensions+1):
                self.event_series[(particle_index,str(D)+'.Min')] = self.time_of_collision(particle_index,str(D)+'.Min')
                self.event_series[(particle_index,str(D)+'.Max')] = self.time_of_collision(particle_index,str(D)+'.Max')
            for index_1 in range(0,particle_index):
                self.event_series[(index_1,particle_index)] = self.time_of_collision(index_1,particle_index)
            for index_2 in range(particle_index+1, self.no_particles):
                self.event_series[(particle_index,index_2)] = self.time_of_collision(particle_index,index_2)
        
        # Ensures the next event can't be between the same objects due to machine precision causing overlaps
        self.event_series[(object_1, object_2)] = np.infty
        
        # Sort the new event_series
        self.event_series = self.event_series.sort_values()

    def collide(self, object_1, object_2):
        """
        Calculate and update the velocities of particles involved in the collision

        object_1 - int type value representing the index of the colliding particle in self.particles
        object_2 - int or str type value representing the index of the colliding particle in self.particles or the
                   dimension of the constraining wall
        """
        particle_1 = self.particles[object_1]
        self.no_collisions += 1

        # Check if object_2 is one of the container walls
        if type(object_2) == str:
            # Identify which coordinate the wall is restricting
            dimension, side = object_2.split('.')
            dimension = int(dimension) - 1
            # Add the impulse acting on the wall to the System total
            self.net_impulse += 2*particle_1.mass*abs(particle_1.velocity[dimension])
            # Invert the velocity component perpendicular to the wall
            particle_1.velocity.invert_component(dimension)
        else:
            particle_2 = self.particles[object_2]
            mass_1 = particle_1.mass
            mass_2 = particle_2.mass
            unit_position_vector = (particle_2.position - particle_1.position).unit_vector()
            delta_velocity = (particle_2.velocity - particle_1.velocity)
            impulse = Vector(unit_position_vector) * (-((2*mass_1*mass_2)/(mass_1+mass_2))*(delta_velocity@unit_position_vector))
            particle_1.velocity.add_velocity(-Velocity(impulse)/mass_1)     
            particle_2.velocity.add_velocity(Velocity(impulse)/mass_2)   

    def system_KE(self):
        """
        Return the total kinetic energy of the system
        """
        KE = 0
        for particle in self.particles:
            KE += np.float64(particle.kinetic_energy())
        return KE

    def simulate_event(self):
        """
        Simulate a single event for the whole system, updating the positions of all particles up to the next event, updating the 
        particles involved in the collision and recalculating relevant collision times in the event_series
        """
        # First index of the sorted series is the next collision
        (object_1, object_2) = self.event_series.first_valid_index()
        time =  self.event_series[0]
        
        # Update all particles over the time step
        for particle in self.particles:
            particle.update(time)
        
        self.global_time += time
        self.collide(object_1, object_2)
        
        # Progress the time of collisions not changed by the collision before updating the event_series
        self.event_series -= time
        self.update_event_series(object_1, object_2)

    def check_N(self):
        """
        Return True if the number of particles in the box equals no_particles
        """
        in_box = 0
        for particle in self.particles:
            if self.within_box(particle):
                in_box += 1
        # Machine precision may leave the last colliding particle temporarily outside the box 
        # before it can propagate inside again
        if in_box == self.no_particles or in_box == self.no_particles - 1:
            return True
        return False

