import bpy
import math
import sys
import mathutils

# current_path = bpy.data.filepath
# current_path = '/'.join(current_path.split('/')[:-1])
# print(f"current path {current_path}/animation_scripts/")
# sys.path.append(f'{current_path}/animation_scripts/')
# windows

# when loaded into blender this file is put into a different place. Need to provide full path 
anim_scripts_path = "C:\\Users\\Andrew Roffee\\gitRepos\\proj-3d\\proj-3d\\blender\\animation_scripts"
sys.path.append(anim_scripts_path)
import circle

def vector_from_list(i_list):
    return mathutils.Vector([x for x in i_list])

def init(selected_obj):
    # clear animations and reset object or origin
    # Iterate through all objects in the current scene
    for obj in bpy.context.scene.objects:
        # Check if the object has animation data
        if obj.animation_data:
            # Clear the animation data for the object
            obj.animation_data_clear()
        obj.keyframe_insert('location', frame=0)
        obj.keyframe_insert('rotation_euler', index=0, frame=0)
        obj.rotation_mode = 'XYZ'
    selected_obj.location.x = 0
    selected_obj.location.y = 0
    selected_obj.location.z = 0
    selected_obj.rotation_euler = (0, 0, 0)
    # make it flat, probably no necessary for all
    selected_obj.rotation_euler = (math.pi/2, 0, 0)
    # Set rotation mode for clarity
    selected_obj.keyframe_insert('location', frame=0)
    selected_obj.keyframe_insert('rotation_euler', index=0, frame=0)
    selected_obj.rotation_mode = 'XYZ'


# Get the active object (assuming it's the one you want to animate)
obj = bpy.context.active_object
init(obj)
def to_deg(rad):
    return rad * (180/math.pi)

def to_rad(deg):
    return deg * math.pi / 180 

class ObjMovement:
    def __init__(self, obj, current_frame, start_location = None, starting_rotation = None):
        self.obj = obj
        self.frame = current_frame
        self.obj.rotation_mode = 'XYZ'
        if start_location:
            self.obj.location = start_location
            self.obj.keyframe_insert('location', frame=self.frame)
        if starting_rotation:
            self.obj.rotation_euler[0] = starting_rotation[0]
            self.obj.rotation_euler[1] = starting_rotation[1]
            self.obj.rotation_euler[2] = starting_rotation[2]
            self.obj.keyframe_insert('rotation_euler', frame=self.frame)


    def apply_location(self, vec):
        self.obj.location = vec
        self.obj.keyframe_insert('location', frame=self.frame)

    def apply_rotation(self, vec, clockwise = -1, tangent=False):
        self.obj.rotation_euler[0] = self.obj.rotation_euler[0] + \
            vec[0] * clockwise
        self.obj.rotation_euler[1] = self.obj.rotation_euler[1] + \
            vec[1] * clockwise
        self.obj.rotation_euler[2] = self.obj.rotation_euler[2] + \
            vec[2] * clockwise
        self.obj.keyframe_insert('rotation_euler', frame=self.frame)
    
    def move(self, change_vector=[0, 0, 0], rotation_vector=[0, 0, 0], clockwise = -1, more_frames = 0):
        self.frame = self.frame + more_frames
        self.obj.location.x = self.obj.location.x + change_vector[0]
        self.obj.location.y = self.obj.location.y + change_vector[1]
        self.obj.location.z = self.obj.location.z + change_vector[2]
        print(f"Moving to {self.obj.location.x} {self.obj.location.y} {self.obj.location.z}")
        if rotation_vector != [0,0,0]:
            s = "Rotating to " 
            if rotation_vector[0] != -1:
                self.obj.rotation_euler[0] = rotation_vector[0] 
                s += f" x {to_deg(rotation_vector[0])}"
            if rotation_vector[1] != -1:
                self.obj.rotation_euler[1] = rotation_vector[1] 
                s += f" y {to_deg(rotation_vector[1])}"
            if rotation_vector[2] != -1:
                self.obj.rotation_euler[2] = rotation_vector[2]
                s += f" z {to_deg(rotation_vector[2])}"
            print(s)
            # self.obj.rotation_euler[0] = self.obj.rotation_euler[0] + \
            #     rotation_vector[0] * clockwise
            # self.obj.rotation_euler[1] = self.obj.rotation_euler[1] + \
            #     rotation_vector[1] * clockwise
            # self.obj.rotation_euler[2] = self.obj.rotation_euler[2] + \
            #     rotation_vector[2] * clockwise
        self.obj.keyframe_insert('location', frame=self.frame)
        self.obj.keyframe_insert('rotation_euler', frame=self.frame)

    def rotation_about_point(self, iterations, angles=mathutils.Vector((0,0,math.pi/4)), frames_per_iteration=20, vertex = [0,0,0]):
        for _ in range(iterations):
            new = circle.vertex_rotation(angles, obj_coord=self.obj.location, vertex_location=vertex)
            new_v = vector_from_list(new)
            diff_v = new_v - self.obj.location
            self.move(diff_v, more_frames = frames_per_iteration)

    def orbit(self, iterations=8, angles=mathutils.Vector((0,0,math.pi/4)), frames_per_iteration=20, vertex = [0,0,0]):
        ''' just like rotation but with object orientation rotation about a vertex'''
        for _ in range(iterations):
            self.frame = self.frame + frames_per_iteration
            new = circle.vertex_rotation(angles, obj_coord=self.obj.location, vertex_location=vertex)
            new_v = vector_from_list(new)
            self.apply_location(new_v)
            self.apply_rotation(angles)
            # self.move(new_v, angles, more_frames = frames_per_iteration)

    def find_tangent_from_vertex(self, next_pos = None, vertex=[0,0,0], clockwise = -1):
        '''finds the tangent angles for each plane to be perpandicular from a vertex'''  
        if next_pos != None:
            angle_per_axis = circle.find_per_plane_axis_angle(next_pos, vertex)
        else:
            angle_per_axis = circle.find_per_plane_axis_angle(self.obj.location, vertex)
        tan_angles = [find_rotation_tangent_angle(angle_per_axis[0], clockwise), find_rotation_tangent_angle(angle_per_axis[1], clockwise), find_rotation_tangent_angle(angle_per_axis[2], clockwise)]
        print(f"tangent angles are {','.join([str(x) for x in tan_angles])}")
        print(f"tangent angles are {','.join([str(to_deg(x)) for x in tan_angles])}")
        return tan_angles

# the tangent to any angle is +90 degrees. If you want clockwise rotation of the asset leave as is,
# otherwaise change clockwise to 1
def find_rotation_tangent_angle(angle, clockwise=-1):
    if angle:
        return angle + (math.pi/2 * clockwise)

# Define animation start and end frames
scene = bpy.context.scene
scene.frame_start = 0

omove = ObjMovement(obj, 0, mathutils.Vector((0,0,0)), [math.pi/2,0,0])
# omove.move(change_vector=[5, 5, 5], rotation_vector=[0, 0, 0], end_frame=120)



# omove.move(change_vector=[4, 1, 0], rotation_vector=[-1, -1, to_rad(find_rotation_tangent_angle(14))], more_frames=40)
omove.move(change_vector=[0, 1, 0], rotation_vector=[0, 0, 0], more_frames=10)
tans = omove.find_tangent_from_vertex(next_pos=[4,1,0]) 
omove.move(change_vector=[4, 0, 0], rotation_vector=[-1, -1, tans[2]], more_frames=40)
# omove.move(change_vector=[4, 0, 0], rotation_vector=[-1, -1, to_rad(find_rotation_tangent_angle(14))], more_frames=40)
# omove.move(change_vector=[1, 0, 0], rotation_vector=[0, 0, 0], more_frames=10)
# omove.move(change_vector=[1, 0, 0], rotation_vector=[0, 0, 0], more_frames=10)
# omove.move(change_vector=[1, 0, 0], rotation_vector=[0, 0, 0], more_frames=10)
omove.orbit(iterations = 12, angles=mathutils.Vector((0,0, math.pi/6)), frames_per_iteration=20)
# omove.orbit(frames_per_iteration=20)
scene.frame_end = omove.frame + 40 
print("Rotation animation created!\n") 
