import bpy

# Get the active object
obj = bpy.context.active_object

obj.rotation_mode = 'XYZ'

# Define animation start and end frames
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 100

obj.keyframe_insert('location', index=1, frame=scene.frame_start)
# Translate along the X-axis
obj.location.x = obj.location.x + 5
obj.keyframe_insert('location', index=1, frame=scene.frame_end)
