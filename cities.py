import random, math
from tkinter import *


def read_cities(file_name):
    try:
        f = open(file_name,'r')
        line = f.readline().rstrip()
    
        cities_list = []
        
        while line:
            elements = line.split('\t')
            cities_list.append((elements[0], elements[1], float(elements[2]), float(elements[3])))
            line = f.readline().rstrip()
        f.close
        
        return cities_list
  
    except Exception:
        print('>> ERROR: Unable to find file! Please check location and try again. <<')
        
    
def print_cities(road_map):
    """
    Prints a list of cities, along with their locations. 
    Print only one or two digits after the decimal point.
    """    
    print('---> The original map (total distance {}) <---'.format(compute_total_distance(road_map)))
    for i, location in enumerate(road_map):
        print('{}. {}, {}: ({},{})'.format(i, location[1], \
              location[0], round(location[2],1), round(location[3],1)))
    print('')
    

def compute_total_distance(road_map):
    """
    Returns, as a floating point number, the sum of the distances of all 
    the connections in the `road_map`. Remember that it's a cycle, so that 
    (for example) in the initial `road_map`, Wyoming connects to Alabama...
    """
    distances = []

    for i, city in enumerate(road_map):
        from_lat, to_lat = road_map[(i-1) % len(road_map)][2], road_map[i][2]
        from_long, to_long = road_map[(i-1) % len(road_map)][3], road_map[i][3]
        distances.append(math.sqrt((from_long - to_long)**2 + (from_lat - to_lat)**2))

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
    
    new_road_map = road_map
    
    try:
        new_road_map[index1], new_road_map[index2] = \
        new_road_map[index2], new_road_map[index1]
        return (new_road_map, compute_total_distance(new_road_map))
    
    except Exception as e:
        print('Error swapping cities: '+str(e))


def shift_cities(road_map):
    """
    For every index i in the `road_map`, the city at the position i moves
    to the position i+1. The city at the last position moves to the position
    0. Return the new road map. 
    """
    shifted_road_map = []
    
    for i, city in enumerate(road_map):
        shifted_road_map.append(road_map[(i-1) % len(road_map)])

    return shifted_road_map


def find_best_cycle(road_map):
    """
    Using a combination of `swap_cities` and `shift_cities`, 
    try `10000` swaps/shifts, and each time keep the best cycle found so far. 
    After `10000` swaps/shifts, return the best cycle found so far.
    Use randomly generated indices for swapping.
    """
    
    best_map = road_map
    attempt_map = road_map
    best_cycle = compute_total_distance(best_map)
    #print('starting best: ', best_cycle)
    #print('computed best: ', compute_total_distance(best_map))
    #print('starting map', [(i, city) for (i, city) in enumerate(attempt_map)])
    #print('starting best cycle', best_cycle)
    i = 1
    
    while i <= 10:
        #try:  
            #attempt_map = road_map  ### AMEND THIS ####
            #print(i, 'best', best_cycle)
            #print(i, '### attempt map ###')
            #print([(num, city) for (num, city) in enumerate(attempt_map)])
            #print(i, 'best cycle so far', best_cycle)
            rand_idx1 = random.randint(0, len(best_map)-1)
            rand_idx2 = random.randint(0, len(best_map)-1)
            #print(i, rand_idx1, rand_idx2)
            (new_map, distance) = swap_cities(best_map, rand_idx1, rand_idx2)
            #print('new_map', new_map)
            print('new dist', distance)
            print('before checking against new dist, best cycle: ', best_cycle)
            if distance < best_cycle:
                #best_cycle = distance
                print('distance updated', best_cycle, distance)
                best_map = new_map
                #print('### best map ###', compute_total_distance(best_map), best_cycle)
                #print([(num, city) for (num, city) in enumerate(best_map)])
                #attempt_map = best_map
                #print('### new attempt map ###', compute_total_distance(best_map))
                #print([(num, city) for (num, city) in enumerate(attempt_map)])        
            else:
                #print('#### No better. now map has shifted. ####')
                #print('### best map unchanged ###', compute_total_distance(best_map), best_cycle)
                #print('best map --> ', [(num, city) for (num, city) in enumerate(best_map)])  
                best_map = shift_cities(new_map) 
                #print('attempt map -->',[(num, city) for (num, city) in enumerate(attempt_map)])
            #print('attempt map updated with new map?', attempt_map == new_map)
            i += 1
        #except Exception as e:
            #print('Error: '+str(e))
        #attempt_map = shift_cities(road_map)
        #i += 1
    
    #print('best dist:', compute_total_distance(best_map))
    #print('ending best: ', best_cycle)
    return best_cycle, best_map


def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and 
    their connections, along with the cost for each connection 
    and the total cost.
    """
    best = find_best_cycle(road_map)

    print('---> The best map (total distance {}) <---'.format(best[0]))
    for i, location in enumerate(best[1]):
        print('{}. {}, {}'.format(i, location[1], location[0]))
    print('')


def visualise(road_map):
    
    #best_map = find_best_cycle(road_map)[1]
       
    root = Tk()
    root.title("TSP: Best Map")
    
    canvas_scale = 3
    canvas_margin = 50
    canvas_height = (180 * canvas_scale) + canvas_margin
    canvas_width = (360 * canvas_scale) + canvas_margin
    
    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='#EFCB9B')
    canvas.pack()
    
    # Draw and Label the Lat/Long lines
    canvas.create_line(canvas_width/2, canvas_margin, canvas_width/2, canvas_height-canvas_margin, dash=(3,1))
    canvas.create_line(canvas_margin, canvas_height/2, canvas_width-canvas_margin, canvas_height/2, dash=(3,1))
    canvas.create_text(canvas_width/2, canvas_margin*0.75, text='Latitude')
    canvas.create_text(canvas_margin-10, (canvas_height/2)-10, text='Longitude')
  
    # Latitude Markers - 90 degrees (with text)
    canvas.create_line(canvas_width/2, canvas_margin, (canvas_width/2)-5, canvas_margin)
    canvas.create_text((canvas_width/2)+13, canvas_margin, text='+90')
        
    canvas.create_line(canvas_width/2, canvas_height-canvas_margin, (canvas_width/2)-5, canvas_height-canvas_margin)
    canvas.create_text((canvas_width/2)+13, canvas_height-canvas_margin, text='-90')
    
    # Latitude Markets- 45 degrees (no text)
    canvas.create_line(canvas_width/2, (canvas_height/4)+(canvas_margin/2), (canvas_width/2)-5, (canvas_height/4)+(canvas_margin/2))
    canvas.create_line(canvas_width/2, (canvas_height/4)*3-(canvas_margin/2), (canvas_width/2)-5, (canvas_height/4)*3-(canvas_margin/2))
    
    
    # Longitude Markers - 180 degrees (with text)
    canvas.create_line(canvas_margin, canvas_height/2, canvas_margin, (canvas_height/2)+5)
    canvas.create_text(canvas_margin, (canvas_height/2)+10, text='-180')
    
    canvas.create_line(canvas_width-canvas_margin, canvas_height/2, canvas_width-canvas_margin, (canvas_height/2)+5)
    canvas.create_text(canvas_width-canvas_margin, (canvas_height/2)+10, text='+180')
    
    # Longitude Markers - 90 degrees (no text)
    canvas.create_line((canvas_width/4)+(canvas_margin/2), canvas_height/2, (canvas_width/4)+(canvas_margin/2), (canvas_height/2)+5)    
    canvas.create_line((canvas_width/4)*3-(canvas_margin/2), canvas_height/2, (canvas_width/4)*3-(canvas_margin/2), (canvas_height/2)+5)    
    

    # Origin
    canvas.create_oval((canvas_width/2)-2 , (canvas_height/2)-2, (canvas_width/2)+2, (canvas_height/2)+2)
    
       
    for state, city, lat, long in road_map: #change to best_map
        adj_lat = (canvas_height/2) - (lat * canvas_scale)
        adj_long = (canvas_width/2) + (long * canvas_scale)
        canvas.create_oval(adj_long-15, adj_lat-15, adj_long+15, adj_lat+15)
        canvas.create_text(adj_long-0, adj_lat-0, text=str(city), font="Times 8 italic")
        print(lat,long)
        
    
    root.mainloop()


def main():
    """
    Reads in, and prints out, the city data, then creates the "best"
    cycle and prints it out.
    """
    roadmap = read_cities(input('Please enter the file location: '))
    print('')
    
    try:    
        #print_cities(roadmap)
        #print(compute_total_distance(roadmap))
        #print(swap_cities(roadmap,2,60))
        #print(shift_cities(roadmap))
        #print(compute_total_distance(shift_cities(roadmap)))
        #print(find_best_cycle(roadmap))
        #print_map(roadmap)
        #print('Note: Visualise function opens in a new window.')
        visualise(roadmap)
        
    except Exception as e:
        print(str(e))


if __name__ == "__main__": 
    main()






''' 
still to do

best cycle: storing best map and best cycle outside of loop.
more tests!
visualise - adjusted coords, additional formatting etc.
best map format, including distance. try not to use dataframe
check all functions return what they are supposed to
remove commented out code
better error classification
coding style, check spacing etc (PEP8)
'''

# C:\Users\samee\Documents\city-data-small.txt
# C:\Users\samee\Documents\POP1\pop-one-project-skhan59\city-data.txt
