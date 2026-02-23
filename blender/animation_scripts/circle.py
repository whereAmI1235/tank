import math

def to_deg(rad):
    return rad * (180/math.pi)

def to_rad(deg):
    return deg * math.pi / 180 

RAD_90 = to_rad(90)
RAD_180 = to_rad(180)
PI = math.pi

def calculate_axis_angle(run, rise, relative_to):
    round_run = round(run, 2)
    round_rise = round(rise, 2)
    print(f"run {round_run} {relative_to}") 
    print(f"rise {round_rise} {relative_to}") 
    if round_rise == 0 and round_run == 0:
        return 0
    ''' take arctan of round_rise over round_run (opposite over adjacent) to get angle '''
    if round_rise > 0 and round_run > 0 or (round_rise == 0 and round_run > 0):
        quadrant = 0
    if round_rise > 0 and round_run < 0 or (round_rise > 0 and round_run == 0):
        quadrant = PI/2
    if round_rise < 0 and round_run < 0 or (round_rise == 0 and round_run < 0):
        quadrant = PI
    if round_rise < 0 and round_run > 0 or (round_rise < 0 and round_run == 0):
        quadrant = PI* 3/2 
    angle = abs(math.atan(rise/run)) if round_run != 0 else 0 
    print(f"current {relative_to} axis roatation angle {to_deg(angle + quadrant)}")
    return angle + quadrant

def rotate_on_axis(starting_angular_position, rotation_angle, radius, clockwise_rotation = -1):
    start_1 = round(math.cos(starting_angular_position)*radius, 5)
    start_2 = round(math.sin(starting_angular_position)*radius, 5)
    new_1 = round(math.cos(starting_angular_position + rotation_angle*(clockwise_rotation))*radius, 5)
    new_2 = round(math.sin(starting_angular_position + rotation_angle*(clockwise_rotation))*radius, 5)
    change_1 = round(new_1 - start_1,5)
    change_2 = round(new_2 - start_2,5)
    return change_1, change_2

def process_axis_rotation(object_coord, vertex_coord, axis_no, angle, clockwise):
    if angle == 0:
        return object_coord
    rise = 0
    run = 0
    axis_name = ''
    # rise is y and run is z for x axis rotation
    if axis_no == 0 :
        rise = 1 
        run = 2 
        axis_name = 'x'
    # rise is x and run is z for y axis rotation
    if axis_no == 1 :
        rise = 0
        run = 2
        axis_name = 'y'
    # rise is y and run is x for z axis rotation
    if axis_no == 2 :
        rise = 1
        run = 0
        axis_name = 'z'
    rise_change = object_coord[rise] - vertex_coord[rise]
    print(f"rise change {rise_change}")
    run_change = object_coord[run] - vertex_coord[run]
    print(f"run change {run_change}")
    # run, rise
    run_after, rise_after = rotate_on_axis(calculate_axis_angle(run_change, rise_change, axis_name), angle, math.hypot(run_change, rise_change), clockwise)
    object_coord[run] += run_after 
    object_coord[rise] += rise_after 
    return object_coord 

# when doing rotation we always calculate with the graph orientation where positive values 
# for axis are the top right quadrant, in other words, we draw the graph with axis1 and axis2
# with positive values as the top right
# In a right handed coordinate systems x axis rotation is calculated looking from -x toward +x with 
# the y axis pointing up and the z axis to the right
# In a right handed coordinate systems y axis rotation is calculated looking from +y toward -y with 
# the x axis pointing up and the z axis to the right
# In a right handed coordinate systems z axis rotation is calculated looking from +z toward -z with 
# the y axis pointing up and the x axis to the right
def vertex_rotation(angles = [0,0,0], vertex_location = [0,0,0], obj_coord = [0,0,0], clockwise = [-1,-1,-1]):
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 0, angles[0], clockwise[0])
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 1, angles[1], clockwise[1])
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 2, angles[2], clockwise[2])
    print(f'New Object coord {obj_coord}')
    return obj_coord
