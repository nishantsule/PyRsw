import numpy as np
from Steppers.Euler import Euler

def AB2(sim):
    if sim.nfluxes < 1:
        sim.nfluxes = 1

    if len(sim.fluxes.u) == 0:

        Euler(sim)

    elif len(sim.fluxes.u) == 1:
        
        # Compute the fluxes
        sim.flux()

        if sim.adaptive:
            # The AB2 weights for adaptive delta(t)
            w1 = sim.dt*(1. + 0.5*sim.dt/sim.dts[0])
            w2 = -0.5*sim.dt**2/sim.dts[0]
        else:
            # The AB2 weights for fixed delta(t)
            w1 =  3./2.*sim.dt
            w2 = -1./2.*sim.dt
        
        # Evolve the system
        sim.soln.u += w1*sim.curr_flux.u + w2*sim.fluxes.u[0]
        sim.soln.v += w1*sim.curr_flux.v + w2*sim.fluxes.v[0]
        sim.soln.h += w1*sim.curr_flux.h + w2*sim.fluxes.h[0]
        
        # Store the appropriate history
        if sim.nfluxes == 1:
            sim.fluxes.u = [sim.curr_flux.u.copy()]
            sim.fluxes.v = [sim.curr_flux.v.copy()]
            sim.fluxes.h = [sim.curr_flux.h.copy()]
            sim.dts    = [sim.dt]
        else:
            sim.fluxes.u = [sim.curr_flux.u.copy()] + sim.fluxes.u
            sim.fluxes.v = [sim.curr_flux.v.copy()] + sim.fluxes.v
            sim.fluxes.h = [sim.curr_flux.h.copy()] + sim.fluxes.h
            sim.dts = [sim.dt] + sim.dts
