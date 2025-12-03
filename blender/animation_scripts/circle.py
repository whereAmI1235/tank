import math

def to_deg(rad):
    return rad * (180/math.pi)

def to_rad(deg):
    return deg * math.pi / 180 

RAD_90 = to_rad(90)
RAD_180 = to_rad(180)
PI = math.pi

def get_distance_between_points(vec1, vec2):
    x_change = vec2[0] - vec1[0]
    y_change = vec2[1] - vec1[1]
    z_change = vec2[2] - vec1[2]
    hypot = math.sqrt(x_change ** 2 + y_change ** 2)
    radius = math.sqrt(hypot ** 2 + z_change ** 2) 
    return radius

def calculate_tangent_angle(radius, angle_deg):
    print(f"calculate tangent angle for {angle_deg}")
    angle_in_rad = to_rad(angle_deg)
    # cut a triangle into the circle with base x and 
    # height y
    x = radius * math.cos(angle_in_rad)
    y = radius * math.sin(angle_in_rad)
    # angle of triangle from the perimiter made when a vertical
    # line is drawn from x to the horizontal line going through 
    # the circle vertex (ie radius is the hypotenuse). Use arcsin to get angle
    delta = math.asin(x / radius)
    # subtract from the 90 degree angle required to for a tangent line for point 
    # x,y
    delta2 = RAD_90 - delta
    
    tan_angle = RAD_180 - (RAD_90 + delta2)
    print(f"tangent angle {to_deg(tan_angle) * -1}")
    return tan_angle * -1

def points_on_circle(r,n=100, starting_angle = 0):
    # starting angle, the angle orientation to start generating points at. In radians
    # ex PI/2 would be at the top of the circle
    start_position = starting_angle if starting_angle != 0 else 2*PI
    step = (2*PI) / n
    print(start_position)
    return [(round(math.cos(start_position-(step*x))*r, 2),round(math.sin(start_position-(step*x))*r,2)) for x in range(n)]

def calculate_axis_angle(run, rise):
    round_run = round(run, 2)
    round_rise = round(rise, 2)
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
    print(f"current angle {to_deg(angle + quadrant)}")
    return angle + quadrant

def calculate_tangent_for_vector(vector, vertex):
    '''calculate the angles that allow an object to lie flat on a shpere's surface'''    
    x, y, z = vector[0], vector[1], vector[2]
    radius = get_distance_between_points(vector, vertex)
    x_tan = calculate_tangent_angle(radius, calculate_axis_angle(z, y))
    y_tan = calculate_tangent_angle(radius, calculate_axis_angle(z, x))
    z_tan = calculate_tangent_angle(radius, calculate_axis_angle(x, y))
    return x_tan, y_tan, z_tan

def rotate_on_axis(starting_angular_position, rotation_angle, radius, clockwise_rotation = -1):
    start_1 = round(math.cos(starting_angular_position)*radius, 5)
    start_2 = round(math.sin(starting_angular_position)*radius, 5)
    new_1 = round(math.cos(starting_angular_position + rotation_angle*(clockwise_rotation))*radius, 5)
    new_2 = round(math.sin(starting_angular_position + rotation_angle*(clockwise_rotation))*radius, 5)
    change_1 = round(new_1 - start_1,5)
    change_2 = round(new_2 - start_2,5)
    # start_1 = math.cos(starting_angular_position)*radius
    # start_2 = math.sin(starting_angular_position)*radius
    # new_1 = math.cos(starting_angular_position + rotation_angle*(clockwise_rotation))*radius
    # new_2 = math.sin(starting_angular_position + rotation_angle*(clockwise_rotation))*radius
    # change_1 = new_1 - start_1
    # change_2 = new_2 - start_2
    return change_1, change_2


def process_axis_rotation(object_coord, vertex_coord, axis_no, angle, clockwise):
    if angle == 0:
        return object_coord
    rise = 0
    run = 0
    # rise is y and run is z for x axis rotation
    if axis_no == 0 :
        rise = 1 
        run = 2 
    # rise is x and run is z for y axis rotation
    if axis_no == 1 :
        rise = 0
        run = 2
    # rise is y and run is x for z axis rotation
    if axis_no == 2 :
        rise = 1
        run = 0
    rise_change = object_coord[rise] - vertex_coord[rise]
    print(f"rise change {rise_change}")
    run_change = object_coord[run] - vertex_coord[run]
    print(f"run change {run_change}")
    # run, rise
    run_after, rise_after = rotate_on_axis(calculate_axis_angle(run_change, rise_change), angle, math.hypot(run_change, rise_change), clockwise)
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
def vertex_rotation_new(angles = [0,0,0], vertex_location = [0,0,0], obj_coord = [0,0,0], clockwise = [-1,-1,-1]):
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 0, angles[0], clockwise[0])
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 1, angles[1], clockwise[1])
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 2, angles[2], clockwise[2])
    print(f'New Object coord {obj_coord}')
    return obj_coord

# z axis is fixed by the radius, therefore these are only x and y changes
# so we yust need to determine angle in the terms of x and y
# starting position is the position on the circle we begin with
# rotation around a single axis gives a 1 d circle
# rotation around two axis gives a fixed "diagonal" pattern (still a 2d trajectory even though it does travel through z)
# rotation around 3 axis give a "spherical" pattern where the diagonal pattern is not moved around to fill a 3d space
# angles in radians
def vertex_rotation(steps, angles = [0,0,0], vertex_location = [0,0,0], obj_coord = [0,0,0], clockwise = True, starting_position = math.pi/2):
    radius = get_distance_between_points(vertex_location, obj_coord)
    step_x = angles[0] / steps
    step_y = angles[1] / steps
    step_z = angles[2] / steps
    clockwise = -1 if clockwise else 1 
    step = step * clockwise 
    for x in range(steps):
        x, y, z = round(math.cos(starting_position-(step_x*x))*radius,2), round(math.sin(starting_position-(step_y*x))*radius,2), round(math.sin(starting_position-(step_z*x))*radius,2) 
        x, y, z = x*clockwise, y*clockwise, z*clockwise
        yield x, y, z 

# make the following assumptions when plotting rotations 
# for x axis rotations we perspective is from the -x looking forward to +z up and +y to the right
# for y axis rotations we perspective is from the -y looking forward to +z up and +y to the right
#  

# right handed orientation 
def calculate_change(ob, vertex, rotation=[0,0,0]):
    x_change = ob[0] - vertex[0]
    y_change = ob[1] - vertex[1]
    z_change = ob[2] - vertex[2]

    if rotation[0] != 0:
        h_sq = y_change ** 2 + z_change **2
        h = math.sqrt(h_sq)
        # right handed coordinates mean that x axis rotation is explained in z axis heigth
        starting_angle = math.atan(z_change / y_change)
        new_angle = starting_angle + rotation[0]
        p = points_on_circle(h, 1, starting_angle)
    c, s= round(math.cos(angle)*radius, 2), round(math.sin(angle)*radius, 2)
    c1 = c - radius
    c2 = s 
    return c1, c2 

def travel_around_circle_generator(points):
    for x in range(len(points)-1):
        yield (points[x+1][0] - points[x][0], points[x+1][1] - points[x][1])
    yield (points[-1][0] - points[0][0], points[-1][1] - points[0][1])


