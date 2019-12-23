import random, math, matplotlib.pyplot as plt#, pandas as pd

def read_cities(file_name):
    try:
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
        return cities_list
   
    except Exception as e:          ### Use custom type error messages ###
        print(e)
    
    
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
    distances = []

    for i, city in enumerate(road_map):
        from_x, to_x = road_map[(i-1) % len(road_map)][2], road_map[i][2]
        from_y, to_y = road_map[(i-1) % len(road_map)][3], road_map[i][3]
        distances.append(math.sqrt((from_x - to_x)**2 + (from_y - to_y)**2))

    #cities_df = pd.DataFrame(road_map, columns=('State','City','Longitude','Latitude'))
    #cities_df['Distance'] = distances
    
    #print(cities_df)
    return round(sum(distances),2)


def swap_cities(road_map, index1, index2):
    """
    Take the city at location `index` in the `road_map`, and the 
    city at location `index2`, swap their positions in the `road_map`, 
    compute the new total distance, and return the tuple 

        (new_road_map, new_total_distance)

    Allow for the possibility that `index1=index2`,
    and handle this case correctly.
    """
    #new_map = []
    #new_dist = 5.2
    
    new_road_map = road_map
    
    try:
        new_road_map[index1], new_road_map[index2] = \
        new_road_map[index2], new_road_map[index1]
        return (new_road_map, compute_total_distance(new_road_map))
    except Exception as e:
        return 'Error: '+str(e)
    

    #return (new_map, new_dist)


def shift_cities(road_map):
    """
    For every index i in the `road_map`, the city at the position i moves
    to the position i+1. The city at the last position moves to the position
    0. Return the new road map. 
    """
    new_road_map = []
    
    for i, city in enumerate(road_map):
        new_road_map.append(road_map[(i-1) % len(road_map)])

    return new_road_map


def find_best_cycle(road_map):
    """
    Using a combination of `swap_cities` and `shift_cities`, 
    try `10000` swaps/shifts, and each time keep the best cycle found so far. 
    After `10000` swaps/shifts, return the best cycle found so far.
    Use randomly generated indices for swapping.
    """
    
    ### shift 50 times, swap 10000 in each shift ####
    
    i = 0
    best_cycle = compute_total_distance(road_map)
    attempt_map = road_map
    
    while i <= 100:
        try:
            rand_idx1 = random.randint(0, len(road_map)-1)
            rand_idx2 = random.randint(0, len(road_map)-1)
            distance = compute_total_distance(swap_cities(attempt_map,rand_idx1, rand_idx2)[0])
            if distance < best_cycle:
                best_cycle = distance
            '''
            else:
                attempt_map = shift_cities(road_map)
            '''
        except Exception as e:
            print('Error: '+str(e))
        attempt_map = shift_cities(road_map)
        i += 1
    #random.seed(100)

    return best_cycle, road_map


def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and 
    their connections, along with the cost for each connection 
    and the total cost.
    """
    
    best_map = find_best_cycle(road_map)[1]
    cities_df = pd.DataFrame(best_map, columns=('State','City','Longitude','Latitude'))
    return cities_df


def main():
    """
    Reads in, and prints out, the city data, then creates the "best"
    cycle and prints it out.
    """
    roadmap = read_cities('C:\\Users\\samee\\Documents\\POP1\\pop-one-project-skhan59\\city-data.txt')
    print('--->> Here is the original route (Distance: {}) <<---'.format(compute_total_distance(roadmap)))
    print_cities(roadmap)
    #print(compute_total_distance(roadmap))
    #visualise(roadmap)
    #print(swap_cities(roadmap,41,17))
    #print(shift_cities(roadmap))
    #print(find_best_cycle(roadmap))
    print('')
    print('--->> Here is a shorter route (Distance: {}) <<---'.format(find_best_cycle(roadmap)[0]))
    print(print_map(roadmap))


def visualise(road_map):
    
    ax, fig = plt.subplots()
    plt.scatter(cities_df['Longitude'], cities_df['Latitude'], marker='x', label='Cities')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    
    plt.show()


if __name__ == "__main__": 
    main()