import numpy as np
import matplotlib.pyplot as plt
import numdifftools as nd
from scipy.integrate import odeint
from mpl_toolkits.axes_grid1 import make_axes_locatable

from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.gp import gp_Pln
from OCC.Extend.ShapeFactory import make_face
from OCCUtils.Construct import make_plane

from OCCDisplay import OCCDisplay


class OpticsTraject_3D (OCCDisplay):

    def __init__(self, xyz=[-50, -50, 0], vec=[1, 1, 0]):
        super(OpticsTraject_3D, self).__init__()

        self.cff = [1.5, 1.5, 2.0]
        self.rng = [30.0, 5.0, 1.0]
        self.sig = [10.0, 20.0, 30.0]
        self.set_axs(xyz, vec)

    def get_dat(self):
        pnt = self.axs.Location()
        vec = self.axs.Direction()
        x, y, z = pnt.X(), pnt.Y(), pnt.Z()
        p, q, r = vec.X(), vec.Y(), vec.Z()
        return [x, y, z, p, q, r]

    def set_axs(self, xyz=[0, 0, 0], vec=[1, 0, 0]):
        ref = self.refract_3d(xyz)
        n_vec = ref * np.array(vec)
        self.axs = gp_Ax3(gp_Pnt(*xyz), gp_Dir(*n_vec))

    def diff_func(self, dat, t):
        # Compute the differential
        pos = [*dat[0:3]]
        vec = [*dat[3:6]]
        grd = nd.Gradient(self.refract)(pos)
        ref = self.refract(pos)
        #self.pos = [self.vec[0], self.vec[1]]
        #self.vec = [grd[0] * ref, grd[1] * ref]
        return vec + [grd[0] * ref, grd[1] * ref, grd[2] * ref]

    def diff_run(self, t=[0, 50, 0.01]):
        self.t_range = np.arange(*t)
        ini_dat = self.get_dat()
        dat = odeint(self.diff_func, ini_dat, self.t_range)
        self.dat = np.array(dat)
        print(self.dat)

    def refract(self, xyz=[0, 0, 0]):
        # Refractive index function
        return self.refract_3d(xyz)

    def refract_1d(self, x=0, cff=1.0, rng=0.0, sig=0):
        ref = cff / (1 + np.exp(-(x - sig) / rng))
        return ref

    def refract_2d(self, xy=[0, 0]):
        ref_x = self.refract_1d(xy[0], self.cff[0], self.rng[0])
        ref_y = self.refract_1d(xy[1], self.cff[1], self.rng[1])
        return ref_x + ref_y

    def refract_3d(self, pos=[0, 0, 0]):
        ref = 0
        for i, p in enumerate(pos):
            cff = self.cff[i]
            rng = self.rng[i]
            sig = self.sig[i]
            ref += self.refract_1d(p, cff, rng, sig)
        return ref

    def plot_countourf_2d(self, dirname="./tmp/", pngname="plot_snell_3d"):
        plt.figure()
        plt.subplot(311)
        plt.plot(self.t_range, self.dat[:, 0])

        plt.subplot(312)
        plt.plot(self.t_range, self.dat[:, 1])

        plt.subplot(313)
        plt.plot(self.t_range, self.dat[:, 2])

        pngfile = dirname + pngname + "_xyz.png"
        plt.savefig(pngfile)

        plt.figure()
        plt.subplot(311)
        px = self.dat[:, 0]
        nx = self.refract_1d(px, self.cff[0], self.rng[0], self.sig[0])
        plt.plot(px, nx)

        plt.subplot(312)
        px = self.dat[:, 1]
        nx = self.refract_1d(px, self.cff[1], self.rng[1], self.sig[1])
        plt.plot(px, nx)

        plt.subplot(313)
        px = self.dat[:, 2]
        nx = self.refract_1d(px, self.cff[2], self.rng[2], self.sig[2])
        plt.plot(px, nx)

        pngfile = dirname + pngname + "_ref.png"
        plt.savefig(pngfile)

    def plot_3d(self):
        print("ok")
        self.display.DisplayShape(gp_Pnt())

        pln_x = make_plane(gp_Pnt(self.sig[0], 0, 0), gp_Vec(1, 0, 0))
        self.display.DisplayShape(pln_x, color="RED", transparency=0.5)

        pln_y = make_plane(gp_Pnt(0, self.sig[1], 0), gp_Vec(0, 1, 0))
        self.display.DisplayShape(pln_y, color="GREEN", transparency=0.5)

        pln_z = make_plane(gp_Pnt(0, 0, self.sig[2]), gp_Vec(0, 0, 1))
        self.display.DisplayShape(pln_z, color="BLUE", transparency=0.5)

        for i, data in enumerate(self.dat):
            xyz = data[0], data[1], data[2]
            self.display.DisplayShape(gp_Pnt(*xyz))


if __name__ == '__main__':
    obj = OpticsTraject_3D()
    obj.diff_run(t=[0, 100, 2.0])
    obj.plot_countourf_2d()
    obj.plot_3d()
    obj.start_display()
