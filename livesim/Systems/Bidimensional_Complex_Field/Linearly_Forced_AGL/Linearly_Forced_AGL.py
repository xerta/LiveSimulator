# coding: utf-8
# !/usr/bin/env python

import numpy as np
import os

from ..Bidimensional_Complex_Field import *


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# constants
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
MU1 = 1
DELTA = 0.1
XI = 0.01
MU2 = 0.1
FREC = 1
N = 2  # Dirichlet border condition


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Linearly_Forced_AGL(Bidimensional_Complex_Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir = os.path.dirname(__file__)

        self.param_strs = ["μ₁", "δ", "ξ", "μ₂", "f"]
        self.params = [MU1, DELTA, XI, MU2, FREC]

        self._title = "Anisotropic Ginzburg Landau"

    def time_step_neumann(self):
        mu1, delta, xi, mu2, f = self.params
        A, Ac, A_sig = np.copy(self.A), np.conj(self.A), np.copy(self.A)
        inv_dx, inv_dy, dt, t = 1/self.dx, 1/self.dy, self.dt, self.t
        inv_dx2, inv_dy2 = 1/self.dx**2, 1/self.dy**2

        A_sig[1:-1, 1:-1] += dt * \
            ((mu1 + mu2*np.cos(2*np.pi*f*t)) * A[1:-1, 1:-1] -
             np.abs(A[1:-1, 1:-1])**2 * A[1:-1, 1:-1] + \
             (A[2:, 1:-1] + A[0:-2, 1:-1] - 2*A[1:-1, 1:-1])*inv_dx2 + \
             (A[1:-1, 2:] + A[1:-1, 0:-2] - 2*A[1:-1, 1:-1])*inv_dy2 + \
             delta*((Ac[2:, 1:-1] + Ac[:-2, 1:-1] - 2*Ac[1:-1, 1:-1])*inv_dx2 -
                    (Ac[1:-1, 2:] + Ac[1:-1, :-2] - 2*Ac[1:-1, 1:-1])*inv_dy2 +
                    0.5j*(Ac[2:, 2:] + Ac[:-2, :-2] - Ac[2:, :-2] -
                          Ac[:-2, 2:])*inv_dx*inv_dy) + \
             np.sqrt(xi) * np.random.normal(size=[self.nx-2, self.ny-2]) * \
             np.exp(2j*np.random.rand(self.nx-2, self.ny-2)*np.pi))

        # Neumann border conditions
        A_sig[0, :] = A_sig[1, :]  # left border
        A_sig[-1, :] = A_sig[-2, :]  # right border
        A_sig[:, 0] = A_sig[:, 1]  # bottom border
        A_sig[:, -1] = A_sig[:, -2]  # upper border

        self.t += self.dt
        self.A = A_sig

    def time_step_periodic(self):
        mu1, delta, xi, mu2, omega = self.params
        A, Ac, A_sig = np.copy(self.A), np.conj(self.A), np.copy(self.A)
        inv_dx, inv_dy, dt, t = 1/self.dx, 1/self.dy, self.dt, self.t
        inv_dx2, inv_dy2 = 1/self.dx**2, 1/self.dy**2

        A_sig += dt * \
            ((mu1 + mu2*np.cos(omega*t)) * A -
             np.abs(A)**2 * A + \
             (np.roll(A,1,axis=0)+np.roll(A,-1,axis=0)-2*A)*inv_dx2 + \
             (np.roll(A,1,axis=1)+np.roll(A,-1,axis=1)-2*A)*inv_dy2 + \
             delta*((np.roll(Ac,1,axis=0)+np.roll(Ac,-1,axis=0)-2*Ac)*inv_dx2 -
                    (np.roll(Ac,1,axis=1)+np.roll(Ac,-1,axis=1)-2*Ac)*inv_dy2 +
                    0.5j*(np.roll(np.roll(Ac,1,axis=0),1,axis=1) +
                          np.roll(np.roll(Ac,-1,axis=0),-1,axis=1) -
                          np.roll(np.roll(Ac,1,axis=0),-1,axis=1) -
                          np.roll(np.roll(Ac,-1,axis=0),1,axis=1)
                          )*inv_dx*inv_dy) + \
             np.sqrt(xi) * np.random.normal(size=[self.nx, self.ny]) * \
             np.exp(2j*np.random.rand(self.nx, self.ny)*np.pi))

        self.t += self.dt
        self.A = A_sig

    def time_step_dirichlet(self):
        mu1, delta, xi, mu2, omega = self.params
        A, Ac, A_sig = np.copy(self.A), np.conj(self.A), np.copy(self.A)
        inv_dx, inv_dy, dt, t = 1/self.dx, 1/self.dy, self.dt, self.t
        inv_dx2, inv_dy2 = 1/self.dx**2, 1/self.dy**2

        A_sig[1:-1, 1:-1] += dt * \
            ((mu1 + mu2*np.cos(omega*t)) * A[1:-1, 1:-1] -
             np.abs(A[1:-1, 1:-1])**2 * A[1:-1, 1:-1] + \
             (A[2:, 1:-1] + A[0:-2, 1:-1] - 2*A[1:-1, 1:-1])*inv_dx2 + \
             (A[1:-1, 2:] + A[1:-1, 0:-2] - 2*A[1:-1, 1:-1])*inv_dy2 + \
             delta*((Ac[2:, 1:-1] + Ac[:-2, 1:-1] - 2*Ac[1:-1, 1:-1])*inv_dx2 -
                    (Ac[1:-1, 2:] + Ac[1:-1, :-2] - 2*Ac[1:-1, 1:-1])*inv_dy2 +
                    0.5j*(Ac[2:, 2:] + Ac[:-2, :-2] - Ac[2:, :-2] -
                          Ac[:-2, 2:])*inv_dx*inv_dy) + \
             np.sqrt(xi) * np.random.normal(size=[self.nx-2, self.ny-2]) * \
             np.exp(2j*np.random.rand(self.nx-2, self.ny-2)*np.pi))

        # Dirichlet border conditions
        A_sig[0, :] = np.sqrt(mu) * \
            np.exp(N * 1j*np.arctan2(.5*self.height-self.y[:],
                                     .5*self.width-self.x[0]))  # left border
        A_sig[-1, :] = np.sqrt(mu) * \
            np.exp(N * 1j*np.arctan2(.5*self.height-self.y[:],
                                     .5*self.width-self.x[-1]))  # right border
        A_sig[:, 0] = np.sqrt(mu) * \
            np.exp(N * 1j*np.arctan2(.5*self.height-self.y[0],
                                     .5*self.width-self.x[:]))  # bottom border
        A_sig[:, -1] = np.sqrt(mu) * \
            np.exp(N * 1j*np.arctan2(.5*self.height-self.y[-1],
                                     .5*self.width-self.x[:]))  # upper border

        self.t += self.dt
        self.A = A_sig
