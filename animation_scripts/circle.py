import math
import sys

def to_deg(rad):
    return rad * (180/math.pi)

def to_rad(deg):
    return deg * math.pi / 180 

RAD_90 = to_rad(90)
RAD_180 = to_rad(180)
PI = math.pi

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

def rotate_on_axis(starting_angular_position, rotation_angle, distance_from_axis, clockwise_rotation = -1):
    start_1 = round(math.cos(starting_angular_position)*distance_from_axis, 2)
    start_2 = round(math.sin(starting_angular_position)*distance_from_axis, 2)
    new_1 = round(math.cos(starting_angular_position + rotation_angle*(clockwise_rotation))*distance_from_axis, 5)
    new_2 = round(math.sin(starting_angular_position + rotation_angle*(clockwise_rotation))*distance_from_axis, 5)
    change_1 = round(new_1 - start_1,5)
    change_2 = round(new_2 - start_2,5)
    return change_1, change_2

def calculate_axis_angle(run, rise):
    if rise == 0 and run == 0:
        return 0
    ''' take arctan of rise over run (opposite over adjacent) to get angle '''
    if rise > 0 and run > 0 or (rise == 0 and run > 0):
        quadrant = 0
    if rise > 0 and run < 0 or (rise > 0 and run == 0):
        quadrant = PI/2
    if rise < 0 and run < 0 or (rise == 0 and run < 0):
        quadrant = PI
    if rise < 0 and run > 0 or (rise < 0 and run == 0):
        quadrant = PI* 3/2 
    new = abs(math.atan(rise/run)) if run != 0 else 0 
    return new + quadrant

def process_axis_rotation(object_coord, vertex_coord, axis_no, angle, clockwise):
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
    run_change = object_coord[run] - vertex_coord[run]
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
def vertex_rotation_new(steps, angles = [0,0,0], vertex_location = [0,0,0], obj_coord = [0,0,0], clockwise = [-1,-1,-1]):
    print(obj_coord)
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 0, angles[0], clockwise[0])
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 1, angles[1], clockwise[1])
    obj_coord = process_axis_rotation(obj_coord, vertex_location, 2, angles[2], clockwise[2])
    print(obj_coord)

# z axis is fixed by the radius, therefore these are only x and y changes
# so we yust need to determine angle in the terms of x and y
# starting position is the position on the circle we begin with
# rotation around a single axis gives a 1 d circle
# rotation around two axis gives a fixed "diagonal" pattern (still a 2d trajectory even though it does travel through z)
# rotation around 3 axis give a "spherical" pattern where the diagonal pattern is not moved around to fill a 3d space
# angles in radians
def vertex_rotation(steps, angles = [0,0,0], vertex_location = [0,0,0], obj_coord = [0,0,0], clockwise = True, starting_position = math.pi/2):
    x_change = obj_coord[0] - vertex_location[0]
    y_change = obj_coord[1] - vertex_location[1]
    z_change = obj_coord[2] - vertex_location[2]
    hypot = math.sqrt(x_change ** 2 + y_change ** 2)
    radius = math.sqrt(hypot ** 2 + z_change ** 2) 
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



# r = 1.0
# y = math.sqrt(.5)
# y = .9
# x = math.sqrt(r ** 2 - y ** 9)
# tan_angle = calculate_tangent_angle(1, float(sys.argv[1]))
# print(f"tangent angle {to_deg(tan_angle)}")

# alpha = to_deg(math.asin(y/r)) 
# beta = 180 - (90 + alpha)
# hypot = r / math.sin(to_rad(beta))
# z = hypot - x
# c = math.sqrt(z **2 + y **2)
# delta = to_deg(math.asin(z/c))
# psi = 180 - (delta + 90)
# print(f"alpha {alpha}")
# print(f"x {x}")
# print(f"beta {beta}")
# print(f"hypot {hypot}")
# print(f"z {z}")
# print(f"delta {delta}")
# print(f"psi {psi}")