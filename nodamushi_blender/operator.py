from .util import *
from . import result

################################
# Mirror Operator X, Y, Z
################################
def mirror(xMirror: bool, yMirror: bool, zMirror: bool) -> result.Result:
  def value(v: float, mirror: bool):
    if mirror:
      return -v
    else:
      return v

  obj = get_edit_obj()
  if not is_mesh_obj(obj):
    return result.error("Must be call Mesh Mode")
  bm = get_bmesh(obj)
  if bm is None:
    return result.error("Not MESH object")
  verts = get_selected_verts(bm.verts)
  if len(verts) != 2:
    return result.error("Select two vertices")

  v1 = verts[1]
  v = verts[0].co
  v1.co.x = value(v.x, xMirror)
  v1.co.y = value(v.y, yMirror)
  v1.co.z = value(v.z, zMirror)


  bm.normal_update()
  bmesh.update_edit_mesh(obj.data)
  bm.free()

  return result.ok()

################################
# △→□
################################

def has_linked_non_tri_face(v: bmesh.types.BMVert, current_face: bmesh.types.BMFace):
  """
  頂点 v が接続している非三角メッシュがあるかどうか
  (※ ただし current_face は検索対象から除く)
  """
  cnt = 0
  for f in v.link_faces:
    if f != current_face and not is_triangle(f):
      cnt += 1
  return cnt == 0

class UpdateTriangle:
  bm: bmesh.types.BMesh
  face: bmesh.types.BMFace
  vert: bmesh.types.BMVert
  edge: bmesh.types.BMEdge
  vert_idx: list[int]
  ok: bool

  def __init__(self, bm: bmesh.types.BMesh, face: bmesh.types.BMFace, vert: bmesh.types.BMVert):
    self.bm = bm
    self.face = face
    self.vert = vert
    self.ok = False

    verts = self.face.verts
    # 最初に対象頂点がある三角ポリゴンの配列 idx
    if verts[0] == vert:
      idx = [0, 1, 2]
    elif verts[1] == vert:
      idx = [1, 2, 0]
    elif verts[2] == vert:
      idx = [2, 0, 1]

    # 削除するエッジの検索
    edge = None
    for e in face.edges:
      if len(e.verts) != 2:
        return
      [v0, v1] = e.verts
      if (v0 == vert or v1 == vert) and len(e.link_faces) == 1:
        edge = e
        break
    if not edge:
      return
    self.edge = edge
    # 削除するエッジと、対象頂点から、新規頂点(-1)の追加位置を決定
    v = e.verts[0]
    if v == vert:
      v = e.verts[1]
    if v == verts[idx[1]]:
      idx.insert(1, -1)
    else:
      idx.append(-1)

    self.vert_idx = idx
    self.ok = True


  def get_vert_idx(self, v: bmesh.types.BMFace):
    verts = self.face.verts
    if verts[0] == v:
      return 0
    elif verts[1] == v:
      return 1
    elif verts[2] == v:
      return 2
    return -1


  def update(self):
    bm = self.bm
    face = self.face
    verts = face.verts
    vert_idx = self.vert_idx

    # store old face material
    mt = face.material_index
    # store old loops
    _loops = [l for l in face.loops]
    loops = []

    # new vert
    new_vert = bm.verts.new(self.vert.co)
    # vert array to create new face
    new_verts = []
    for idx in vert_idx:
      if idx == -1:
        new_verts.append(new_vert)
        loops.append(_loops[vert_idx[0]])
      else:
        new_verts.append(verts[idx])
        loops.append(_loops[idx])


    # add new face
    new_face = bm.faces.new(new_verts)
    new_face.select_set(True)

    # set material
    new_face.material_index = mt

    # set loop
    for idx, loop in enumerate(new_face.loops):
      loop.copy_from(loops[idx])

    # remove old triangle face and edge
    bm.faces.remove(face)
    bm.edges.remove(self.edge)


def add_update_triangle(
  bm: bmesh.types.BMesh,
  face: bmesh.types.BMFace,
  out: list[UpdateTriangle]):
  """
  更新すべき三角メッシュである場合は、outにUpdateTriangleを追加
  """
  verts = [v for v in face.verts if has_linked_non_tri_face(v, face)]
  if len(verts) == 1:
    out.append(UpdateTriangle(bm, face, verts[0]))

def tri_to_seq() -> result.Result:
  """
  三角メッシュの先端を増やして四角メッシュにする
  編集モードでなくてはならない
  """
  mode = BMode()
  if not mode.is_edit_mesh():
    return result.error("Not mesh edit mode")

  obj = get_edit_obj()
  mesh = get_mesh(obj)

  if mesh is None:
    return result.error("Not MESH object")

  bm = get_edit_bmesh(obj)
  faces = bm.faces
  selected_faces = get_selected_faces(faces)

  if len(selected_faces) == 0:
    return result.ok("No slected face.")

  selected_triangles = [f for f in selected_faces if is_triangle(f)]

  update_triangles: list[UpdateTriangle] = []
  for f in selected_triangles:
    add_update_triangle(bm, f, update_triangles)

  if len(update_triangles) == 0:
    return result.ok("No triangular mesh was found at the tip.")

  for ut in update_triangles:
    ut.update()

  bmesh.update_edit_mesh(mesh)
  mode.reset()

  return result.ok(f"The triangular mesh at the {len(update_triangles)} tips has been replaced by a square mesh.")

