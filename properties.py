import bpy

def update_RBsize(self,context):
    for obj in context.selected_objects:
        obj.mmd_rigid.size = obj.mmd_rigid.size + self.Coe

def props():
    bpy.types.Scene.Coe = bpy.props.FloatVectorProperty(
        name="size",
        subtype="XYZ",
        default=[0,0,0],
        update = update_RBsize
        )