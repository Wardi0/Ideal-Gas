import pytest
from Tracker import *

@pytest.mark.parametrize("test_input,expected", 
[(([10,10,10],10), 2.41e24),
(([100,100],50), 9.05e25),
(([10,10,10,10],0), 0)])

def test_temperature(test_input, expected):
    tester = Tracker(System(10, 1, 1, test_input[0], test_input[1]))
    temp = tester.temperature()
    assert (temp-expected) <= 0.01 * temp

@pytest.mark.parametrize("test_input,expected", 
[(([10,20,10],100), 1e-3),
(([100,50],504), 1.68e-2),
(([10,10,10,10],0), 0)])

def test_pressure(test_input, expected):
    tester = Tracker(System(10, 1, 1, test_input[0], 1))
    tester.system.global_time = 100
    tester.system.net_impulse = test_input[1]
    pressure = tester.pressure()
    assert (pressure-expected) <= 0.01 * pressure

@pytest.mark.parametrize("test_input,expected", 
[([10,10,10], 1000),
([100,100], 10000),
([10,10,10,0], 0)])

def test_volume(test_input, expected):
    tester = Tracker(System(10, 1, 1, test_input, 1))
    volume = tester.volume()
    assert (volume-expected) <= 0.01 * volume