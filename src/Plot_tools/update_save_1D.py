# Update plot objects if saving
# Assume the field is 1-dimensional

import matplotlib.pyplot as plt
import numpy as np
from Plot_tools.smart_time import smart_time

def update_save_1D(sim):

    sim.fig.suptitle(smart_time(sim.time))

    for var_cnt in range(len(sim.plot_vars)):

        var = sim.plot_vars[var_cnt]

        # Update plot
        for L in range(sim.Nz):

            if var == 'u':
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.u[0:sim.Nx,0:sim.Ny+1,L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.u[0:sim.Nx,0:sim.Ny,L]
            elif var == 'v':
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.v[0:sim.Nx+1,0:sim.Ny,L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.v[0:sim.Nx,0:sim.Ny,L]
            elif var == 'h':
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.h[0:sim.Nx+1,0:sim.Ny+1,L] - sim.Hs[L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.h[0:sim.Nx,0:sim.Ny,L] - sim.Hs[L]
            elif var == 'vort':
                to_plot = sim.ddx_v(sim.soln.v[:,:,L],sim) \
                        - sim.ddy_u(sim.soln.u[:,:,L],sim)
                to_plot = to_plot.ravel()
                if sim.f0 != 0:
                    to_plot *= 1./sim.f0
            elif var == 'div':
                h = sim.soln.h[:,:,L]
                to_plot = sim.ddx_u(h*sim.soln.u[:,:,L],sim) \
                        + sim.ddy_v(h*sim.soln.v[:,:,L],sim)
                to_plot = to_plot.ravel()
                if sim.f0 != 0:
                    to_plot *= 1./sim.f0


            sim.Qs[var_cnt][L].set_ydata(to_plot)

            if len(sim.ylims[var_cnt]) != 2: 
                sim.axs[var_cnt][L].relim()
                tmp = sim.axs[var][L].get_ylim()
                sim.axs[var_cnt][L].set_ylim([-np.max(np.abs(tmp)), np.max(np.abs(tmp))]);
                sim.axs[var_cnt][L].autoscale_view()

    plt.draw()

    sim.fig.savefig('Outputs/{0:s}/Frames/frame_{1:05d}.png'.format(sim.run_name,sim.frame_count))
    sim.frame_count += 1

