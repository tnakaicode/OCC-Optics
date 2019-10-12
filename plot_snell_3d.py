import numpy as np
import matplotlib.pyplot as plt
import numdifftools as nd
from scipy.integrate import odeint
from mpl_toolkits.axes_grid1 import make_axes_locatable

from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Ax1, gp_Ax2, gp_Ax3
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir

from OCCDisplay import OCCDisplay


class OpticsTraject_3D (OCCDisplay):

    def __init__(self, xyz=[-50, -50, 0], vec=[1, 0, 0]):
        super(OpticsTraject_3D, self).__init__()

        self.cff = [1.1, 1.1, 1.0]
        self.rng = [30.0, 1.5, 1.0]
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

    def refract_2d(self, x=0, y=0):
        ref_x = self.cff_x - (self.cff_x - 1) / \
            (1 + np.exp(-(x - self.cff_x**2) / self.rng_x))
        ref_y = self.cff_y - (self.cff_y - 1) / \
            (1 + np.exp(-(y - self.cff_y**2) / self.rng_y))
        return ref_x + ref_y

    def refract_3d(self, pos=[0, 0, 0]):
        ref = 0
        for i, p in enumerate(pos):
            cff = self.cff[i]
            rng = self.rng[i]
            ref += cff - (cff - 1) / (1 + np.exp(-(p - cff**2) / rng))
        return ref

    def plot_2d(self, dirname="./", pngname="plot_snell_3d"):

        plt.subplot(311)
        plt.plot(self.t_range, self.dat[:, 0])

        plt.subplot(312)
        plt.plot(self.t_range, self.dat[:, 1])

        plt.subplot(313)
        plt.plot(self.t_range, self.dat[:, 2])

        pngfile = dirname + pngname + "_xyz.png"
        plt.savefig(pngfile)

    def plot_3d(self):
        print("ok")
        self.display.DisplayShape(gp_Pnt())
        for i, data in enumerate(self.dat):
            xyz = data[0], data[1], data[2]
            self.display.DisplayShape(gp_Pnt(*xyz))


if __name__ == '__main__':
    obj = OpticsTraject_3D()
    obj.diff_run(t=[0, 100, 2.0])
    obj.plot_2d()
    obj.plot_3d()
    obj.start_display()
