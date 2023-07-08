import sys
import math
if sys.version_info.major >= 3:
    from functools import reduce

import pymel.core as pm


class Vec3:

    def __init__(self, *args):
        if len(args) == 0:
            x = y = z = 0
        elif len(args) == 1:
            x = y = z = args[0]
        elif len(args) == 3:
            x, y, z = args
        else:
            raise Exception("Vec3 expects at most 3 dimension")
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __div__(self, other):
        return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)

    def __iadd__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __isub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __imul__(self, other):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __idiv__(self, other):
        return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)

    def __repr__(self):
        return "<Vec3 %f %f %f>" % (self.x, self.y, self.z)

    @staticmethod 
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def cross(a, b):
        return Vec3(
                a.y * b.z - a.z * b.y,
                a.z * b.x - a.x * b.z,
                a.x * b.y - a.y * b.x
                )

    @staticmethod
    def normalize(v):
        l = math.sqrt(Vec3.dot(v, v))
        if l == 0:
            return Vec3()
        return Vec3(v.x / l, v.y / l, v.z / l)

def get_verts(m):
    nverts = pm.polyEvaluate(m.longName(), v=True)
    verts = pm.xform(
            m.longName() + ".vtx[0:%d]" % nverts,
            q=True, t=True, ws=True)
    ret = []
    for i in range(nverts):
        v = Vec3(*verts[i*3:i*3+3])
        ret.append(v)
    return ret

def get_face_normals(m):
    nfaces = pm.polyEvaluate(m.longName(), f=True)
    return list(map(lambda item: Vec3(*map(lambda s: float(s),
                                           item.split(":")[-1]
                                           .strip()
                                           .split())),
                    pm.polyInfo(m.longName() + ".f[0:%d]" % nfaces, fn=True)))


def get_faces_using_edge(m, idx):
    name = m.longName() + ".e[%d]" % idx
    return list(map(lambda idx: int(idx),
                    pm.polyInfo(name, ef=True)[0]
                    .strip()
                    .split(":")[-1]
                    .split()))


def get_verts_using_face(m, idx):
    name = m.longName() + ".f[%d]" % idx
    return list(map(lambda item: int(item),
                    pm.polyInfo(name, fv=True)[0]
                    .strip()
                    .split(":")[-1]
                    .split()))

def get_verts_using_edge(m, idx):
    name = m.longName() + ".e[%d]" % idx
    return list(map(lambda item: int(item),
                    pm.polyInfo(name, ev=True)[0]
                    .strip()
                    .split(":")[-1]
                    .split()[:2]))

def is_poly_convex_hull(m, EPSILON=0.0001):
    nedges = pm.polyEvaluate(m.longName(), e=True)
    verts = get_verts(m)
    normals = get_face_normals(m)
    for idxe in range(nedges):
        faces = get_faces_using_edge(m, idxe)
        # Hole and Non-Manifest
        if len(faces) != 2:
            return False
        f1 = faces[0]
        f2 = faces[1]
        nf1 = Vec3.normalize(normals[f1])
        nf2 = Vec3.normalize(normals[f2])
        d = Vec3.dot(nf1, nf2)
        # Acute angle
        if d < -EPSILON:
            vf1 = get_verts_using_face(m, f1)
            vf2 = get_verts_using_face(m, f2)
            lvf1 = len(vf1)
            lvf2 = len(vf2)
            cf1 = reduce(lambda t, idx: t + verts[vf1[idx]], range(lvf1), Vec3()) / Vec3(lvf1)
            cf2 = reduce(lambda t, idx: t + verts[vf2[idx]], range(lvf2), Vec3()) / Vec3(lvf2)
            ve = get_verts_using_edge(m, idxe)
            lc = (verts[ve[0]] + verts[ve[1]]) / Vec3(2.0)
            cinner = Vec3.cross(nf1, nf2)
            coutter = Vec3.cross(Vec3.normalize(cf1 - lc), Vec3.normalize(cf2 - lc))
            r = Vec3.dot(cinner, coutter)
            if r > 0:
                return False
        # Obtuse angle
        elif d > EPSILON:
            ne = Vec3.normalize(nf1 + nf2)
            vf1 = get_verts_using_face(m, f1)
            vf2 = get_verts_using_face(m, f2)
            cf1 = Vec3()
            cf2 = Vec3()
            lvf1 = len(vf1)
            lvf2 = len(vf2)
            cf1 = reduce(lambda t, idx: t + verts[vf1[idx]], range(lvf1), Vec3()) / Vec3(lvf1)
            cf2 = reduce(lambda t, idx: t + verts[vf2[idx]], range(lvf2), Vec3()) / Vec3(lvf2)
            ve = get_verts_using_edge(m, idxe)
            lc = (verts[ve[0]] + verts[ve[1]]) / Vec3(2.0)
            if Vec3.dot(ne, Vec3.normalize(cf1 - lc)) > EPSILON:
                return False
    return True


for o in pm.ls(sl=True):
    if is_poly_convex_hull(o):
        print(o.shortName() + " is Convex Hull")
    else:
        print(o.shortName() + " is not Convex Hull")

