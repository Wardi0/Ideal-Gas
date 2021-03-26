from Vector import Vector, DimensionError

class Position(Vector):
    """
    Class representing a position vector of a particle

    Has the following attributes:
    self.components -> Contains the position coordinate in each spatial direction (np.array)
    """

    def __init__(self, values):
        """
        Initialisation arguments:
        
        values - array-like or Vector-like object containing the position components
        """
        super().__init__(values)

    def propagate(self, velocity, time_step):
        """
        Propagates the position through a given time step for the given velocity

        velocity - Vector-like object to propagate in the direction of
        time_step - float or int type value to propagate over
        """
        if self.dimension() == velocity.dimension():
            self.__init__(self.components + velocity.components*time_step)
        else:
            raise DimensionError("Objects have incompatible dimensions")
