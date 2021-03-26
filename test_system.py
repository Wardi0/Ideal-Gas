import pytest
import numpy as np
from System import *

@pytest.mark.parametrize("test_input,expected", 
[(([10,10,10],Particle([2,2,2],[2,5,1],1,1)), True),
(([5,5,4],Particle([2,2,2],[-1,0,3],1,2)), True),
(([10,10],Particle([1,1],[5,-2],1,1.5)), False),
(([10,10],Particle([9.3,4],[5,-2],7,1.5)), False)])

def test_within_box(test_input, expected):
    box = System(0, 1, 1, test_input[0], 1)
    assert box.within_box(test_input[1]) == expected

@pytest.mark.parametrize("test_input,expected", 
[((Particle([2,2,2],[1,1,1],1,2),Particle([8,8,8],[0,0,0],1,1)), 4.268),
((Particle([1,0,2],[-1,0,0],6,1),Particle([9,0,2],[2,0,0],1.2,0.4)), np.infty),
((Particle([2,2,0],[4,7,0],1,2),Particle([6,9,0],[0,0,0],1,2)), 0.504)])

def test_time_of_collision(test_input, expected):
    box = System(0, 1, 1, [100,100,100], 1)
    box.particles = [test_input[0], test_input[1]]
    assert round(box.time_of_collision(0,1),3) == expected

@pytest.mark.parametrize("test_input,expected", 
[([Particle([2,0,0],[np.sqrt(32),0,0],1,2),Particle([8,0,0],[0,0,0],1,1)], 0.530),
([Particle([5,0,0],[-4,0,0],1,2),Particle([8,0,0],[4,0,0],1,1)], 0)])


def test_initialise_event_series(test_input, expected):
    box = System(0, 1, 1, [100,100,100], 1)
    box.particles = test_input
    box.initialise_event_series()
    assert round(box.event_series[(0,1)],3) == expected

def test_simualate_event():
    box = System(0, 1, 1, [100,100,100], 1)
    box.particles = [Particle([2,2,5],[1,1,0],1,1), Particle([8,6,5],[0,0,0],1,1)]
    box.initialise_event_series()
    box.simulate_event()
    coordinates_0 = [round(r_i,10) for r_i in box.particles[0].position]
    coordinates_1 = [round(r_i,10) for r_i in box.particles[1].position]
    velocity_0 = [round(v_i,10) for v_i in box.particles[0].velocity]
    velocity_1 = [round(v_i,10) for v_i in box.particles[1].velocity]
    assert coordinates_0 == [6,6,5] and round(box.global_time,10) == 4 \
           and velocity_1 == [1,0,0] and coordinates_1 == [8,6,5] \
           and velocity_0 == [0,1,0]

@pytest.mark.parametrize("test_input,expected", 
[((Particle([2,2,2],[1,1,1],1,2),Particle([8,8,8],[-4,2,5],1,1)), 24),
((Particle([1,0],[-1,0],6,1),Particle([9,2],[2,0],1.2,0.4)), 5.4),
((Particle([2,2,0],[4,7,0],1,2),Particle([6,9,0],[0,0,0],1,2)), 32.5)])

def test_system_KE(test_input, expected):
    box = System(0, 1, 1, [100,100,100], 1)
    box.particles = [test_input[0], test_input[1]]
    assert float(round(box.system_KE(),3)) == expected

def test_update_event_series():
    box = System(0,1,1,[100,100],1)
    p_1 = Particle([2,2],[1,1],1,1)
    p_2 = Particle([8,6],[0,0],1,1)
    p_3 = Particle([16,6],[0.5,0],1,1)
    p_4 = Particle([10,10],[0,0],1,1)
    p_5 = Particle([6,20],[0,-1],1,1)
    box.particles = [p_1,p_2,p_3,p_4,p_5]
    box.initialise_event_series()
    box.simulate_event()
    assert round(box.event_series[(0,4)],10) == 4 and \
           round(box.event_series[(1,2)],10) == 16 and \
           round(box.event_series[(0,3)],10) == np.infty and \
           round(box.event_series[(0,'2.Max')],10) == 93 and \
           round(box.event_series[(1,'1.Max')],10) == 91 and \
           round(box.event_series[(0,1)],10) == np.infty
           




