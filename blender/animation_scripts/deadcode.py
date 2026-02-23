
def points_on_circle(r,n=100, starting_angle = 0):
    # starting angle, the angle orientation to start generating points at. In radians
    # ex PI/2 would be at the top of the circle
    start_position = starting_angle if starting_angle != 0 else 2*PI
    step = (2*PI) / n
    print(start_position)
    return [(round(math.cos(start_position-(step*x))*r, 2),round(math.sin(start_position-(step*x))*r,2)) for x in range(n)]

def calculate_tangent_angle(radius, angle_rad, axis_name):
    print(f"calculate tangent angle for {to_deg(angle_rad)}")
    print(f"radius {radius}")
    # cut a triangle into the circle with base x and 
    # height y
    x = radius * math.cos(angle_rad)
    # y = radius * math.sin(angle_in_rad)
    # angle of triangle from the perimiter made when a vertical
    # line is drawn from x to the horizontal line going through 
    # the circle vertex (ie radius is the hypotenuse). Use arcsin to get angle
    delta = math.asin(x / radius)
    # subtract from the 90 degree angle required to for a tangent line for point 
    # x,y
    delta2 = RAD_90 - delta
    print(f"axis {axis_name} tangent angle {to_deg(delta2) * -1}")
    return delta2 * -1
    
    # tan_angle = RAD_180 - (RAD_90 + delta2)
    # print(f"tangent angle {to_deg(tan_angle) * -1}")
    # return tan_angle * -1

def calculate_tangent_for_vector(vector, vertex):
    ''' keep but not in use '''
    '''calculate the angles that allow an object to lie flat on a sphere's surface'''    
    x, y, z = vector[0], vector[1], vector[2]
    radius = get_distance_between_points(vector, vertex)
    if radius == 0:
        raise Exception("RadiusZeroError")
    print(f"radius {radius}")
    x_tan = calculate_tangent_angle(radius, calculate_axis_angle(z, y, 'x'), 'x')
    y_tan = calculate_tangent_angle(radius, calculate_axis_angle(z, x, 'y'), 'y')
    z_tan = calculate_tangent_angle(radius, calculate_axis_angle(x, y, 'z'), 'z')
    print(f"tanx {x_tan}")
    print(f"tany {y_tan}")
    print(f"tanz {z_tan}")
    return x_tan, y_tan, z_tan

def get_distance_between_points(vec1, vec2):
    x_change = vec2[0] - vec1[0]
    y_change = vec2[1] - vec1[1]
    z_change = vec2[2] - vec1[2]
    print(f"{x_change}")
    print(f"{y_change}")
    print(f"{z_change}")
    hypot = math.sqrt(x_change ** 2 + y_change ** 2)
    radius = math.sqrt(hypot ** 2 + z_change ** 2) 
    return radius