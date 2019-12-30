import random, math, pandas as pd
from tkinter import *


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
        #return (new_road_map, compute_total_distance(new_road_map))
    except Exception as e:
        print('Error: '+str(e))
    
    return (new_road_map, compute_total_distance(new_road_map))
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
    
    best_map = road_map
    #attempt_map = road_map
    best_cycle = compute_total_distance(best_map)
    print('starting best: ', best_cycle)
    print('computed best: ', compute_total_distance(best_map))
    #print('starting map', [(i, city) for (i, city) in enumerate(attempt_map)])
    #print('starting best cycle', best_cycle)
    i = 1
    
    while i <= 2:
        #try:  
            attempt_map = road_map  ### BOTH ARE CONNECTED. MAKE SHALLOW COPY INSTEAD!! ####
            print(i, 'best', best_cycle)
            print(i, '### attempt map ###')
            print([(num, city) for (num, city) in enumerate(attempt_map)])
            #print(i, 'best cycle so far', best_cycle)
            rand_idx1 = random.randint(0, len(attempt_map)-1)
            rand_idx2 = random.randint(0, len(attempt_map)-1)
            print(i, rand_idx1, rand_idx2)
            (new_map, distance) = swap_cities(attempt_map, rand_idx1, rand_idx2)
            print('new_map', new_map)
            print('new dist', distance)
            print('before checking against new dist, best cycle: ', best_cycle)
            if distance < best_cycle:
                best_cycle = distance
                best_map = new_map
                print('### best map ###', compute_total_distance(best_map), best_cycle)
                print([(num, city) for (num, city) in enumerate(best_map)])
                attempt_map = best_map
                print('### new attempt map ###', compute_total_distance(best_map))
                print([(num, city) for (num, city) in enumerate(attempt_map)])        
            else:
                print('#### No better. now map has shifted. ####')
                print('### best map unchanged ###', compute_total_distance(best_map), best_cycle)
                print('best map --> ', [(num, city) for (num, city) in enumerate(best_map)])  
                attempt_map = shift_cities(new_map) 
                print('attempt map -->',[(num, city) for (num, city) in enumerate(attempt_map)])
            #print('attempt map updated with new map?', attempt_map == new_map)
            i += 1
        #except Exception as e:
            #print('Error: '+str(e))
        #attempt_map = shift_cities(road_map)
        #i += 1
    
    print('best dist:', compute_total_distance(best_map))
    print('ending best: ', best_cycle)
    return best_cycle, best_map


def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and 
    their connections, along with the cost for each connection 
    and the total cost.
    """
    
    best_map = find_best_cycle(road_map)[1]
    cities_df = pd.DataFrame(best_map, columns=('State','City','Longitude','Latitude'))
    return cities_df

def visualise(road_map):
    
    root = Tk()
    # implementation here
    root.mainloop()


def main():
    """
    Reads in, and prints out, the city data, then creates the "best"
    cycle and prints it out.
    """
    ## change read_cities to user input
    #roadmap = read_cities('C:\\Users\\samee\\Documents\\city-data-small.txt')
    #print('--->> Here is the original route (Distance: {}) <<---'.format(compute_total_distance(roadmap)))
    #print_cities(roadmap)
    road_map2 = [("Kentucky", "Frankfort", 38.197274, -84.86311),\
                ("Delaware", "Dover", 39.161921, -75.526755),\
                ("Minnesota", "Saint Paul", 44.95, -93.094),\
                ('Georgia', 'Atlanta', 33.76, -84.39),\
                ('Florida', 'Tallahassee', 30.45, -84.27)]
    print(compute_total_distance(road_map2))
    #visualise(roadmap)
    #print(swap_cities(roadmap,24,31))
    #print(compute_total_distance(shift_cities(roadmap)))
    #print(find_best_cycle(roadmap))
    
    #print('')
    #print('--->> Here is a shorter route (Distance: {}) <<---'.format(find_best_cycle(roadmap)[0]))
    #print(print_map(roadmap))



if __name__ == "__main__": 
    main()






''' 
still to do

best cycle: storing best map and best cycle outside of loop.
more tests!
visualise with tkinter
user input map file location
best map format, including distance. try not to use dataframe
check all functions return what they are supposed to
remove commented out code

'''


