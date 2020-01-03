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
    print('*** THE ORIGINAL MAP (TOTAL DISTANCE {}) ***'.format(compute_total_distance(road_map)))
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
    distances = distances_and_limits(road_map)[0]
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
    
    best_map = road_map
    best_cycle = compute_total_distance(best_map)
    i = 0
        
    while i < 10000:
        try:
            attempt_map = shift_cities(best_map)
            rand_idx1 = random.randint(0, len(best_map)-1)
            rand_idx2 = random.randint(0, len(best_map)-1)
            (new_map, distance) = swap_cities(attempt_map, rand_idx1, rand_idx2)
            if distance < best_cycle:
                best_cycle = distance
                best_map = new_map
            i += 1
        except Exception as e:
            print('Error with find_best_cycle function: '+str(e))
   
    return best_cycle, best_map


def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and 
    their connections, along with the cost for each connection 
    and the total cost.
    """
    best = find_best_cycle(road_map)
    distances = distances_and_limits(best[1])[0]

    print('*** THE BEST ROUTE FOUND (TOTAL DISTANCE {}) ***'.format(best[0]))
    print('')

    for i, location in enumerate(best[1]):
        print('Trip #{}: {}, {} ----> {}, {}'.format(i+1, \
              best[1][(i-1) % len(road_map)][1], best[1][(i-1) % len(road_map)][0], \
              best[1][i][1], best[1][i][0]))
        print('Distance = {}'.format(round(distances[i],2)))
        print('')


def distances_and_limits(road_map):
    
    distance_list = [math.sqrt((road_map[(i-1) % len(road_map)][3] - road_map[i][3])**2 + \
                           (road_map[(i-1) % len(road_map)][2] - road_map[i][2])**2) \
    for i, city in enumerate(road_map)]
    
    lats_list = [road_map[i][2] for i, city in enumerate(road_map)]
    longs_list = [road_map[i][3] for i, city in enumerate(road_map)]
    min_lat, max_lat = min(lats_list), max(lats_list)
    min_long, max_long = min(longs_list), max(longs_list)

    return distance_list, min_lat, max_lat, min_long, max_long
    
def visualise(road_map):
    
    #best_map = find_best_cycle(road_map)[1]
       
    root = Tk()
    root.title("TSP: Best Route")
    
    canvas_scale = 2
    canvas_margin = 30
    canvas_height = (180 * canvas_scale) + canvas_margin
    canvas_width = (360 * canvas_scale) + canvas_margin
    
    ########### Canvas 1 - WORLD VIEW ###########
    canvas1 = Canvas(root, width=canvas_width, height=canvas_height, bg='#EFCB9B')
    canvas1.pack()
        
    # Origin and Legend
    canvas1.create_oval((canvas_width/2)-2 , (canvas_height/2)-2, (canvas_width/2)+2, (canvas_height/2)+2, fill='black')
    canvas1.create_text(canvas_width/4, 10, text='| WHOLE WORLD VIEW |', font='arial 10 bold')
    
    # Draw and Label the Lat/Long lines
    canvas1.create_line(canvas_width/2, canvas_margin, canvas_width/2, canvas_height-canvas_margin, dash=(3,1))
    canvas1.create_line(canvas_margin, canvas_height/2, canvas_width-canvas_margin, canvas_height/2, dash=(3,1))
    canvas1.create_text(canvas_width/2, canvas_margin*0.65, text='Latitude', font='arial 8 italic')
    canvas1.create_text(canvas_margin+5, (canvas_height/2)-10, text='Longitude', font='arial 8 italic')
  
    # Latitude Markers - 90 degrees (with text)
    canvas1.create_line(canvas_width/2, canvas_margin, (canvas_width/2)-5, canvas_margin)
    canvas1.create_text((canvas_width/2)+13, canvas_margin, text='+90')
        
    canvas1.create_line(canvas_width/2, canvas_height-canvas_margin, (canvas_width/2)-5, canvas_height-canvas_margin)
    canvas1.create_text((canvas_width/2)+13, canvas_height-canvas_margin, text='-90')
    
    # Latitude Markets- 45 degrees (no text)
    canvas1.create_line(canvas_width/2, (canvas_height/4)+(canvas_margin/2), (canvas_width/2)-5, (canvas_height/4)+(canvas_margin/2))
    canvas1.create_line(canvas_width/2, (canvas_height/4)*3-(canvas_margin/2), (canvas_width/2)-5, (canvas_height/4)*3-(canvas_margin/2))
        
    # Longitude Markers - 180 degrees (with text)
    canvas1.create_line(canvas_margin, canvas_height/2, canvas_margin, (canvas_height/2)+5)
    canvas1.create_text(canvas_margin, (canvas_height/2)+10, text='-180')
    
    canvas1.create_line(canvas_width-canvas_margin, canvas_height/2, canvas_width-canvas_margin, (canvas_height/2)+5)
    canvas1.create_text(canvas_width-canvas_margin, (canvas_height/2)+10, text='+180')
    
    # Longitude Markers - 90 degrees (no text)
    canvas1.create_line((canvas_width/4)+(canvas_margin/2), canvas_height/2, (canvas_width/4)+(canvas_margin/2), (canvas_height/2)+5)    
    canvas1.create_line((canvas_width/4)*3-(canvas_margin/2), canvas_height/2, (canvas_width/4)*3-(canvas_margin/2), (canvas_height/2)+5)    

    # Rescale and Draw Cities
    for state, city, lat, long in road_map: #change to best_map
        adj_lat = (canvas_height/2) - (lat * canvas_scale)
        adj_long = (canvas_width/2) + (long * canvas_scale)
        canvas1.create_oval(adj_long-2, adj_lat-2, adj_long+2, adj_lat+2, fill='red')
        #canvas.create_text(adj_long-0, adj_lat-0, text=str(city), font="Times 8 italic")
        #print(lat,long)
        
        
    ########### Canvas 2 - ZOOMED IN ###########
    canvas2 = Canvas(root, width=canvas_width, height=canvas_height, bg='#EFCB9B')
    canvas2.pack()
    
    limits = distances_and_limits(road_map)[1:]
    min_lat, max_lat = limits[0], limits[1]
    min_long, max_long = limits[2], limits[3]
    
    lat_axis_length = max_lat - min_lat
    long_axis_length = max_long - min_long
    
    # Origin and legend
    canvas2.create_oval(canvas_width-canvas_margin-1, canvas_height-canvas_margin-1, canvas_width-canvas_margin+1, canvas_height-canvas_margin+1)
    canvas2.create_text(canvas_width/4, 10, text='| ZOOMED IN VIEW |', font='arial 10 bold')   
    
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
    canvas2.create_text(canvas_width-canvas_margin+15, canvas_height-(canvas_margin*2), text=str(round(min_lat)), font='arial 7 italic')
    
    canvas2.create_line(canvas_width-canvas_margin, canvas_margin*2, (canvas_width-canvas_margin)+5, canvas_margin*2)    
    canvas2.create_text(canvas_width-canvas_margin+15, canvas_margin*2, text=str(round(max_lat)), font='arial 7 italic')
    
    canvas2.create_line(canvas_margin, canvas_height-(canvas_margin*2), canvas_margin-5, canvas_height-(canvas_margin)*2)
    canvas2.create_text(canvas_margin-20, canvas_height-(canvas_margin*2), text=str(round(min_lat)), font='arial 7 italic')
    
    canvas2.create_line(canvas_margin, canvas_margin*2, canvas_margin-5, canvas_margin*2)
    canvas2.create_text(canvas_margin-20, canvas_margin*2, text=str(round(max_lat)), font='arial 7 italic')
    
    
    # Longitude Markers and Text
    canvas2.create_line(canvas_margin*2, canvas_height-canvas_margin, canvas_margin*2, (canvas_height-canvas_margin)+5)
    canvas2.create_text(canvas_margin*2, canvas_height-canvas_margin+10, text=str(round(min_long)), font='arial 7 italic')
    
    canvas2.create_line(canvas_margin*2, canvas_margin, canvas_margin*2, canvas_margin-5)
    canvas2.create_text(canvas_margin*2, canvas_margin-10, text=str(round(min_long)), font='arial 7 italic')
    
    canvas2.create_line(canvas_width-(canvas_margin*2), canvas_height-canvas_margin, canvas_width-(canvas_margin*2), (canvas_height-canvas_margin)+5)
    canvas2.create_text(canvas_width-(canvas_margin*2), canvas_height-canvas_margin+10, text=str(round(max_long)), font='arial 7 italic')
    
    canvas2.create_line(canvas_width-(canvas_margin*2), canvas_margin, canvas_width-(canvas_margin*2), canvas_margin-5)
    canvas2.create_text(canvas_width-(canvas_margin*2), canvas_margin-10, text=str(round(max_long)), font='arial 7 italic')
    
    # Rescale and Draw Cities
    for state, city, lat, long in road_map: #change to best_map
        adj_lat_zoom = canvas_height - (lat/90 * canvas_height)
        adj_long_zoom = canvas_width - (-long/180 * canvas_width)
        canvas2.create_oval(adj_long_zoom-3, adj_lat_zoom-3, adj_long_zoom+3, adj_lat_zoom+3, fill='red')
        print((lat, long), (adj_lat_zoom, adj_long_zoom))
        
    canvas2.create_oval(200,200,210,210)
    canvas2.create_oval(300,300,310,310)
    canvas2.create_oval(100,100,110,110)  
    canvas2.create_oval(canvas_margin-5,canvas_margin-5,canvas_margin+5,canvas_margin+5)
    
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
        print_map(roadmap)
        #print(distances_and_limits(roadmap))
        #print('Note: Visualise function opens in a new window.')
        #visualise(roadmap)
        
    except Exception as e:
        print(str(e))


if __name__ == "__main__": 
    main()






''' 
still to do

visualise - relevant dimensions only, additional formatting etc.
replace road_map with best_map where applicable


before submitting

more tests?
better error classification
check all functions return what they are supposed to
coding style, remove commented out code, check spacing etc
'''

# C:\Users\samee\Documents\city-data-small.txt
# C:\Users\samee\Documents\POP1\pop-one-project-skhan59\city-data.txt
