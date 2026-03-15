import math

def to_deg(rad):
    return rad * (180/math.pi)

def to_rad(deg):
    return deg * math.pi / 180 

RAD_90 = to_rad(90)
RAD_180 = to_rad(180)
PI = math.pi

def calculate_2d_axis_angle(rise, run):
    '''returns radians'''
    round_rise = round(rise, 2)
    round_run = round(run, 2)
    if round_rise == 0 and round_run == 0:
        return None
    
    ''' take arctan of round_rise over round_run (opposite over adjacent) to get angle '''
    if round_rise > 0 and round_run > 0 or (round_rise == 0 and round_run > 0):
        quadrant = 0
    if round_rise > 0 and round_run < 0 or (round_rise > 0 and round_run == 0):
        quadrant = PI/2
    if round_rise < 0 and round_run < 0 or (round_rise == 0 and round_run < 0):
        quadrant = PI
    if round_rise < 0 and round_run > 0 or (round_rise < 0 and round_run == 0):
        quadrant = PI* 3/2 
    angle = math.atan(rise/run) if round_run != 0 else 0 
    if angle > 0:
        print(f"calculated angle {to_deg(angle + quadrant)}")
        return angle + quadrant
    print(f"calculated angle {to_deg(quadrant + PI/2 + abs(angle))}")
    return quadrant + PI/2 + angle

# calculate new realtive position by using the radius and the new angle
def rotate_on_axis(starting_angle, rotation_angle, radius, clockwise_rotation = -1):
    print(f"rotating {to_deg(rotation_angle)}")
    new_1 = round(math.cos(starting_angle + rotation_angle*(clockwise_rotation))*radius, 5)
    new_2 = round(math.sin(starting_angle + rotation_angle*(clockwise_rotation))*radius, 5)
    return new_1, new_2 


# when doing rotation we always calculate with the graph orientation where positive values 
# for axis are the top right quadrant, in other words, we draw the graph with axis1 and axis2
# with positive values as the top right
# In a right handed coordinate systems x axis rotation is calculated looking from -x toward +x with 
# the y axis pointing up and the z axis to the right
# In a right handed coordinate systems y axis rotation is calculated looking from +y toward -y with 
# the x axis pointing up and the z axis to the right
# In a right handed coordinate systems z axis rotation is calculated looking from +z toward -z with 
# the y axis pointing up and the x axis to the right
def find_per_plane_axis_angle(object_coord, vertex_coord):
    '''returns a vector [x,y,z] where x y and z are the respective angles the object will need to be rotated
    to in order to be orthogonal to the vertex'''
    z_rise_index = 1
    z_run_index = 0
    y_rise_index = 0
    y_run_index = 2
    x_rise_index = 1
    x_run_index = 2
    x_rise = object_coord[x_rise_index] - vertex_coord[x_rise_index]
    x_run = object_coord[x_run_index] - vertex_coord[x_run_index]
    y_rise = object_coord[y_rise_index] - vertex_coord[y_rise_index]
    y_run = object_coord[y_run_index] - vertex_coord[y_run_index]
    z_rise = object_coord[z_rise_index] - vertex_coord[z_rise_index]
    z_run = object_coord[z_run_index] - vertex_coord[z_run_index]
    return [calculate_2d_axis_angle(x_rise, x_run), calculate_2d_axis_angle(y_rise, y_run), calculate_2d_axis_angle(z_rise, z_run)]

def axis_rotation_about_vertex(object_coord, vertex_coord, axis_no, angle, clockwise):
    if angle == 0:
        return object_coord
    rise = 0
    run = 0
    # rise is y and run is z for x axis rotation
    if axis_no == 0:
        rise = 1 
        run = 2 
    # rise is x and run is z for y axis rotation
    if axis_no == 1:
        rise = 0
        run = 2
    # rise is y and run is x for z axis rotation
    if axis_no == 2:
        rise = 1
        run = 0
    init_rise = object_coord[rise] - vertex_coord[rise]
    init_run = object_coord[run] - vertex_coord[run]
    # run, rise
    radius = math.hypot(init_run, init_rise)
    print(f"radius {radius}")
    run_after_rotation, rise_after_rotation = rotate_on_axis(calculate_2d_axis_angle(init_rise, init_run), angle, radius, clockwise)
    object_coord[run] = vertex_coord[run] + run_after_rotation 
    object_coord[rise] = vertex_coord[rise] + rise_after_rotation 
    return object_coord 

def vertex_rotation(angles = [0,0,0], vertex_location = [0,0,0], obj_coord = [0,0,0], clockwise = [-1,-1,-1]):
    obj_coord = axis_rotation_about_vertex(obj_coord, vertex_location, 0, angles[0], clockwise[0])
    obj_coord = axis_rotation_about_vertex(obj_coord, vertex_location, 1, angles[1], clockwise[1])
    obj_coord = axis_rotation_about_vertex(obj_coord, vertex_location, 2, angles[2], clockwise[2])
    print(f'New Object coord {obj_coord}')
    return obj_coord
