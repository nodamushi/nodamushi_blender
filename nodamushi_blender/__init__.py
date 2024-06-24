import bpy
from . import operator as op

#
# bl_info
# https://developer.blender.org/docs/handbook/addons/addon_meta_info/
#
bl_info = {
    "name" : "Nodamushi Blender Addon",
    "author" : "nodamushi",
    "description" : "For me",
    "blender" : (4, 1, 0),
    "version" : (0, 1),
    "category" : "Object"
}

##################################################
##################################################
# Add classes
#   Operator: bpy.types.Operator, OP, https://docs.blender.org/api/current/bpy.types.Operator.html
#   Panel: bpy.types.Panel, PT, https://docs.blender.org/api/current/bpy.types.Panel.html
#
classes = []
##################################################

class NODAMUSHI_OP_MirrorX(bpy.types.Operator):
  bl_idname = "nodamushi.mirrorx"
  bl_label = "Mirror X"
  bl_description = "Select two vertices. Make their vertex coordinates the x-axis target."

  def execute(self, context: bpy.types.Context):
    ret = op.mirror(True, False, False)
    ret.report(self)
    return ret.get()
classes.append(NODAMUSHI_OP_MirrorX)

class NODAMUSHI_OP_MirrorY(bpy.types.Operator):
  bl_idname = "nodamushi.mirrory"
  bl_label = "Mirror Y"
  bl_description = "Select two vertices. Make their vertex coordinates the x-axis target."

  def execute(self, context: bpy.types.Context):
    ret = op.mirror(False, True, False)
    ret.report(self)
    return ret.get()

classes.append(NODAMUSHI_OP_MirrorY)

class NODAMUSHI_OP_MirrorZ(bpy.types.Operator):
  bl_idname = "nodamushi.mirrorz"
  bl_label = "Mirror Z"
  bl_description = "Select two vertices. Make their vertex coordinates the x-axis target."

  def execute(self, context: bpy.types.Context):
    ret = op.mirror(False, False, True)
    ret.report(self)
    return ret.get()

classes.append(NODAMUSHI_OP_MirrorZ)

class NODAMUSHI_OP_Tri2seq(bpy.types.Operator):
  bl_idname = "nodamushi.tri2seq"
  bl_label = "△→□"
  bl_description = ""

  def execute(self, context: bpy.types.Context):
    ret = op.tri_to_seq()
    ret.report(self)
    return ret.get()
classes.append(NODAMUSHI_OP_Tri2seq)

class NODAMUSHI_PT_Hello(bpy.types.Panel):
  bl_label = "Nodamushi"
  # https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items
  bl_space_type = "VIEW_3D"
  # https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#rna-enum-region-type-items
  bl_region_type = "UI" # UI はサイドバーのこと
  bl_category = "Edit" # Edit(編集) に追加

  def draw(self, context: bpy.types.Context):
    # Operator を実行するボタンは layout.operator から簡単に登録可能
    self.layout.operator(NODAMUSHI_OP_MirrorX.bl_idname)
    self.layout.operator(NODAMUSHI_OP_MirrorY.bl_idname)
    self.layout.operator(NODAMUSHI_OP_MirrorZ.bl_idname)
    self.layout.operator(NODAMUSHI_OP_Tri2seq.bl_idname)

classes.append(NODAMUSHI_PT_Hello)
################# Don't touch #####################
def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
###################################################
