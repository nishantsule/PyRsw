# Initialize plot objects for anim or save
# Assume that hte field is 2-dimensional

import numpy as np
import matplotlib.pyplot as plt

from Plot_tools.update_anim_2D import update_anim_2D
from Plot_tools.update_save_2D import update_save_2D

def initialize_plots_animsave_2D(sim):

    figs = []
    Qs   = []
    ttls = []

    # Loop through each element of plot_vars
    # Each field will be given its own figure
    for var_cnt in range(len(sim.plot_vars)):

        Qs   += [[]]
        ttls += [[]]

        var = sim.plot_vars[var_cnt]

        fig = plt.figure()
        figs += [fig]

        # Plot the data
        for L in range(sim.Nz):

            plt.subplot(1,sim.Nz,L+1)

            if var == 'u':
                ttl = fig.suptitle('Zonal Velocity : t = 0')
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.u[0:sim.Nx,0:sim.Ny+1,L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.u[0:sim.Nx,0:sim.Ny,L]
                X = sim.grid_x.u
                Y = sim.grid_y.u
            elif var == 'v':
                ttl = fig.suptitle('Meridional Velocity : t = 0')
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.v[0:sim.Nx+1,0:sim.Ny,L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.v[0:sim.Nx,0:sim.Ny,L]
                X = sim.grid_x.v
                Y = sim.grid_y.v
            elif var == 'h':
                ttl = fig.suptitle('Free Surface Displacement : t = 0')
                if sim.method.lower() == 'sadourny':
                    to_plot = sim.soln.h[0:sim.Nx+1,0:sim.Ny+1,L] - sim.Hs[L]
                elif sim.method.lower() == 'spectral':
                    to_plot = sim.soln.h[0:sim.Nx,0:sim.Ny,L] - sim.Hs[L]
                X = sim.grid_x.h
                Y = sim.grid_y.h
            elif var == 'vort':
                
                if sim.method.lower() == 'sadourny':
                    to_plot =     sim.ddx_v(sim.soln.v[0:sim.Nx+1,0:sim.Ny,L],sim.dx[0]) \
                                - sim.ddy_u(sim.soln.u[0:sim.Nx,0:sim.Ny+1,L],sim.dx[1])
                    to_plot = sim.avx_u(sim.avy_v(to_plot))
                elif sim.method.lower() == 'spectral':
                    to_plot =     sim.ddx_v(sim.soln.v[0:sim.Nx,0:sim.Ny,L],sim) \
                                - sim.ddy_u(sim.soln.u[0:sim.Nx,0:sim.Ny,L],sim)
                
                X = sim.grid_x.h
                Y = sim.grid_y.h

                if sim.f0 != 0:
                    ttl = fig.suptitle('Vorticity / f_0 : t = 0')
                    to_plot *= 1./sim.f0
                else:   
                    ttl = fig.suptitle('Vorticity : t = 0')
            elif var == 'div':

                if sim.method.lower() == 'sadourny':
                    to_plot =     sim.ddx_u(sim.avx_h(sim.soln.h[0:sim.Nx+1,0:sim.Ny+1,L])*sim.soln.u[0:sim.Nx,0:sim.Ny+1,L],sim.dx[0]) \
                                + sim.ddy_v(sim.avy_h(sim.soln.h[0:sim.Nx+1,0:sim.Ny+1,L])*sim.soln.v[0:sim.Nx+1,0:sim.Ny,L],sim.dy[0])
                elif sim.method.lower() == 'spectral':
                    h = sim.soln.h[:,:,L] 
                    to_plot =     sim.ddx_u(h*sim.soln.u[0:Nx,0:Ny,L],sim) \
                                + sim.ddy_v(h*sim.soln.v[0:Nx,0:Ny,L],sim)

                X = sim.grid_x.h
                Y = sim.grid_y.h

                if sim.f0 != 0:
                    ttl = fig.suptitle('Divergence of mass-flux / f_0 : t = 0')
                    to_plot *= 1./sim.f0
                else:   
                    ttl = fig.suptitle('Divergence of mass-flux : t = 0')

            # Has the user specified plot limits?
            if len(sim.clims[var_cnt]) == 2:
                vmin = sim.clims[var_cnt][0]
                vmax = sim.clims[var_cnt][1]
            else:
                cv = np.max(np.abs(to_plot.ravel()))
                vmin = -cv
                vmax =  cv

            # Extend the grid to account for pcolor peculiarities
            Nx = X.shape[0]
            Ny = Y.shape[1]
            X_plot = np.zeros((Nx+1,Ny+1))
            Y_plot = np.zeros((Nx+1,Ny+1))

            X_plot[1:,1:] = X + sim.dx[0]/2.
            X_plot[1:,0]  = X[:,0] + sim.dx[0]/2.
            X_plot[0,:]   = X[0,0] - sim.dx[0]/2.

            Y_plot[1:,1:] = Y + sim.dx[1]/2.
            Y_plot[0,1:]  = Y[0,:] + sim.dx[1]/2.
            Y_plot[:,0]   = Y[0,0] - sim.dx[1]/2.

            Q = plt.pcolormesh(X_plot/1e3, Y_plot/1e3, to_plot, cmap=sim.cmap, 
                        vmin = vmin, vmax = vmax)
            Qs[var_cnt] += [Q]
            ttls[var_cnt] += [ttl]

            plt.colorbar()

            plt.axis('tight')

            if 1./1.1 <= sim.Ly/sim.Lx <= 1.1:
                plt.gca().set_aspect('equal')

    if sim.animate == 'Anim':
        sim.update_plots = update_anim_2D
    elif sim.animate == 'Save':
        sim.update_plots = update_save_2D
        plt.ioff()
        plt.pause(0.01)

    if sim.animate == 'Anim':
        plt.ion()
        plt.pause(0.01)
        plt.draw()

    sim.figs = figs
    sim.Qs = Qs
    sim.ttls = ttls

