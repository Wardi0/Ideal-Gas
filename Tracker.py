from System import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import time as tm
import scipy.constants as sp

class Tracker:
    """
    Class to handle analysis of the simulation data

    Has the following attributes:
    self.system -> System to simulate and analyse (System)
    """

    def __init__(self, system = System(0,1,1,[1,1,1],1)):
        """
        Initialisation arguments:
        
        system - System type object to simulate
        """
        self.system = system

    def temperature(self):
        """
        Returns the temperature of the system
        """

        # Calculate the total energy of the system
        KE_total = 0
        for particle in self.system.particles:
            KE_total += particle.kinetic_energy()
        return 2*KE_total/(sp.Boltzmann*self.system.no_particles*len(self.system.box))

    def pressure(self):
        """
        Return the pressure of the system
        """
        if self.system.global_time == 0:
            return 0
        container_area = 0
        for dimension_main in range(len(self.system.box)):
            other_dimensions = list(range(len(self.system.box)))
            other_dimensions.remove(dimension_main)
            # Opposite sides have equal area
            area = 2
            for dimension in other_dimensions:
                area *= self.system.box[dimension]
            container_area += area
        return self.system.net_impulse / (self.system.global_time*container_area)

    def volume(self):
        """
        Return the volume of the system
        """
        volume = 1
        for length in self.system.box:
            volume *= length
        return volume

    def simulate(self, total_collisions, simulation_name):
        """
        Run the simulation for the given number of collsions, save the final state of the system as a
        .pkl file and separately save simulated quantities in a .csv file

        total_collisions - int type value of the number of collisions to simulate
        simulation_name - str type value for the file names
        """
        # Run the simulation
        print(tm.process_time())
        while self.system.no_collisions < total_collisions:
            self.system.simulate_event()
        print(tm.process_time())

        # Check N is conserved
        if not self.system.check_N():
            raise SimulationError("Unexpected number of particles in the box")

        # Store all particle properties in a nested dictionary
        final_state_dict = {}
        for index, particle in enumerate(self.system.particles):
            final_state_dict[index] = {'Position': particle.position.components, \
                                  'Velocity': particle.velocity.components, \
                                  'Mass': particle.mass, \
                                  'Radius': particle.radius}
                  
        final_state = pd.DataFrame(final_state_dict)
        final_state.transpose().to_pickle(simulation_name + ' State.pkl')

        quantities = pd.Series({'Pressure': self.pressure(), 'Volume': self.volume(), \
                                'Temperature': self.temperature(), 'Number of particles': self.system.no_particles, \
                                'Number of collisions': self.system.no_collisions, \
                                'Time': self.system.global_time})
        quantities.to_csv(simulation_name + ' Quantities.csv')

    def simulate_conservation(self, total_collisions, simulation_name):
        """
        Run the simulation for the given number of collsions, exporting the values of the supposedly conserved quantity 
        energy after each event to a .pkl file and a .csv file

        total_collisions - int type value of the number of collisions to simulate
        simulation_name - str type value for the file names
        """
        quantities_dict = {}

        # Run the simulation
        print(tm.process_time())
        while self.system.no_collisions < total_collisions:
            quantities_dict[self.system.no_collisions] = {'Energy': self.system.system_KE()}
            self.system.simulate_event()
        quantities_dict[self.system.no_collisions] = {'Energy': self.system.system_KE()}
        print(tm.process_time())

        # Check N is conserved
        if not self.system.check_N():
            raise SimulationError("Unexpected number of particles in the box")

        # Check N is conserved
        if not self.system.check_N():
            raise SimulationError("Unexpected number of particles in the box")
                  
        quantities = pd.DataFrame(quantities_dict)
        quantities.transpose().to_pickle(simulation_name + ' Conservation.pkl')
        quantities.transpose().to_csv(simulation_name + ' Conservation.csv')
    
    def simulate_track_particles(self, total_collisions, tracked_particles):
        """
        Track the motion of the given particles and plot their trajectories throughout the simulation

        total_collisions - int type value of the number of collisions to simulate
        tracked_particles - list of int type values of the indices of particles to track in System.particles
        """

        # Empty DataFrame of the particle positions
        positions = pd.DataFrame(columns=range(2*len(tracked_particles)))
        while self.system.no_collisions < total_collisions:
            position_frame = []
            for index, particle_index in enumerate(tracked_particles):    
                position_frame.append(self.system.particles[particle_index].position.components[0])
                position_frame.append(self.system.particles[particle_index].position.components[1])
            positions = positions.append(pd.DataFrame([position_frame]), ignore_index=True)
            self.system.simulate_event()

        # Check N is conserved
        if not self.system.check_N():
            raise SimulationError("Unexpected number of particles in the box")
        
        # Add the positions of the final frame
        position_frame = []
        for index, particle_index in enumerate(tracked_particles):    
            position_frame.append(self.system.particles[particle_index].position.components[0])
            position_frame.append(self.system.particles[particle_index].position.components[1])
        positions = positions.append(pd.DataFrame([position_frame]), ignore_index=True)

        # Plot the particle trajectories
        fig, ax = plt.subplots()
        for index, particle_index in enumerate(tracked_particles):
            x = positions[2*index].to_list()
            y = positions[2*index + 1].to_list()
            plt.plot(x,y, zorder=1)

        # Plot the final locations of the particles
        x = []
        y = []
        radius = []
        for particle in self.system.particles:
            x.append(particle.position[0])
            y.append(particle.position[1])
            radius.append(particle.radius)
        particles = [plt.Circle(np.array([x_i,y_i]), radius=r_i) for x_i, y_i, r_i in zip(x,y,radius)]
        ensemble = mpl.collections.PatchCollection(particles, color='k', zorder=20)
        ax.set_xlim(0, self.system.box[0])
        ax.set_ylim(0, self.system.box[1])
        fig.set_size_inches(6,6)
        ax.add_collection(ensemble)
        plt.show()
 
    def speed_distribution(self, number_bins, max_speed):
        """
        Return a histogram of the speeds of particles in the system and compare to the expected 
        Maxwell-Boltzmann distribution, assuming all particles have the same mass

        number_bins - int type value of the number of bins to plot
        max_speed - float type value for the max speed to include if the actual values don't exceed it
        """
        mass = self.system.particles[0].mass
        plt.rcParams.update({'font.size': 25})
        
        # Create a list of all particle speeds
        velocities = []
        for particle in self.system.particles:
            velocity = particle.velocity.magnitude()    
            velocities.append(velocity)

        # Calculate the histogram bins
        if max_speed > math.ceil(max(velocities)):
            bins = [v for v in range(0, max_speed, math.ceil(max_speed/number_bins))] 
        else:
            bins = [v for v in range(0, math.ceil(max(velocities)), math.ceil(max(velocities)/number_bins))]

        fig,ax = plt.subplots(1,1)
        ax.set_xlabel('Speed ($ms^{-1}$)')
        ax.set_ylabel('Frequency')
        ax.set_title('Number of collisions = ' + str(int(self.system.no_collisions)))
        ax.hist(velocities, bins, label='Simulation Data')
        bin_width = bins[1]-bins[0]
        kT = sp.Boltzmann * self.temperature()
        v = np.linspace(0,bins[-1]*1.2,1000)
        f = bin_width*self.system.no_particles * np.sqrt((2 * mass**3) / (np.pi * kT**3)) \
            * v**2 * np.exp((-mass * v**2)/(2*kT))
        plt.plot(v,f,label='MB Expectation Values')
        plt.legend()
        plt.show()

    def import_state(self, file_name):
        """
        Read a .pkl file and import its state into the Tracker - only imports the particle states 
        It is not recommended to continue a simulation from this imported state - the last collision may be 
        repeated leading to loss of particles from the box

        file_name - str value of the file name in the directory of this file containing the state data
        """
        # Initialise the empty System.particles
        self.system.particles = []

        # Read .pkl file as DataFrames
        directory = 'C:\\Users\\wardi\\Documents\\Uni\\OneDrive - Lancaster University\\Year 4\\Computer Modelling\\Kinetic Gas\\phys389-2021-project-Wardi0-1\\' +  file_name
        state = pd.read_pickle(directory)
        
        positions = state['Position']
        velocities = state['Velocity']
        masses = state['Mass']
        radii = state['Radius']
        for i in range(len(positions)):
            self.system.particles.append(Particle(positions[i],velocities[i],masses[i],radii[i]))

        # Initialise the new event_series
        self.system.initialise_event_series()
