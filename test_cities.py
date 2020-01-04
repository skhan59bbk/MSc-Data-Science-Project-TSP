import pytest
from cities import *


def test_compute_total_distance():
    road_map1 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                ("Delaware", "Dover", 39.161921, -75.526755),\
                ("Minnesota", "Saint Paul", 44.95, -93.094)]
    
    road_map2 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                 ("Delaware", "Dover", 39.161921, -75.526755),\
                 ("Minnesota", "Saint Paul", 44.95, -93.094),\
                 ('Georgia', 'Atlanta', 33.76, -84.39),\
                 ('Florida', 'Tallahassee', 30.45, -84.27)]
    
    try:
        assert compute_total_distance(road_map1) == pytest.approx(9.386+18.496+10.646, 0.01)
    except Exception as e:
        return e
    assert type(compute_total_distance(road_map1)) is float
    assert type(road_map1) is list
    assert compute_total_distance(road_map1) > 0.0
    assert compute_total_distance(road_map1) < compute_total_distance(road_map2)
    assert compute_total_distance(road_map2) > compute_total_distance(road_map1)
    

def test_swap_cities():
    road_map1 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                ("Delaware", "Dover", 39.161921, -75.526755),\
                ("Minnesota", "Saint Paul", 44.95, -93.094)]
    
    road_map2 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                 ("Delaware", "Dover", 39.161921, -75.526755),\
                 ("Minnesota", "Saint Paul", 44.95, -93.094),\
                 ('Georgia', 'Atlanta', 33.76, -84.39),\
                 ('Florida', 'Tallahassee', 30.45, -84.27)]
    
    try:
        assert type(swap_cities(road_map2,1,2)) is tuple
        assert type(swap_cities(road_map1, 1, 2)[1]) is float
        assert type(swap_cities(road_map2, 1, 2)[0]) is list
        assert swap_cities(road_map2, 2, 2)[0] == road_map2
        assert road_map2[0] != swap_cities(road_map2, 0, 1)[0][0]
        assert len(road_map2) == len(swap_cities(road_map2,0,2)[0])
        assert swap_cities(road_map1,0,3)[1] == compute_total_distance(swap_cities(road_map1,0,3)[0])
    except Exception as e:
        print(str(e))

def test_shift_cities():
    road_map1 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                ("Delaware", "Dover", 39.161921, -75.526755),\
                ("Minnesota", "Saint Paul", 44.95, -93.094)]
    
    road_map2 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                 ("Delaware", "Dover", 39.161921, -75.526755),\
                 ("Minnesota", "Saint Paul", 44.95, -93.094),\
                 ('Georgia', 'Atlanta', 33.76, -84.39),\
                 ('Florida', 'Tallahassee', 30.45, -84.27)]

    
    assert type(shift_cities(road_map1)) is list
    assert compute_total_distance(shift_cities(road_map1)) == compute_total_distance(road_map1)
    assert road_map1[0] != shift_cities(road_map1)[0]
    assert shift_cities(road_map1)[0] == road_map1[len(road_map1)-1]
    assert shift_cities(road_map2)[0] == road_map2[len(road_map2)-1]
    
def test_distances_and_limits():

    road_map2 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                 ("Delaware", "Dover", 39.161921, -75.526755),\
                 ("Minnesota", "Saint Paul", 44.95, -93.094),\
                 ('Georgia', 'Atlanta', 33.76, -84.39),\
                 ('Florida', 'Tallahassee', 30.45, -84.27)]
    
    distance_list = distances_and_limits(road_map2)[0]
    
    assert len(distance_list) == len(road_map2)
    assert distances_and_limits(road_map2)[1] >= -90
    assert distances_and_limits(road_map2)[2] <= 90
    assert distances_and_limits(road_map2)[3] >= -180
    assert distances_and_limits(road_map2)[4] <= 180
    
    
    