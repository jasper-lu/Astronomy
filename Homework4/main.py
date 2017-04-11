import numpy

import numpy as np
import matplotlib.pyplot as plt

HUBBLE_DIST = 3
HUBBLE_TIME = 9.78
STEPS = 100
# Utility functions
def mid_rect(f,x,h):
  return f(x + h/2)

def integrate(f, a, b, steps):
    h = (b - a) / steps
    ival = h * sum(mid_rect(f, a + i * h, h) for i in range(steps))
    return ival

def make_E(matter, energy, w):
    def E(z):
        m_term = matter * ((1 + z) ** 3)
        e_term = energy * ((1 + z) ** (3 * (1 + w)))
        return np.sqrt(m_term + e_term)
    return E

class Model:
    # omega_m and omega_e represent the constants
    # for matter and dark energy, respectively
    def __init__(self, omega_m, omega_e, w=0):
        self.E = make_E(omega_m, omega_e, w)
        self.omega_m = omega_m
        self.omega_e = omega_e
        self.w = w
        if w == 0:
            self.name = "$\Omega_m$=%s $\Omega_{\Lambda}$=%s" %(omega_m, omega_e)
        else:
            self.name = "$\Omega_m$=%s $\Omega_{\Lambda}$=%s w=%s" %(omega_m, omega_e, w)

    # Comoving distance
    def d_c(self, z):
        def to_int(x):
            return 1 / self.E(x)
        return HUBBLE_DIST * integrate(to_int, 0, z, STEPS)

    # Comoving Distance, transverse.
    # We Assumes model will only have a flat universe, so this function
    # is redundant, but for completeness's sake, we include it anyway
    def d_m(self, z):
        return self.d_c(z)

    # Angular Distance
    def d_a(self, z):
        return self.d_m(z) / (1 + z)

    # Luminosity Distance
    def d_l(self, z):
            return ((1 + z) ** 2) * self.d_a(z)

    # Comoving Volume
    # Again, we have a flat universe, so this function is greatly simplified
    def v_c(self, z):
        return 4 * np.pi * (self.d_m(z) ** 3) / 3

    # Lookback Time
    # Might need to play with paramters of c to get this work properly
    def t_l(self, z):
        def to_int(x):
            return 1 / ((1 + x) * self.E(x))
        return HUBBLE_TIME * integrate(to_int, 0, z, STEPS)

lin_steps = np.linspace(0, 3, 60)

def plot_helper(axes, f):
    return [axes.plot(lin_steps, [g(x) for x in lin_steps])[0] for g in f]


def create_plot_a(models):
    fig = plt.figure()
    axes = fig.add_subplot(111)
    plots = plot_helper(axes, [m.d_c for m in models])
    plt.legend(plots, [m.name for m in models])
    plt.ylabel("$D_C$ ($h^{-1}Gpc$)")
    plt.xlabel("z")
    plt.title("Comoving Distance vs Redshift")
    return plt

def create_plot_b(models):
    fig = plt.figure()
    axes = fig.add_subplot(111)
    plots = plot_helper(axes, [m.d_l for m in models])
    plt.legend(plots, [m.name for m in models])
    plt.ylabel("$D_L$ ($h^{-1}Gpc$)")
    plt.xlabel("z")
    plt.title("Luminosity Distance vs Redshift")
    return plt

def create_plot_c(models):
    fig = plt.figure()
    axes = fig.add_subplot(111)
    plots = plot_helper(axes, [m.d_a for m in models])
    plt.legend(plots, [m.name for m in models])
    plt.ylabel("$D_A$ ($h^{-1}Gpc$)")
    plt.xlabel("z")
    plt.title("Angular Diameter Distance vs Redshift")
    return plt

def create_plot_d(models):
    fig = plt.figure()
    axes = fig.add_subplot(111)
    plots = plot_helper(axes, [m.v_c for m in models])
    plt.legend(plots, [m.name for m in models])
    plt.ylabel("$V_C$ ($h^{-3}Gpc^3$)")
    plt.xlabel("z")
    plt.title("Comoving Volume of a Sphere vs Redshift")
    return plt

def create_plot_e(models):
    fig = plt.figure()
    axes = fig.add_subplot(111)
    plots = plot_helper(axes, [m.t_l for m in models])
    plt.legend(plots, [m.name for m in models])
    plt.ylabel("Lookback Time (Gyr)")
    plt.xlabel("z")
    plt.title("Lookback Time vs Redshift")
    return plt

def main():
    model_1 = Model(1, 0)
    model_2 = Model(0.25, .75, -1)
    model_3 = Model(0.25, .75, -0.8)
    model_4 = Model(0.25, .75, -1.2)

    model_arr = [model_1, model_2, model_3, model_4]
    plot_a = create_plot_a(model_arr)
    plot_a.savefig("PlotA")
    plot_b = create_plot_b(model_arr)
    plot_b.savefig("PlotB")
    plot_c = create_plot_c(model_arr)
    plot_c.savefig("PlotC")
    plot_d = create_plot_d(model_arr)
    plot_d.savefig("PlotD")
    plot_e = create_plot_e(model_arr)
    plot_e.savefig("PlotE")

if __name__ == '__main__':
    main()
