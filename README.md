# turbo-eureka

simulation.py

File to run the actual simulation
To use:
    1. Change the system parameters to the desired values
    2. Adjust the simulation parameters to the desired values
    3. The simulated quantities will be contained in a .csv file
    4. Multiple of these files can be plotted together if contained in a single folder using plor_relation (only vary 1 variable across simulations)
This is set up to simulate a 3D cube
All units are taken to be SI standard - no prefixes
The initialisation of the System can be changed to arbitrary dimensions - if the simulation does not run, the volume may not be large enough for the desired number of particles

errors.py

Contains the DimensionalError and SimulationError definitions
Used to handle incompatible vector operations and particles escaping the box

Vector.py

Contains the Vector-class definition
Overloads various operators to perform vector operations relevant to the simulation like multiplying
by a scalar and the scalar product
Contains methods to generate unit vectors with randomly distributed direction in arbitrary dimensions based on the Gaussian 
distribution
Has a method to test the randomly distributed unit vector in 2D

Position.py

Contains the Position-class definition that inherits from the Vector-class
Contains a method to update the position over a given time step for a given velocity

Velocity.py 

Contains the Velocity-class definition that inherits from the Vector-class
Contains a method to update the objects componenents by adding another velocity

Particle.py

Contains the Particle-class definition
Contains methods to update its position over an arbitrary time step, check for overlap with other particles and to 
calculate its kinetic energy

System.py

Contains the System-class definition
Contains the structure and methods to run the actual simulation
Contains methods to calculate collision times, initialise the system, update the collision times, handle a collision, calculate the total kinetic energy, check the location of particles and simulate a single event
Has attributes to track important quantities in the simulation like the time and number of collisions

Tracker.py

Contains the Tracker-class definition
Handles the running of the actual simulation as well as the storing of resulting data in files
Contains methods to simulate the pressure of the system, analyse the speed distribution of the system, generate energy conservation data, track particle motion and import a System state from a .pkl file

plotter.py

Contains a function to plot the simulated pressure against one of the following variables: temperature, volume, 1/volume, number of particles or the number of collisions
Accepts files produced by the Tracker simulate method

test_particle.py

Contains test functions for the Particle, Velocity and Position classes for use with pytest

test_vector.py

Contains test functions for the Vector class for use with pytest

test_system.py

Contains test functions for the System class for use with pytest

test_tracker.py

Contains test functions for the Tracker class for use with pytest