import numpy as np
import matplotlib.pyplot as plt
import numdifftools as nd
from scipy.integrate import odeint
from mpl_toolkits.axes_grid1 import make_axes_locatable


class OpticsTraject (object):

    def __init__(self):
        self.cff_x = 0.1
        self.rng_x = 10.0
        self.cff_y = 2.0
        self.rng_y = 1.5

        self.xy0 = [0, 0]
        self.th0 = 0.0
        # self.vc0 = [self.refract_2d(r_0[0]) * np.cos(theta_0),
        #            self.refract_2d(r_0[0]) * np.sin(theta_0)]

    def initialize(self, xy=[0,0], th=0):
        print("ok")

    def refract_2d(self, x=0, y=0):
        ref_x = self.cff_x - (self.cff_x - 1) / \
            (1 + np.exp(-(x - self.cff_x**2) / self.rng_x))
        ref_y = self.cff_y - (self.cff_y - 1) / \
            (1 + np.exp(-(y - self.cff_y**2) / self.rng_y))
        return ref_x + ref_y

    def refract(self, r):
        # Refractive index function
        return self.refract_2d(*r)

    def diff_y(self, y, t):
        # Compute the differential
        grd = nd.Gradient(self.refract)([y[0], y[1]])
        n_t = self.refract([y[0], y[1]])
        return [y[2], y[3], grd[0] * n_t, grd[1] * n_t]

    def plot_2d(self):
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
        plt.colorbar(im, ax=ax, shrink=0.9)

        plt.savefig("./plot_snell.png")


if __name__ == '__main__':
    obj = OpticsTraject()
    obj.plot_2d()
