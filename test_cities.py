import pytest
from cities import *


def test_compute_total_distance():
    road_map1 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                ("Delaware", "Dover", 39.161921, -75.526755),\
                ("Minnesota", "Saint Paul", 44.95, -93.094)]
    
    try:
        assert compute_total_distance(road_map1) == pytest.approx(9.386+18.496+10.646, 0.01)
    except Exception as e:
        return e
    assert type(compute_total_distance(road_map)) is float
    assert type(road_map) is list
    assert type(distances) is list
    assert compute_total_distance() > 0.0
    

def test_swap_cities():
    road_map1 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                ("Delaware", "Dover", 39.161921, -75.526755),\
                ("Minnesota", "Saint Paul", 44.95, -93.094)]
    
    assert type(swap_cities(road_map1,5,12)) is tuple


def test_shift_cities():
    road_map1 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                ("Delaware", "Dover", 39.161921, -75.526755),\
                ("Minnesota", "Saint Paul", 44.95, -93.094)]
    
    assert type(shift_cities(road_map1)) is list

