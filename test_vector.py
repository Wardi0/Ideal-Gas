import pytest
import numpy as np
from Vector import *

@pytest.mark.parametrize("test_input,expected", 
[((Vector([1,2]),Vector([-3,2])), 1),
((Vector([5,2]),Vector([0,-1])), -2)])

def test_matmul(test_input, expected):
    assert test_input[0]@test_input[1] == expected

@pytest.mark.parametrize("test_input,expected", 
[((Vector([1,2]),3), Vector([3,6])),
((Vector([5,2]),0), Vector([0,0]))])

def test_mul(test_input, expected):
    assert test_input[0]*test_input[1] == expected

@pytest.mark.parametrize("test_input,expected", 
[(Vector([1,2.0]), Vector([1.0,2])),
(Vector([0,-1]), Vector([0,-1]))])

def test_eq(test_input,expected):
    assert test_input == expected

@pytest.mark.parametrize("test_input,expected", 
[(Vector([1,2.0]), Vector([-1.0,-2])),
(Vector([0,-1]), Vector([-0,1]))])

def test_neg(test_input,expected):
    assert -test_input == expected

@pytest.mark.parametrize("test_input,expected", 
[((Vector([1,2]),Vector([-3,2])), Vector([-2,4])),
((Vector([5,2]),Vector([0,-1])), Vector([5,1]))])

def test_add(test_input,expected):
    assert test_input[0] + test_input[1] == expected

@pytest.mark.parametrize("test_input,expected", 
[((Vector([1,2]),Vector([-3,2])), Vector([4.0,0])),
((Vector([5,2]),Vector([0,-1])), Vector([5,3]))])

def test_sub(test_input,expected):
    assert test_input[0] - test_input[1] == expected

@pytest.mark.parametrize("test_input,expected", 
[((Vector([1,2]),0.5), Vector([2,4])),
((Vector([5,2]),3), Vector([5/3,2/3]))])

def test_truediv(test_input,expected):
    assert test_input[0]/test_input[1] == expected

@pytest.mark.parametrize("test_input,expected", 
[(Vector([1,2.0]), 2),
(Vector([0,-1,1,2,4]), 5)])

def test_dimension(test_input,expected):
    assert test_input.dimension() == expected    

@pytest.mark.parametrize("test_input,expected", 
[(Vector([1,2.0]), np.sqrt(5)),
(Vector([0,-1,1,2,4]), np.sqrt(22))])

def test_magnitude(test_input,expected):
    assert test_input.magnitude() == expected    

@pytest.mark.parametrize("test_input,expected", 
[(Vector([1,2.0]), Vector([1,2.0])/np.sqrt(5)),
(Vector([0,-1,1,2,4]), Vector([0,-1,1,2,4])/np.sqrt(22))])

def test_unit_vector(test_input,expected):
    assert test_input.unit_vector() == expected and round(test_input.unit_vector().magnitude(), 7) == 1

@pytest.mark.parametrize("test_input,expected", 
[(Vector([1,2.0]), 63),
(Vector([0,-1]), 270)])

def test_polar_angle(test_input,expected):
    assert round(test_input.polar_angle()) == expected 

@pytest.mark.parametrize("test_input,expected", 
[((Vector([1,2.0]),Vector([2,1,2,4])), DimensionError),
((Vector([1,2.0]), Vector([2,1,3])), DimensionError)])

def test_DimensionError(test_input,expected):
    with pytest.raises(expected):
        y = test_input[0] + test_input[1]