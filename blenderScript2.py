import bpy
for x in range(0,101):
    scene=bpy.context.scene
    scene.frame_set(x)
def get_location(frame):
    scene=bpy.context.scene
    scene.frame_set(frame)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj=bpy.data.objects['8_of_Spades'].evaluated_get(depsgraph)
    current_location=obj.matrix_world.translation.z
    return current_location
f=open('result.txt', 'w')
f.write(str(get_location(100)))
f.close()