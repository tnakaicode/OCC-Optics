# http://ruggero.sci.yokohama-cu.ac.jp
# http://ruggero.sci.yokohama-cu.ac.jp/data/pgGraphexample_3D.py

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl

### something to graph ######
pi = 3.1415
X = np.linspace(-10, 10, 100)
Y1 = 2 + np.sin(X)
Y2 = -2 + Y1 * Y1
Y3 = np.cos(1 * Y1) / (X + 0.0131415)
Y4 = 4 + np.sin(X) * np.cos(2 * X)
Z = np.exp(-0.1 * X * X) * np.cos(0.3 *
                                  (X.reshape(100, 1)**2 + X.reshape(1, 100)**2))
#############################
# you need this call ONCE
app = pg.QtGui.QApplication([])
#############################

##### plot 3D surface data  ####
w = gl.GLViewWidget()
# Saddle example with x and y specified
p = gl.GLSurfacePlotItem(x=X, y=X, z=Z, shader='heightColor', facecolors=Z)
w.addItem(p)
# show
w.show()
pg.QtGui.QApplication.exec_()
