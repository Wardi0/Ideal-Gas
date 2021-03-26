import pytest
import numpy as np
from Particle import Particle, Velocity, Position, Vector, DimensionError

@pytest.mark.parametrize("test_input,expected", 
[(Position([9,8,8]), Position([9,8,8])), 
(Vector([1,3,2,6]), Vector([1,3,2,6])),
(Velocity([0,-4]), Velocity([0,-4]))])

def test_new(test_input, expected):
    assert test_input.new(test_input.components) == expected 

@pytest.mark.parametrize("test_input,expected", 
[((Position([1,4,2]),Velocity([4,2,3]),2), Position([9,8,8])), 
((Position([-12,0,5]),Velocity([-2,7,1]),6), Position([-24,42,11]))])

def test_propagate(test_input, expected):
    test_input[0].propagate(test_input[1],test_input[2])
    assert test_input[0] == expected 

@pytest.mark.parametrize("test_input,expected", 
[((Velocity([1,4,2]),Velocity([4,2,3])), Velocity([5,6,5])), 
((Velocity([-12,0,5]),Velocity([-2,7,1])), Velocity([-14,7,6]))])

def test_add_velocity(test_input, expected):
    test_input[0].add_velocity(test_input[1])
    assert test_input[0] == expected 

@pytest.mark.parametrize("test_input,expected", 
[((Velocity([1,4,2]),2), Velocity([1,4,-2])), 
((Velocity([-12,0,5]),1), Velocity([-12,0,5]))])

def test_invert_component(test_input, expected):
    test_input[0].invert_component(test_input[1])
    assert test_input[0] == expected 

@pytest.mark.parametrize("test_input,expected", 
[((Particle([2,4,1],[-4,2,0],1,3),4), Position([-14,12,1])), 
((Particle([-3,5,1],[7,-4,2],8,5),6), Position([39,-19,13]))])

def test_update(test_input, expected):
    test_input[0].update(test_input[1])
    assert test_input[0].position == expected 

@pytest.mark.parametrize("test_input,expected", 
[((Particle([2,4,1],[-4,2,0],1,3),Particle([2,5,2],[7,25,-4],1,2)), True),
 ((Particle([8,5,2],[-4,2,0],1,3),Particle([-3,0,-2],[-4,2,0],1,3)), False)])

def test_overlap(test_input, expected):
    assert test_input[0].overlap(test_input[1]) == expected

@pytest.mark.parametrize("test_input,expected", 
[(Particle([2,4,1],[-4,2,2],1,3), 12), 
(Particle([-3,5],[7,-6],8,5), 340)])

def test_kinetic_energy(test_input, expected):
    assert round(test_input.kinetic_energy(),5) == expected  

