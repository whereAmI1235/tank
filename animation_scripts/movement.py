import bpy
import math
# from circle import calculate_tangent_angle, points_on_circle

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
    selected_obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert('location', frame=0)
    obj.keyframe_insert('rotation_euler', index=1, frame=0)

# Get the active object (assuming it's the one you want to animate)
obj = bpy.context.active_object
init(obj)

class ObjMovement:
    def __init__(self, obj, current_frame):
        self.obj = obj
        self.frame = current_frame 
    def move(self, change_vector = [0,0,0], rotation_vector = [0,0,0], end_frame = 120):
        self.obj.location.x = self.obj.location.x + change_vector[0] 
        self.obj.location.y = self.obj.location.y + change_vector[1] 
        self.obj.location.z = self.obj.location.z + change_vector[2]
        self.obj.rotation_euler[0] = self.obj.rotation_euler[0] + math.radians(rotation_vector[0])
        self.obj.rotation_euler[1] = self.obj.rotation_euler[1] + math.radians(rotation_vector[1])
        self.obj.rotation_euler[2] = self.obj.rotation_euler[2] + math.radians(rotation_vector[2])
        # if rotation_vector[0] != 0: 
        #     self.obj.rotate_axis('X', math.radians(rotation_vector[0]))
        # elif rotation_vector[1] != 0: 
        #     self.obj.rotate_axis('Y', math.radians(rotation_vector[1]))
        # elif rotation_vector[2] != 0: 
        #     self.obj.rotate_axis('Z', math.radians(rotation_vector[2]))
        self.obj.keyframe_insert('location', frame = end_frame)
        self.obj.keyframe_insert('rotation_euler', frame = end_frame)
        self.frame = end_frame
    def rotation(self, points, frames_per_iteration = 10):
        self.frame = self.frame + frames_per_iteration 
        points = points_on_circle()
        for _ in po:
            self.move(change_vector=[.2,0,-.2], rotation_vector=[0, 45, 0], end_frame=self.frame)
    


# Set rotation mode for clarity
obj.rotation_mode = 'XYZ'
# Define animation start and end frames
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 120

omove = ObjMovement(obj, 0)
omove.move(change_vector=[5,5,5], rotation_vector=[0, 0, 0], end_frame=120)
# omove.smooth_rotation(5, 120)
# omove.move(change_vector=[.2,0,-.2], rotation_vector=[0, 45, 0], end_frame=150)
# omove.move(change_vector=[.2,0,-.2], rotation_vector=[0, 15, 0], end_frame=160)
# omove.move(change_vector=[.2,0,-.2], rotation_vector=[0, 15, 0], end_frame=170)
# omove.move(change_vector=[.2,0,-.2], rotation_vector=[0, 15, 0], end_frame=180)
# omove.move(change_vector=[.2,0,-.2], rotation_vector=[0, 15, 0], end_frame=190)
# omove.move(change_vector=[.2,0,-.2], rotation_vector=[0, 15, 0], end_frame=200)
# omove.move(change_vector=[0,0,0], rotation_vector=[0, 45, 0], end_frame=210)
# omove.move(change_vector=[-2,0,-1], rotation_vector=[0, 0, 0], end_frame=240)
print("Rotation animation created!")    