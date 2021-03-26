from Vector import Vector, DimensionError

class Velocity(Vector):
    """
    Class representing a velocity vector of a particle

    Has the following attributes:
    self.components -> Contains the velocity component in each spatial direction (np.array)
    """

    def __init__(self, components):
        """
        Initialisation arguments:
        
        values - array-like or Vector-like object containing the velocity components
        """
        super().__init__(components)

    def add_velocity(self, delta_velocity):
        """
        Adds the given vector to the velocity

        delta_velocity - Vector-like object to add the components of to self
        """
        if self.dimension() == delta_velocity.dimension():
            self.__init__(self.components + delta_velocity.components)
        else:
            raise DimensionError("Objects have incompatible dimensions")

    def invert_component(self, dimension):
        """
        Invert the component at the index given by the dimension

        dimension - Int type value of the index to invert
        """
        self.components[dimension] = -self.components[dimension]
