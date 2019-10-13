# https://www.opencascade.com/doc/occt-7.3.0/overview/html/occt_user_guides__visualization.html
# https://github.com/tpaviot/pythonocc-core/issues/608

import numpy as np
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_XY
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_NOC_BLACK

from OCC.Core.V3d import V3d_Plane, V3d_ColorScale
from OCC.Core.Visual3d import Visual3d_ContextView

from OCC.Core.MeshVS import MeshVS_Mesh, MeshVS_DataSource3D, MeshVS_NodalColorPrsBuilder
from OCC.Core.TColStd import TColStd_DataMapOfIntegerReal
from OCC.Core.Aspect import Aspect_SequenceOfColor
from OCC.Core.Quantity import Quantity_NOC_RED, Quantity_NOC_BLUE1, Quantity_NOC_BLACK
from OCC.Core.Quantity import Quantity_Color
"""
// assign nodal builder to the mesh
Handle(MeshVS_NodalColorPrsBuilder) aBuilder = new MeshVS_NodalColorPrsBuilder (theMeshPrs, MeshVS_DMF_NodalColorDataPrs | MeshVS_DMF_OCCMask);
aBuilder->UseTexture (true);
// prepare color map
Aspect_SequenceOfColor aColorMap;
aColorMap.Append (Quantity_NOC_RED);
aColorMap.Append (Quantity_NOC_BLUE1);
// assign color scale map  values (0..1) to nodes
TColStd_DataMapOfIntegerReal aScaleMap;
...
// iterate through the  nodes and add an node id and an appropriate value to the map
aScaleMap.Bind (anId, aValue);
// pass color map and color scale values to the builder
aBuilder->SetColorMap (aColorMap);
aBuilder->SetInvalidColor (Quantity_NOC_BLACK);
aBuilder->SetTextureCoords (aScaleMap);
aMesh->AddBuilder (aBuilder, true);
"""


# from matplotlib import (_path, artist, cbook, cm, colors as mcolors, docstring,
#                        lines as mlines, path as mpath, transforms)
#from matplotlib.collections import Collection

display, start_display, add_menu, add_function_to_menu = init_display()

myBox = BRepPrimAPI_MakeBox(60, 60, 50).Shape()

view = display.View
colorscale = view.ColorScale()

aMesh = MeshVS_Mesh()

builder = MeshVS_NodalColorPrsBuilder(aMesh)

a_cm = Aspect_SequenceOfColor()
a_cm.Append(Quantity_Color())
#a_cm.Append(Quantity_NOC_BLUE1)

a_cl = TColStd_DataMapOfIntegerReal(10)
for i in range(10 + 1):
    a_cl.Bind(i + 1, i)

builder.SetColorMap(a_cm)
builder.SetTextureCoords(a_cl)
#builder.SetInvalidColor(Quantity_NOC_BLACK)
aMesh.AddBuilder(builder, True)

aMinRange = colorscale.GetMin()
aMaxRange = colorscale.GetMax()
aNbIntervals = colorscale.GetNumberOfIntervals()
aTextHeight = colorscale.GetTextHeight()
labPosition = colorscale.GetLabelPosition()
position = gp_XY(colorscale.GetXPosition(), colorscale.GetYPosition())
title = colorscale.GetTitle()

view.ColorScaleDisplay()
display.DisplayShape(myBox)
start_display()
