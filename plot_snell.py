import numpy as np
import matplotlib.pyplot as plt
import numdifftools as nd
from scipy.integrate import odeint
from mpl_toolkits.axes_grid1 import make_axes_locatable


class OpticsTraject (object):

    def __init__(self, xy=[-50, -50], th=45):
        self.cff_x = 1.1
        self.rng_x = 30.0
        self.cff_y = 1.5
        self.rng_y = 0.1
        self.initialize(xy, th)

    def diff_func(self, dat, t):
        # Compute the differential
        pos = [dat[0], dat[1]]
        vec = [dat[2], dat[3]]
        grd = nd.Gradient(self.refract)(pos)
        ref = self.refract(pos)
        #self.pos = [self.vec[0], self.vec[1]]
        #self.vec = [grd[0] * ref, grd[1] * ref]
        return vec + [grd[0] * ref, grd[1] * ref] + [ref]

    def diff_run(self, t=[0, 50, 0.01]):
        self.t_range = np.arange(*t)
        ini_dat = self.pos + self.vec + [self.ref]
        dat = odeint(self.diff_func, ini_dat, self.t_range)
        self.dat = np.array(dat)
        print(self.dat)

    def initialize(self, xy=[0, 0], th=0):
        self.pos = [xy[0], xy[1]]
        self.rad = np.deg2rad(th)

        self.ref = self.refract_2d(*self.pos)
        self.vec = [
            self.ref * np.cos(self.rad),
            self.ref * np.sin(self.rad)
        ]

    def refract_2d(self, x=0, y=0):
        ref_x = self.cff_x - (self.cff_x - 1) / \
            (1 + np.exp(-(x - self.cff_x**2) / self.rng_x))
        ref_y = self.cff_y - (self.cff_y - 1) / \
            (1 + np.exp(-(y - self.cff_y**2) / self.rng_y))
        return ref_x + ref_y

    def refract(self, xy=[0, 0]):
        # Refractive index function
        return self.refract_2d(*xy)

    def plot_2d(self, dirname="./", pngname="plot_snell"):
        sx, sy = 50.0, 50.0
        nx, ny = 100, 100
        px = np.linspace(-1, 1, nx) * 100
        py = np.linspace(-1, 1, ny) * 100
        mesh = np.meshgrid(px, py)
        func = self.refract(mesh)

        xs, ys = mesh[0][0, 0], mesh[1][0, 0]
        dx, dy = mesh[0][0, 1] - mesh[0][0, 0], mesh[1][1, 0] - mesh[1][0, 0]
        mx, my = int((sy - ys) / dy), int((sx - xs) / dx)

        fig, ax = plt.subplots()
        divider = make_axes_locatable(ax)
        ax.set_aspect('equal')

        ax_x = divider.append_axes("bottom", 1.0, pad=0.5, sharex=ax)
        ax_x.plot(mesh[0][mx, :], func[mx, :])
        ax_x.set_title("y = {:.2f}".format(sy))

        ax_y = divider.append_axes("right", 1.0, pad=0.5, sharey=ax)
        ax_y.plot(func[:, my], mesh[1][:, my])
        ax_y.set_title("x = {:.2f}".format(sx))

        im = ax.contourf(*mesh, func, cmap="jet")
        ax.plot(self.dat[:, 0], self.dat[:, 1])
        plt.colorbar(im, ax=ax, shrink=0.9)

        pngfile = dirname + pngname + ".png"
        plt.savefig(pngfile)

        plt.subplot(211)
        plt.plot(self.t_range, self.dat[:, 0])

        plt.subplot(212)
        plt.plot(self.t_range, self.dat[:, 1])

        pngfile = dirname + pngname + "_xy.png"
        plt.savefig(pngfile)

        plt.subplot()
        plt.plot(self.t_range, self.dat[:, -1])

        pngfile = dirname + pngname + "_ref.png"
        plt.savefig(pngfile)


if __name__ == '__main__':
    obj = OpticsTraject()
    obj.diff_run()
    obj.plot_2d()

    obj.initialize(xy=[-50, -50], th=30)
    obj.diff_run(t=[0, 50, 1.0])
    obj.plot_2d(pngname="plot_snell01")

    obj.initialize(xy=[-50, -50], th=30)
    obj.diff_run(t=[0, 50, 0.01])
    obj.plot_2d(pngname="plot_snell02")
