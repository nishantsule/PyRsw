# Update plot objects if animating
import numpy as np
from smart_time import smart_time
import matplotlib.pyplot as plt

def update_anim_2D(sim):

    Nx, Ny = sim.Nx, sim.Ny
    for var_cnt in range(len(sim.plot_vars)):

        var = sim.plot_vars[var_cnt]

        for L in range(sim.Nz):

            if var == 'u':
                sim.ttls[var_cnt][L].set_text('Zonal Velocity : {0:s}'.format(smart_time(sim.time)))
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.u[0:sim.Nx,0:sim.Ny+1,L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.u[0:sim.Nx,0:sim.Ny,L]
            elif var == 'v':
                sim.ttls[var_cnt][L].set_text('Meridional Velocity : {0:s}'.format(smart_time(sim.time)))
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.v[0:sim.Nx+1,0:sim.Ny,L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.v[0:sim.Nx,0:sim.Ny,L]
            elif var == 'h':
                sim.ttls[var_cnt][L].set_text('Free Surface Displacement : {0:s}'.format(smart_time(sim.time)))
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.h[0:sim.Nx+1,0:sim.Ny+1,L] - sim.Hs[L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.h[0:sim.Nx,0:sim.Ny,L] - sim.Hs[L]
            elif var == 'vort':
                to_plot =     sim.ddx_v(sim.soln.v[0:Nx,0:Ny,L],sim) \
                            - sim.ddy_u(sim.soln.u[0:Nx,0:Ny,L],sim)
                if sim.f0 != 0:
                    sim.ttls[var_cnt][L].set_text('Vorticity / f_0 : {0:s}'.format(smart_time(sim.time)))
                    to_plot *= 1./sim.f0
                else:   
                    sim.ttls[var_cnt][L].set_text('Vorticity : {0:s}'.format(smart_time(sim.time)))
            elif var == 'div':
                h = sim.soln.h[:,:,L] 
                to_plot =     sim.ddx_u(h*sim.soln.u[0:Nx,0:Ny,L],sim) \
                            + sim.ddy_v(h*sim.soln.v[0:Nx,0:Ny,L],sim)
                if sim.f0 != 0:
                    sim.ttls[var_cnt][L].set_text('Divergence of mass-flux / f_0 : {0:s}'.format(smart_time(sim.time)))
                    to_plot *= 1./sim.f0
                else:   
                    sim.ttls[var_cnt][L].set_text('Divergence of mass-flux : {0:s}'.format(smart_time(sim.time)))

            sim.Qs[var_cnt][L].set_array(to_plot.ravel())
            sim.Qs[var_cnt][L].changed()
        plt.pause(0.01) 
    plt.draw()



