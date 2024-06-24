import bpy
import bmesh

def set_object_mode():
  """
  オブジェクトモードに移行する
  """
  bpy.ops.object.mode_set(mode='OBJECT')


def get_context(context: bpy.types.Context | None = None) -> bpy.types.Context:
  """
  context が None の場合は bpy.context を返す.
  context が None でない場合はそのまま contextを返す
  """
  if context:
    return context
  return bpy.context

class BMode:
  """
  Blender の Mode を保持する。
  reset で元に戻すことが出来る
  """

  _obj: list[bpy.types.Object]
  _mode: str

  def __init__(self, context: bpy.types.Context | None = None) -> None:
    context = get_context(context)
    self._mode = context.mode
    self._obj = [obj for obj in context.selected_objects]

  def is_edit_mesh(self) -> bool:
    return self._mode == 'EDIT_MESH'

  def is_object(self)->bool:
    return self._mode == 'OBJECT'

  def is_sculpt(self) -> bool:
      return self._mode == 'SCULPT'

  def is_vertex_paint(self) -> bool:
      return self._mode == 'VERTEX_PAINT'

  def is_weight_paint(self) -> bool:
      return self._mode == 'WEIGHT_PAINT'

  def is_texture_paint(self) -> bool:
      return self._mode == 'TEXTURE_PAINT'

  def reset(self):
    if self.is_edit_mesh():
      bpy.ops.object.mode_set(mode='OBJECT')
      for obj in self._obj:
        obj.select_set(True)
      bpy.context.view_layer.objects.active = self._obj[0]
      bpy.ops.object.mode_set(mode='EDIT')
    else:
      bpy.ops.object.mode_set(mode=self._mode)


def get_obj(context: bpy.types.Context | None = None):
  """
  bpy.context.active_object のショートカット
  """
  return get_context(context).active_object

def get_edit_obj(obj: bpy.types.Object | None = None, context: bpy.types.Context | None = None):
  """"
  obj が None の場合は編集中のオブジェクトを取得する.
  obj が None でない場合は、オブジェクトが編集中の場合のみ obj を返す
  編集中のオブジェクトが見つからない場合は None
  """
  if obj is None:
    return get_context(context).edit_object
  if obj.mode == 'EDIT':
    return obj

  return None

def is_mesh_obj(obj: bpy.types.Object | None):
  """
  obj.type が MESH かどうか
  """
  return obj is not None and obj.type == 'MESH'

def get_mesh(obj: bpy.types.Object | None = None) -> bpy.types.Mesh | None :
  """
  Mesh を返す
  """
  if obj is None or obj.type != 'MESH':
    return None
  return obj.data

def get_edit_bmesh(obj: bpy.types.Object | None, context: bpy.types.Context | None = None):
  """
  メッシュ編集中の Object から bmesh を取得する
  """
  obj = get_edit_obj(obj, context)
  if obj is None or not is_mesh_obj(obj):
    return None
  return bmesh.from_edit_mesh(obj.data)

def get_bmesh(obj: bpy.types.Object | None, context: bpy.types.Context | None = None):
  """
  Object から bmesh を取得する
  """
  if not obj or not is_mesh_obj(obj):
    return None
  eobj = get_edit_obj(obj, context)
  if eobj:
    return get_edit_bmesh(eobj, context)
  bm = bmesh.new()
  bm.from_mesh(obj.data)
  return bm

def get_selected_faces(faces: bmesh.types.BMFaceSeq):
  """
  選択された面を取得
  """
  return [f for f in faces if f.select]

def get_selected_verts(verts: bmesh.types.BMVertSeq):
  """
  選択された頂点を取得
  """
  return [v for v in verts if v.select]

def is_triangle(face: bmesh.types.BMFace):
  """
  面が三角形かどうか
  """
  return len(face.verts) == 3

def print_vert(v: bmesh.types.BMVert):
  """
  頂点座標をprint
  """
  co = v.co
  x, y, z = co.x, co.y, co.z
  print(f"Vert({x},{y},{z})")
