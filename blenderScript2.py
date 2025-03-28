import bpy
def get_location(frame):
    scene=bpy.context.scene
    scene.frame_set(frame)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj=bpy.data.objects['8_of_Clubs'].evaluated_get(depsgraph)
    current_location=obj.matrix_world.translation.z
    return current_location
print(get_location(0))
print(get_location(10))
print(get_location(100))
