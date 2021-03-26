from Tracker import *
from plotter import *

# Define all the System parameters
N = 200     # Number of particles
L = (5e-7)  # Length of one side of the cube
temp = 300  #Temperature of the gas
radius = 2.5e-11    # Radius of the particles
mass = 3.3e-27      # Mass of the particles

# Choose the simulation parameters
no_collisions = 5000    # Number of collisions to simulate
file_name = 'Simulation 1'      # Root file name to save data

speed = np.sqrt(3*sp.Boltzmann*temp/mass)
gas = System(N, mass, radius, [L,L,L], speed)
simulation = Tracker(gas)
simulation.simulate(no_collisions, file_name)




