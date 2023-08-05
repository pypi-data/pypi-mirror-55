"""
graphicsHelper.py

Functions to help build graphics data
"""

import igeCore as core
import igeVmath as vmath

def createSprite(width:float=100, height:float=100, texture=None, uv_left_top:tuple=(0,0), uv_right_bottom:tuple=(1,1), normal=None):
    """
    Create Visible Rectangle

	Parameters
	----------
        width : float (optional)
            sprite width
        height: float (optional)
            sprite height
        texture: string (optional)
            texture file name
        uv_left_top: tuple (optional)
            texture uv value of left top cornar
        uv_right_bottom: tuple (optional)
            texture uv value of right bottom cornar
        normal: pyvmath.vec3 (optional)
            specify rectangle's nomal vector
	Returns
	-------
        editableFigure
    """
    w = width/2
    h = height/2
    points = ((-w,h,0.0), (w,h,0.0), (-w,-h,0.0), (w,-h,0.0))
    uvs = (0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0)
    tris = (0, 2, 1, 1, 2, 3)

    if normal is not None:
        newpoints = []
        nom0 = (0, 0, 1)
        mat = vmath.mat33(vmath.quat_rotation(nom0, normal))
        for p in points:
            newpoints.append(mat * p)
        points = newpoints

    return createMesh(points, tris, texture, uvs)


def createMesh(points, tris, texture=None, uvs = None):
    """
    Create a polygon mesh by specifying vertex coordinates and triangle index

	Parameters
	----------
        points: tuple or list
            list or tuple of points
        tris: tuple or list
            list or tuple of triangle indices
        texture: string (optional)
            file path of texture
        uvs: list or tuple (optional)
            list or tuple of  texture uv
	Returns
	-------
        editableFigure
   
    """
    gen = core.shaderGenerator()
    if texture != None:
        gen.setColorTexture(True)
    gen.setBoneCondition(1, 1)

    efig = core.editableFigure("sprite")
    efig.addMaterial("mate", gen)
    efig.addMesh("mesh", "mate");

    efig.setVertexElements("mesh", core.ATTRIBUTE_ID_POSITION, points)
    if uvs:
        efig.setVertexElements("mesh", core.ATTRIBUTE_ID_UV0,uvs)
    efig.setTriangles("mesh", tris);
    efig.addJoint("joint");
    efig.setMaterialParam("mate", "DiffuseColor", (1.0, 1.0, 1.0, 1.0));
    #efig.setMaterialRenderState("mate", "cull_face_enable", False)

    if texture != None:
        efig.setMaterialParamTexture("mate", "ColorSampler", texture,
                                     wrap_s=core.SAMPLERSTATE_BORDER,wrap_t=core.SAMPLERSTATE_BORDER,
                                     minfilter=core.SAMPLERSTATE_NEAREST, magfilter=core.SAMPLERSTATE_NEAREST)
        efig.setMaterialRenderState("mate", "blend_enable", True)
    return efig
