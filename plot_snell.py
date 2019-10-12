import numpy as np
import matplotlib.pyplot as plt
import numdifftools as nd
from scipy.integrate import odeint


class OpticsTraject (object):

    def __init__(self):
        self.cff_x = 2.0
        self.rng_x = 0.2
        self.cff_y = 2.0
        self.rng_y = 1.5

        self.xy0 = [0, 0]
        self.th0 = 0.0
        # self.vc0 = [self.refract_2d(r_0[0]) * np.cos(theta_0),
        #            self.refract_2d(r_0[0]) * np.sin(theta_0)]
    
    def initialize (self):
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
        px = np.linspace(-1, 1, 100) * 100
        py = np.linspace(-1, 1, 100) * 100
        mesh = np.meshgrid(px, py)
        pcm = plt.pcolormesh(*mesh, self.refract(mesh), cmap='jet', vmin=1)
        cbar = plt.colorbar(pcm)
        cbar.ax.set_ylabel("n  Refractive index")

        plt.xlabel("cm")
        plt.ylabel("cm")
        plt.savefig("./plot_snell.png")
        plt.show()


if __name__ == '__main__':
    obj = OpticsTraject()
    obj.plot_2d()
