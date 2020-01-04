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
    """    
    
    print('*** THE ORIGINAL MAP (TOTAL DISTANCE {}) ***'.format(compute_total_distance(road_map)))
    print('')
    for i, location in enumerate(road_map):
        print('- {}, {}: ({},{})'.format(location[1], \
              location[0], round(location[2],1), round(location[3],1)))
    print('____________________________________________________________________')
    print('')
    
def compute_total_distance(road_map):
    """
    Returns, as a floating point number, the sum of the distances of all 
    the connections in the `road_map`. 
    """
    
    distances = distances_and_limits(road_map)[0]
    return round(sum(distances),2)
    
def swap_cities(road_map, index1, index2):
    """
    Take the city at location `index` in the `road_map`, and the 
    city at location `index2`, swap their positions in the `road_map`, 
    compute the new total distance.
    """
    
    new_road_map = road_map
    
    try:
        new_road_map[index1], new_road_map[index2] = \
        new_road_map[index2], new_road_map[index1]
        return (new_road_map, compute_total_distance(new_road_map))
    
    except Exception as e:
        print('Error with swap_cities function: '+str(e))

def shift_cities(road_map):
    """
    For every index i in the `road_map`, the city at the position i moves
    to the position i+1. The city at the last position moves to the position
    0. Return the new road map. 
    """
    
    shifted_road_map = [road_map[(i-1) % len(road_map)] for i, city in enumerate(road_map)]
    return shifted_road_map

def find_best_cycle(road_map):
    """
    Using a combination of `swap_cities` and `shift_cities`, 
    try `10000` swaps/shifts, and each time keep the best cycle found so far. 
    After `10000` swaps/shifts, return the best cycle found so far.
    Use randomly generated indices for swapping.
    """
    
    best_cycle = road_map
    best_dist = compute_total_distance(best_cycle)
    i = 0
        
    while i < 10000:
        try:
            attempt_map = shift_cities(best_cycle)
            rand_idx1 = random.randint(0, len(best_cycle)-1)
            rand_idx2 = random.randint(0, len(best_cycle)-1)
            (new_map, distance) = swap_cities(attempt_map, rand_idx1, rand_idx2)
            if distance < best_dist:
                best_dist = distance
                best_cycle = new_map
            i += 1
        except Exception as e:
            print('Error with find_best_cycle function: '+str(e))
   
    return best_cycle

def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and 
    their connections, along with the cost for each connection 
    and the total cost.
    """
    
    distances = distances_and_limits(road_map)[0]

    print('*** THE BEST ROUTE FOUND (TOTAL DISTANCE {}) ***'.format(round(sum(distances),1)))
    print('')

    for i, location in enumerate(road_map):
        print('Trip #{}: {}, {} ----> {}, {}'.format(i+1, \
              road_map[(i-1) % len(road_map)][1], road_map[(i-1) % len(road_map)][0], \
              road_map[i][1], road_map[i][0]))
        print('Distance = {}'.format(round(distances[i],2)))
        print('')
    print('____________________________________________________________________')
    print('')

def distances_and_limits(road_map):
    """
    Computes and returns euclidean distances, 
    plus max/min co-ords to be used in visualise function.
    """
    
    distance_list = [math.sqrt((road_map[(i-1) % len(road_map)][3] - road_map[i][3])**2 + \
                           (road_map[(i-1) % len(road_map)][2] - road_map[i][2])**2) \
    for i, city in enumerate(road_map)]
    
    lats_list = [road_map[i][2] for i, city in enumerate(road_map)]
    longs_list = [road_map[i][3] for i, city in enumerate(road_map)]
    
    min_lat, max_lat = min(lats_list), max(lats_list)
    min_long, max_long = min(longs_list), max(longs_list)

    return distance_list, min_lat, max_lat, min_long, max_long
    
def visualise(road_map):
    """
    Visualisation of route using tkinter module
    """

    canvas_scale = 3
    canvas_margin = 30
    canvas_height = (180 * canvas_scale) + canvas_margin
    canvas_width = (360 * canvas_scale) + canvas_margin
   
    limits = distances_and_limits(road_map)[1:]
    min_lat, max_lat = limits[0], limits[1]
    min_long, max_long = limits[2], limits[3]
       
    
    ''' Canvas 1  '''
    frame1 = Tk()
    frame1.title("Traveling Salesman Problem | Best Route | Full Scale View | Total Distance: {}".format(compute_total_distance(road_map)))

    canvas1 = Canvas(frame1, width = canvas_width, \
                     height = canvas_height, bg='#FCEDBD')
    canvas1.pack()
        
    # Origin and Legend
    canvas1.create_oval((canvas_width/2)-2 , (canvas_height/2)-2, (canvas_width/2)+2, (canvas_height/2)+2, fill='black')
    canvas1.create_text(canvas_width/2, 10, text='| WHOLE WORLD VIEW |', font='arial 10 bold')
    
    # Draw and Label the Lat/Long lines
    canvas1.create_line(canvas_width/2, canvas_margin, canvas_width/2, canvas_height-canvas_margin, dash=(3,1))
    canvas1.create_line(canvas_margin, canvas_height/2, canvas_width-canvas_margin, canvas_height/2, dash=(3,1))
    canvas1.create_text(canvas_width/2, canvas_height-(canvas_margin/2), text='Latitude', font='arial 8 italic')
    canvas1.create_text(canvas_margin+5, (canvas_height/2)-10, text='Longitude', font='arial 8 italic')
  
    # Latitude Markers - 90 degrees
    canvas1.create_line(canvas_width/2, canvas_margin, (canvas_width/2)-5, canvas_margin)
    canvas1.create_text((canvas_width/2)+13, canvas_margin, text='+90')
        
    canvas1.create_line(canvas_width/2, canvas_height-canvas_margin, (canvas_width/2)-5, canvas_height-canvas_margin)
    canvas1.create_text((canvas_width/2)+13, canvas_height-canvas_margin, text='-90')
    
    # Latitude Markets- 45 degrees
    canvas1.create_line(canvas_width/2, (canvas_height/4)+(canvas_margin/2), (canvas_width/2)-5, (canvas_height/4)+(canvas_margin/2))
    canvas1.create_text((canvas_width/2)+13, (canvas_height/4)+(canvas_margin/2), text='+45')    
    
    canvas1.create_line(canvas_width/2, (canvas_height/4)*3-(canvas_margin/2), (canvas_width/2)-5, (canvas_height/4)*3-(canvas_margin/2))
    canvas1.create_text((canvas_width/2)+13, (canvas_height/4)*3-(canvas_margin/2), text='-45') 
        
    # Longitude Markers - 180 degrees
    canvas1.create_line(canvas_margin, canvas_height/2, canvas_margin, (canvas_height/2)+5)
    canvas1.create_text(canvas_margin, (canvas_height/2)+10, text='-180')
    
    canvas1.create_line(canvas_width-canvas_margin, canvas_height/2, canvas_width-canvas_margin, (canvas_height/2)+5)
    canvas1.create_text(canvas_width-canvas_margin, (canvas_height/2)+10, text='+180')
    
    # Longitude Markers - 90 degrees
    canvas1.create_line((canvas_width/4)+(canvas_margin/2), canvas_height/2, (canvas_width/4)+(canvas_margin/2), (canvas_height/2)+5)    
    canvas1.create_text((canvas_width/4)+(canvas_margin/2), (canvas_height/2)+10, text='-90')    
    
    canvas1.create_line((canvas_width/4)*3-(canvas_margin/2), canvas_height/2, (canvas_width/4)*3-(canvas_margin/2), (canvas_height/2)+5)    
    canvas1.create_text((canvas_width/4)*3-(canvas_margin/2), (canvas_height/2)+10, text='+90') 

    lat_adj_factor1 = (canvas_height-(canvas_margin*2)) / 180
    long_adj_factor1 = (canvas_width-(canvas_margin*2)) / 360
    
    # Rescale and Draw Cities
    for i, location in enumerate(road_map):
        adj_lat = canvas_height - canvas_margin - ((location[2]-(-90)) * lat_adj_factor1)
        adj_long = canvas_margin + ((location[3]-(-180)) * long_adj_factor1)
        canvas1.create_oval(adj_long-3, adj_lat-3, adj_long+3, adj_lat+3, fill='red')

        prev_lat, prev_long = road_map[(i-1)%len(road_map)][2], road_map[(i-1)%len(road_map)][3]
        adj_prev_lat = canvas_height - canvas_margin - ((prev_lat-(-90)) * lat_adj_factor1)
        adj_prev_long = canvas_margin + ((prev_long-(-180)) * long_adj_factor1)
        canvas1.create_line(adj_prev_long, adj_prev_lat, adj_long, adj_lat, arrow='last', fill='green')

                
    ''' Canvas 2 - ZOOMED IN '''
    frame2 = Tk()
    frame2.title("Traveling Salesman Problem | Best Route | Zoomed In View | Total Distance: {}".format(compute_total_distance(road_map)))
    
    canvas2 = Canvas(frame2, width = canvas_width, \
                     height = canvas_height, bg='#FCEDBD') 
    canvas2.pack()

    lat_range = max_lat - min_lat
    long_range = max_long - min_long
    lat_adj_factor2 = (canvas_height-(canvas_margin*4)) / lat_range
    long_adj_factor2 = (canvas_width-(canvas_margin*4)) / long_range    
    
    # Origin and legend
    canvas2.create_oval(canvas_width-canvas_margin-1, canvas_height-canvas_margin-1, canvas_width-canvas_margin+1, canvas_height-canvas_margin+1)
    canvas2.create_text(canvas_width/2, 10, text='| ZOOMED IN VIEW |', font='arial 10 bold')   
    
    # Draw Lat/Long lines
    canvas2.create_line(canvas_width-canvas_margin, canvas_margin, canvas_width-canvas_margin, canvas_height-canvas_margin, dash=(5,2))
    canvas2.create_line(canvas_margin, canvas_height-canvas_margin, canvas_width-canvas_margin, canvas_height-canvas_margin, dash=(5,2))
    canvas2.create_line(canvas_margin, canvas_margin, canvas_margin, canvas_height-canvas_margin, dash=(5,2))
    canvas2.create_line(canvas_margin, canvas_margin, canvas_width-canvas_margin, canvas_margin, dash=(5,2))
    
    # Inner Grid
    for i in range(2, int(canvas_height/canvas_margin)-1):
        canvas2.create_line(canvas_margin, canvas_margin*i, canvas_width-canvas_margin, canvas_margin*i, fill='grey', dash=(4,2))

    for i in range(2, int(canvas_width/canvas_margin)-1):
        canvas2.create_line(canvas_margin*i, canvas_margin, canvas_margin*i, canvas_height-canvas_margin, fill='grey', dash=(4,2))
            
    # Latitude Markers and Text
    canvas2.create_line(canvas_width-canvas_margin, canvas_height-(canvas_margin*2), (canvas_width-canvas_margin)+5, canvas_height-(canvas_margin*2))
    canvas2.create_text(canvas_width-canvas_margin+15, canvas_height-(canvas_margin*2), text=str(round(min_lat)), font='arial 8 italic')
    
    canvas2.create_line(canvas_width-canvas_margin, canvas_margin*2, (canvas_width-canvas_margin)+5, canvas_margin*2)    
    canvas2.create_text(canvas_width-canvas_margin+15, canvas_margin*2, text=str(round(max_lat)), font='arial 8 italic')
    
    canvas2.create_line(canvas_margin, canvas_height-(canvas_margin*2), canvas_margin-5, canvas_height-(canvas_margin)*2)
    canvas2.create_text(canvas_margin-20, canvas_height-(canvas_margin*2), text=str(round(min_lat)), font='arial 8 italic')
    
    canvas2.create_line(canvas_margin, canvas_margin*2, canvas_margin-5, canvas_margin*2)
    canvas2.create_text(canvas_margin-20, canvas_margin*2, text=str(round(max_lat)), font='arial 8 italic')
    
    mid_lat = round(min_lat + (lat_range/2))
    canvas2.create_line(canvas_margin, canvas_height/2, canvas_margin-5, canvas_height/2)
    canvas2.create_text(canvas_margin-20, canvas_height/2, text=str(mid_lat), font='arial 8 italic')

    canvas2.create_line(canvas_width-canvas_margin, canvas_height/2, (canvas_width-canvas_margin)+5, canvas_height/2)
    canvas2.create_text((canvas_width-canvas_margin)+15, canvas_height/2, text=str(mid_lat), font='arial 8 italic')    
    
    
    # Longitude Markers and Text
    canvas2.create_line(canvas_margin*2, canvas_height-canvas_margin, canvas_margin*2, (canvas_height-canvas_margin)+5)
    canvas2.create_text(canvas_margin*2, canvas_height-canvas_margin+10, text=str(round(min_long)), font='arial 8 italic')
    
    canvas2.create_line(canvas_margin*2, canvas_margin, canvas_margin*2, canvas_margin-5)
    canvas2.create_text(canvas_margin*2, canvas_margin-10, text=str(round(min_long)), font='arial 8 italic')
    
    canvas2.create_line(canvas_width-(canvas_margin*2), canvas_height-canvas_margin, canvas_width-(canvas_margin*2), (canvas_height-canvas_margin)+5)
    canvas2.create_text(canvas_width-(canvas_margin*2), canvas_height-canvas_margin+10, text=str(round(max_long)), font='arial 8 italic')
    
    canvas2.create_line(canvas_width-(canvas_margin*2), canvas_margin, canvas_width-(canvas_margin*2), canvas_margin-5)
    canvas2.create_text(canvas_width-(canvas_margin*2), canvas_margin-10, text=str(round(max_long)), font='arial 8 italic')
    
    mid_long = round(min_long + (long_range/2))
    canvas2.create_line(canvas_width/2, canvas_height-canvas_margin, canvas_width/2, (canvas_height-canvas_margin)+5)
    canvas2.create_text(canvas_width/2, (canvas_height-canvas_margin)+10, text=str(mid_long), font='arial 8 italic')

    canvas2.create_line(canvas_width/2, canvas_margin, canvas_width/2, canvas_margin-5)
    canvas2.create_text(canvas_width/2, canvas_margin-10, text=str(mid_long), font='arial 8 italic')
    
    # Rescale and Draw Cities
    for i, location in enumerate(road_map):
        adj_lat_zoom = (canvas_height - (2*canvas_margin)) - ((location[2]-min_lat) * lat_adj_factor2)
        adj_long_zoom = (canvas_margin*2) + ((location[3]-min_long) * long_adj_factor2)
        canvas2.create_oval(adj_long_zoom-11, adj_lat_zoom-11, adj_long_zoom+11, adj_lat_zoom+11, fill='#EC7068')
        canvas2.create_text(adj_long_zoom, adj_lat_zoom, text=str(i), font='arial 12 bold')
        canvas2.create_text(adj_long_zoom, adj_lat_zoom-18, text=str(location[1]), font='arial 9')
        
        prev_lat, prev_long = road_map[(i-1)%len(road_map)][2], road_map[(i-1)%len(road_map)][3]
        adj_prev_lat = (canvas_height - (2*canvas_margin)) - ((prev_lat-min_lat) * lat_adj_factor2)
        adj_prev_long = (canvas_margin*2) + ((prev_long-min_long) * long_adj_factor2)
        canvas2.create_line(adj_prev_long, adj_prev_lat+3, adj_long_zoom, adj_lat_zoom+3, arrow='last', fill='green', width=1)
            
    frame1.mainloop()
    frame2.mainloop()

def main():
    """
    Reads in, and prints out, the city data, then creates the "best"
    cycle and prints it out.
    """
    
    roadmap = read_cities(input('Please enter the file location: '))
    print('')
    print_cities(roadmap)
    best = find_best_cycle(roadmap)
    print_map(best)
    
    try:
        run_viz = input('>> Run visualisation function? (Y/N): ')
        print('')
        while run_viz != 'N':
            if run_viz == 'Y':
                print('Two windows opened. Please close to end.')
                visualise(best)
                break
            else:
                print('Please type only Y or N')
                run_viz = input('>> Run visualisation function? (Y/N): ')
    except Exception as e:
        print(str(e))


if __name__ == "__main__": 
    main()
