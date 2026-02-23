import bpy
import math
import sys
import mathutils
import os

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
    return mathutils.Vector((i_list[0], i_list[1], i_list[2]))

def init(selected_obj):
    # clear animations and reset object or origin
    # Iterate through all objects in the current scene
    for obj in bpy.context.scene.objects:
        # Check if the object has animation data
        if obj.animation_data:
            # Clear the animation data for the object
            obj.animation_data_clear()
    selected_obj.location.x = 0
    selected_obj.location.y = 0
    selected_obj.location.z = 0
    selected_obj.rotation_euler = (math.pi/2, 0, 0)
    # selected_obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert('location', frame=0)
    obj.keyframe_insert('rotation_euler', index=1, frame=0)


# Get the active object (assuming it's the one you want to animate)
obj = bpy.context.active_object
init(obj)


class ObjMovement:
    def __init__(self, obj, current_frame):
        self.obj = obj
        self.frame = current_frame
        self.frames = []

    def move(self, change_vector=[0, 0, 0], rotation_vector=[0, 0, 0], end_frame=120, clockwise = -1):
        self.obj.location.x = self.obj.location.x + change_vector[0]
        self.obj.location.y = self.obj.location.y + change_vector[1]
        self.obj.location.z = self.obj.location.z + change_vector[2]
        print(f"Moving to {self.obj.location.x} {self.obj.location.y} {self.obj.location.z}")
        print(f"Rotating {rotation_vector[0]} {rotation_vector[1]} {rotation_vector[2]}")
        self.obj.rotation_euler[0] = self.obj.rotation_euler[0] + \
            rotation_vector[0] * clockwise
        self.obj.rotation_euler[1] = self.obj.rotation_euler[1] + \
            rotation_vector[1] * clockwise
        self.obj.rotation_euler[2] = self.obj.rotation_euler[2] + \
            rotation_vector[2] * clockwise
        self.obj.keyframe_insert('location', frame=end_frame)
        self.obj.keyframe_insert('rotation_euler', frame=end_frame)
        self.frame = end_frame

    def rotation(self, iterations, angles=mathutils.Vector((0,0,math.pi/4)), frames_per_iteration=20):
        for x in range(iterations):
            self.frame = self.frame + frames_per_iteration
            new = circle.vertex_rotation(angles, obj_coord=self.obj.location)
            new_v = vector_from_list(new)
            diff_v = new_v - self.obj.location
            self.move(diff_v, end_frame = self.frame)

    def orbit(self, iterations=8, angles=mathutils.Vector((0,0,math.pi/4)), frames_per_iteration=20, vertex = [0,0,0]):
        ''' just like rotation but with object orientation rotation about a vertex'''
        for x in range(iterations):
            self.frame = self.frame + frames_per_iteration
            new = circle.vertex_rotation(angles, obj_coord=self.obj.location)
            new_v = vector_from_list(new)
            diff_v = new_v - self.obj.location
            print(f"Difference vector {diff_v}")
            self.move(diff_v, angles, end_frame = self.frame)

# Set rotation mode for clarity
obj.rotation_mode = 'XYZ'
# Define animation start and end frames
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 120  

omove = ObjMovement(obj, 0)
# omove.move(change_vector=[5, 5, 5], rotation_vector=[0, 0, 0], end_frame=120)
omove.move(change_vector=[0, 1, 0], rotation_vector=[0, 0, 0], end_frame=20)
# omove.rotation(8, angles=mathutils.Vector((0,0,math.pi/4)))
omove.orbit(frames_per_iteration=10)
print("Rotation animation created!\n")
