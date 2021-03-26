class DimensionError(Exception):
    """
    Incompatible dimensions for the attempted operation
    """
    pass

class SimulationError(Exception):
    """
    Unexpected number of particles in the box
    """
    pass