import numpy as np
from errors import DimensionError
import matplotlib.pyplot as plt
class Vector:
    """
    Class with basic vector functionality that the Position and Velocity classes can inherit from

    Has the following attributes:
    self.components -> Contains the vector's components (np.array)
    """

    def __init__(self, values):
        """
        Initialisation arguments:
        
        values - array-like or Vector-like object containing the vector's components
        """
        # In case a vector is initialised from a Position, Velocity or Vector object
        if type(values) not in [list, np.ndarray]:
            self.components = np.array(values.components, dtype=float)
        else:
            self.components = np.array(values, dtype=float)

    def __repr__(self):
        return str(type(self)) + ': ' + str(self.components)

    @classmethod
    def new(cls, values):
        """
        Create a new instance of the object's class

        values - array-like or Vector-like object containing the object's components
        """
        return cls(values)

    def __getitem__(self, index):
        """
        Overload the index operation to work with the vector's components

        index - int type value of the index to access
        """
        return self.components[index]

    def __add__(self, other):
        """
        Overload the addition operator to add individual components if dimensionally compatible

        other - Vector-like object to add 
        """
        if self.dimension() == other.dimension():
            return self.new(self.components + other.components)
        else:
            raise DimensionError("Objects have incompatible dimensions")

    def __neg__(self):
        """
        Overload the negation operator to invert each component of the vector
        """
        return self.new(-self.components)

    def __sub__(self, other):
        """
        Overload the subtraction operator to subtract components of the second vector from the corresponding 
        components if dimensionally compatible

        other - Vector-like object to subtract
        """
        return self + (-other)

    def __mul__(self, val):
        """
        Overload the multiplication operator to scale the vector's components by the scalar value

        val - int or float type value to multiply each component by
        """
        if type(val) in [float, int, np.float64]:
            return self.new(self.components * val)
        else:
            raise TypeError("Can only multiply by a float or integer")

    def __matmul__(self, other):
        """
        Overload the matrix multiplication operator to perform the scalar product of the 2 vectors if dimensionally compatible

        other - Vector-like object to calculate the scalar product with
        """
        if self.dimension() == other.dimension():
            return sum(self.components * other.components)
        else:
            raise DimensionError("Objects have incompatible dimensions")

    def __truediv__(self, val):
        """
        Overload the division operator to divide each component by the given value

        val - int or float type value to divide each component by
        """
        if type(val) in [float, int, np.float64]:
            return self.new(self.components / val)
        else:
            raise TypeError("Can only divide by a float or integer")

    def __eq__(self, other):
        """
        Overload the equality operator such that 2 Vectors are equal if every component is equal

        other - Vector-like object to compare components with
        """
        if self.dimension() == other.dimension():
            if all([self.components[i] == other.components[i] for i in range(self.dimension())]):
                return True
        return False

    def dimension(self):
        """
        Return the dimension of the vector
        """
        return len(self.components)

    def magnitude(self):
        """
        Return the magnitude of the vector
        """
        return np.sqrt(abs(self@self))

    def unit_vector(self):
        """
        Return a unit vector with the same direction
        """
        return self/(self.magnitude())

    def random_unit_vector(self):
        """
        Return a unit vector with a random direction, where the distribution is uniform across all possible directions, of
        the same dimension 
        """
        components = []
        for D in range(len(self.components)):
            components.append(np.random.normal(0,1))
        return self.new(components).unit_vector()
    
    def polar_angle(self):
        """
        Returns the polar angle of a given 2D Vector in the range 0-360 degrees
        """
        if len(self.components) != 2:
            raise DimensionError('Vector must be 2-dimensional')
        x, y = self.components
        if y >= 0:
            return (np.arctan2(y,x)*180/np.pi)
        else:
            return (np.arctan2(y,x)*180/np.pi) + 360

    def random_distribution(self, no_samples):
        """
        Plot a histogram of angles (polar coordinates in degrees) produced by random_unit_vector in 2D 
        Expect the distribution to be uniform for large no_samples

        no_samples - int type value for the number of random vectors generated
        """
        base = Vector([0,0])
        angles = []
        for sample in range(no_samples):
            unit_vector = base.random_unit_vector()
            angle = unit_vector.polar_angle()
            angles.append(angle)
        fig,ax = plt.subplots(1,1)
        bins = [10*n for n in range(37)] 
        ax.set_xticks([0,90,180,270,360])
        ax.set_xlabel('Angle (Degrees)')
        ax.set_ylabel('Frequency')
        ax.set_title('Histogram of angles produced by random_unit_vector in 2D (N='+str(no_samples)+')')
        ax.hist(angles, bins)
        plt.show()