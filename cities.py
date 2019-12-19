import random, math, matplotlib.pyplot as plt #, pandas as pd, 

def read_cities(file_name):

    f = open(file_name,'r')
    line = f.readline().rstrip()
    road_map = dict()
    
    while line:
        elements = line.split('\t')
        road_map[(elements[0],elements[1])] = \
        (round(float(elements[2]),2), round(float(elements[3]),2))
        line = f.readline().rstrip()
    f.close
    
    cities_list = [location + road_map[location] for location in road_map]
    #cities_df = pd.DataFrame(cities_list, columns=('State','City','Longitude','Latitude'))
    
    return cities_list


def print_cities(road_map):
    """
    Prints a list of cities, along with their locations. 
    Print only one or two digits after the decimal point.
    """
    print(road_map)
    

def compute_total_distance(road_map):
    """
    Returns, as a floating point number, the sum of the distances of all 
    the connections in the `road_map`. Remember that it's a cycle, so that 
    (for example) in the initial `road_map`, Wyoming connects to Alabama...
    """
    #return (9.386+18.496+10.646)
    # euclidean dist between x, y coordinates
    distances = []
    for i, city in enumerate(road_map):
        if i == 0 or i > 5:
            pass
        else:
            from_x = city[2]
            from_y = city[2]
            distances.append(from_x)
    
    return sum(distances)
    #euclid = math.sqrt((from_x - to_x)^2 + (from_y - to_y)^2)

def swap_cities(road_map, index1, index2):
    """
    Take the city at location `index` in the `road_map`, and the 
    city at location `index2`, swap their positions in the `road_map`, 
    compute the new total distance, and return the tuple 

        (new_road_map, new_total_distance)

    Allow for the possibility that `index1=index2`,
    and handle this case correctly.
    """
    new_map = []
    new_dist = 5.2
    return (new_map, new_dist)


def shift_cities(road_map):
    """
    For every index i in the `road_map`, the city at the position i moves
    to the position i+1. The city at the last position moves to the position
    0. Return the new road map. 
    """
    new_road_map = []
    return new_road_map


def find_best_cycle(road_map):
    """
    Using a combination of `swap_cities` and `shift_cities`, 
    try `10000` swaps/shifts, and each time keep the best cycle found so far. 
    After `10000` swaps/shifts, return the best cycle found so far.
    Use randomly generated indices for swapping.
    """
    pass


def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and 
    their connections, along with the cost for each connection 
    and the total cost.
    """
    pass


def main():
    """
    Reads in, and prints out, the city data, then creates the "best"
    cycle and prints it out.
    """
    pass


def visualise(road_map):
    call_map = print_cities(road_map)
    
    ax, fig = plt.subplots()
    plt.scatter(call_map.Longitude, call_map.Latitude, marker='x', label='Cities')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    
    plt.show()

if __name__ == "__main__": #keep this in
    main()


roadmap = read_cities('C:\\Users\\samee\\Documents\\POP1\\pop-one-project-skhan59\\city-data.txt')
#print_cities(roadmap)
print(compute_total_distance(roadmap))
#visualise(roadmap)