"""Time stepping (:mod:`fluidsim.base.time_stepping.pseudo_spect`)
========================================================================

Provides:

.. autoclass:: TimeSteppingPseudoSpectral
   :members:
   :private-members:

.. todo::

  It would be interesting to implement phase-shifting timestepping schemes as:

  - RK2 + phase-shifting

  - Adams-Bashforth (leapfrog) + phase-shifting

  For a theoretical presentation of phase-shifting see
  https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19810022965.pdf.

"""

import numpy as np

from transonic import Transonic, Type, NDim, Array

from .base import TimeSteppingBase

ts = Transonic()

N = NDim(3, 4)
A = Array[np.complex128, N]

T = Type(np.float64, np.complex128)
A1 = Array[T, N]
A2 = Array[T, N - 1]


class ExactLinearCoefs:
    """Handle the computation of the exact coefficient for the RK4."""

    def __init__(self, time_stepping):
        self.time_stepping = time_stepping
        sim = time_stepping.sim
        self.shapeK_loc = sim.oper.shapeK_loc
        self.freq_lin = time_stepping.freq_lin

        self.exact = np.empty_like(self.freq_lin)
        self.exact2 = np.empty_like(self.freq_lin)

        if sim.params.time_stepping.USE_CFL:
            self.get_updated_coefs = self.get_updated_coefs_CLF
            self.dt_old = 0.0
        else:
            self.compute(time_stepping.deltat)
            self.get_updated_coefs = self.get_coefs

    def compute(self, dt):
        """Compute the exact coefficients."""
        f_lin = self.freq_lin
        exact = self.exact
        exact2 = self.exact2

        if ts.is_transpiled:
            ts.use_block("exact_lin_compute")
        else:
            # transonic block (
            #     A1 f_lin, exact, exact2;
            #     float dt
            # )
            # transonic block (
            #     A2 f_lin, exact, exact2;
            #     float dt
            # )
            exact[:] = np.exp(-dt * f_lin)
            exact2[:] = np.exp(-dt / 2 * f_lin)
        self.dt_old = dt

    def get_updated_coefs_CLF(self):
        """Get the exact coefficient updated if needed."""
        dt = self.time_stepping.deltat
        if self.dt_old != dt:
            self.compute(dt)
        return self.exact, self.exact2

    def get_coefs(self):
        """Get the exact coefficients as stored."""
        return self.exact, self.exact2


class TimeSteppingPseudoSpectral(TimeSteppingBase):
    """Time stepping class for pseudo-spectral solvers.

    """

    @staticmethod
    def _complete_params_with_default(params):
        """This static method is used to complete the *params* container.
        """
        TimeSteppingBase._complete_params_with_default(params)
        params.time_stepping.USE_CFL = True

    def __init__(self, sim):
        super().__init__(sim)

        self._init_freq_lin()
        self._init_compute_time_step()
        self._init_exact_linear_coef()
        self._init_time_scheme()

    def _init_freq_lin(self):
        f_d, f_d_hypo = self.sim.compute_freq_diss()
        freq_dissip = f_d + f_d_hypo

        if hasattr(self.sim, "compute_freq_complex"):
            freq_complex = self._compute_freq_complex()
            self.freq_lin = freq_dissip + freq_complex
            freq_max = freq_complex.imag.max()
            self.deltat_max = 0.78 * np.pi / freq_max
        else:
            self.freq_lin = freq_dissip

    def _init_time_scheme(self):

        params_ts = self.params.time_stepping

        if params_ts.type_time_scheme not in ["RK2", "RK4"]:
            raise ValueError("Problem name time_scheme")

        self._state_spect_tmp = np.empty_like(self.sim.state.state_spect)

        if params_ts.type_time_scheme == "RK4":
            self._state_spect_tmp1 = np.empty_like(self.sim.state.state_spect)

        if params_ts.type_time_scheme == "RK2":
            time_step_RK = self._time_step_RK2
        else:
            time_step_RK = self._time_step_RK4
        self._time_step_RK = time_step_RK

    def _compute_freq_complex(self):
        state_spect = self.sim.state.state_spect
        freq_complex = np.empty_like(state_spect)
        for ik, key in enumerate(state_spect.keys):
            freq_complex[ik] = self.sim.compute_freq_complex(key)
        return freq_complex

    def _init_exact_linear_coef(self):
        self.exact_linear_coefs = ExactLinearCoefs(self)

    def one_time_step_computation(self):
        """One time step"""
        # WARNING: if the function _time_step_RK comes from an extension, its
        # execution time seems to be attributed to the function
        # one_time_step_computation by cProfile
        self._time_step_RK()
        self.sim.oper.dealiasing(self.sim.state.state_spect)
        self.sim.state.statephys_from_statespect()
        # np.isnan(np.sum seems to be really fast
        if np.isnan(np.sum(self.sim.state.state_spect[0])):
            raise ValueError(f"nan at it = {self.it}, t = {self.t:.4f}")

    def _time_step_RK2(self):
        r"""Advance in time with the Runge-Kutta 2 method.

        .. _rk2timescheme:

        Notes
        -----

        .. |p| mathmacro:: \partial

        We consider an equation of the form

        .. math:: \p_t S = \sigma S + N(S),

        The Runge-Kutta 2 method computes an approximation of the
        solution after a time increment :math:`dt`. We denote the
        initial time :math:`t = 0`.

        - Approximation 1:

          .. math:: \p_t \log S = \sigma + \frac{N(S_0)}{S_0},

          Integrating from :math:`t` to :math:`t+dt/2`, it gives:

          .. |SA1halfdt| mathmacro:: S_{A1dt/2}

          .. math:: \SA1halfdt = (S_0 + N_0 dt/2) e^{\frac{\sigma dt}{2}}.


        - Approximation 2:

          .. math::
             \p_t \log S = \sigma
             + \frac{N(\SA1halfdt)}{ \SA1halfdt },

          Integrating from :math:`t` to :math:`t+dt` and retaining
          only the terms in :math:`dt^1` gives:

          .. math::
             S_{dtA2} = S_0 e^{\sigma dt}
             + N(\SA1halfdt) dt e^{\frac{\sigma dt}{2}}.

        """
        dt = self.deltat
        diss, diss2 = self.exact_linear_coefs.get_updated_coefs()

        compute_tendencies = self.sim.tendencies_nonlin
        state_spect = self.sim.state.state_spect

        tendencies_n = compute_tendencies()

        state_spect_n12 = self._state_spect_tmp

        if ts.is_transpiled:
            ts.use_block("rk2_step0")
        else:
            # transonic block (
            #     A state_spect_n12, state_spect, tendencies_n;
            #     A1 diss2;
            #     float dt
            # )
            # transonic block (
            #     A state_spect_n12, state_spect, tendencies_n;
            #     A2 diss2;
            #     float dt
            # )

            state_spect_n12[:] = (state_spect + dt / 2 * tendencies_n) * diss2

        tendencies_n12 = compute_tendencies(state_spect_n12, old=tendencies_n)

        if ts.is_transpiled:
            ts.use_block("rk2_step1")
        else:
            # transonic block (
            #     A state_spect, tendencies_n12;
            #     A1 diss, diss2;
            #     float dt
            # )

            # transonic block (
            #     A state_spect, tendencies_n12;
            #     A2 diss, diss2;
            #     float dt
            # )

            state_spect[:] = state_spect * diss + dt * diss2 * tendencies_n12

    def _time_step_RK4(self):
        r"""Advance in time with the Runge-Kutta 4 method.

        .. _rk4timescheme:

        We consider an equation of the form

        .. math:: \p_t S = \sigma S + N(S),

        The Runge-Kutta 4 method computes an approximation of the
        solution after a time increment :math:`dt`. We denote the
        initial time as :math:`t = 0`. This time scheme uses 4
        approximations. Only the terms in :math:`dt^1` are retained.

        - Approximation 1:

          .. math:: \p_t \log S = \sigma + \frac{N(S_0)}{S_0},

          Integrating from :math:`t` to :math:`t+dt/2` gives:

          .. math:: \SA1halfdt = (S_0 + N_0 dt/2) e^{\sigma \frac{dt}{2}}.

          Integrating from :math:`t` to :math:`t+dt` gives:

          .. math:: S_{A1dt} = (S_0 + N_0 dt) e^{\sigma dt}.


        - Approximation 2:

          .. math::
             \p_t \log S = \sigma
             + \frac{N(\SA1halfdt)}{ \SA1halfdt },

          Integrating from :math:`t` to :math:`t+dt/2` gives:

          .. |SA2halfdt| mathmacro:: S_{A2 dt/2}

          .. math::
             \SA2halfdt = S_0 e^{\sigma \frac{dt}{2}}
             + N(\SA1halfdt) \frac{dt}{2}.

          Integrating from :math:`t` to :math:`t+dt` gives:

          .. math::
             S_{A2dt} = S_0 e^{\sigma dt}
             + N(\SA1halfdt) e^{\sigma \frac{dt}{2}} dt.


        - Approximation 3:

          .. math::
             \p_t \log S = \sigma
             + \frac{N(\SA2halfdt)}{ \SA2halfdt },

          Integrating from :math:`t` to :math:`t+dt` gives:

          .. math::
             S_{A3dt} = S_0 e^{\sigma dt}
             + N(\SA2halfdt) e^{\sigma \frac{dt}{2}} dt.

        - Approximation 4:

          .. math::
             \p_t \log S = \sigma
             + \frac{N(S_{A3dt})}{ S_{A3dt} },

          Integrating from :math:`t` to :math:`t+dt` gives:

          .. math::
             S_{A4dt} = S_0 e^{\sigma dt} + N(S_{A3dt}) dt.


        The final result is a pondered average of the results of 4
        approximations for the time :math:`t+dt`:

          .. math::
             \frac{1}{3} \left[
             \frac{1}{2} S_{A1dt}
             + S_{A2dt} + S_{A3dt}
             + \frac{1}{2} S_{A4dt}
             \right],

        which is equal to:

          .. math::
             S_0 e^{\sigma dt}
             + \frac{dt}{3} \left[
             \frac{1}{2} N(S_0) e^{\sigma dt}
             + N(\SA1halfdt) e^{\sigma \frac{dt}{2}}
             + N(\SA2halfdt) e^{\sigma \frac{dt}{2}}
             + \frac{1}{2} N(S_{A3dt})\right].

        """
        dt = self.deltat
        diss, diss2 = self.exact_linear_coefs.get_updated_coefs()

        compute_tendencies = self.sim.tendencies_nonlin
        state_spect = self.sim.state.state_spect

        tendencies_0 = compute_tendencies()
        state_spect_tmp = self._state_spect_tmp
        state_spect_tmp1 = self._state_spect_tmp1
        state_spect_np12_approx1 = state_spect_tmp1

        if ts.is_transpiled:
            ts.use_block("rk4_step0")
        else:
            # based on approximation 0
            # transonic block (
            #     A state_spect, state_spect_tmp,
            #       tendencies_0, state_spect_np12_approx1;
            #     A1 diss, diss2;
            #     float dt
            # )

            # transonic block (
            #     A state_spect, state_spect_tmp,
            #       tendencies_0, state_spect_np12_approx1;
            #     A2 diss, diss2;
            #     float dt
            # )

            state_spect_tmp[:] = (state_spect + dt / 6 * tendencies_0) * diss
            state_spect_np12_approx1[:] = (
                state_spect + dt / 2 * tendencies_0
            ) * diss2

        tendencies_1 = compute_tendencies(
            state_spect_np12_approx1, old=tendencies_0
        )
        del state_spect_np12_approx1

        state_spect_np12_approx2 = state_spect_tmp1

        if ts.is_transpiled:
            ts.use_block("rk4_step1")
        else:
            # based on approximation 1
            # transonic block (
            #     A state_spect, state_spect_tmp,
            #       state_spect_np12_approx2, tendencies_1;
            #     A1 diss2;
            #     float dt
            # )

            # transonic block (
            #     A state_spect, state_spect_tmp,
            #       state_spect_np12_approx2, tendencies_1;
            #     A2 diss2;
            #     float dt
            # )

            state_spect_tmp[:] += dt / 3 * diss2 * tendencies_1
            state_spect_np12_approx2[:] = (
                state_spect * diss2 + dt / 2 * tendencies_1
            )

        tendencies_2 = compute_tendencies(
            state_spect_np12_approx2, old=tendencies_1
        )
        del state_spect_np12_approx2

        state_spect_np1_approx = state_spect_tmp1

        if ts.is_transpiled:
            ts.use_block("rk4_step2")
        else:
            # based on approximation 2
            # transonic block (
            #     A state_spect, state_spect_tmp,
            #       state_spect_np1_approx, tendencies_2;
            #     A1 diss, diss2;
            #     float dt
            # )

            # transonic block (
            #     A state_spect, state_spect_tmp,
            #       state_spect_np1_approx, tendencies_2;
            #     A2 diss, diss2;
            #     float dt
            # )

            state_spect_tmp[:] += dt / 3 * diss2 * tendencies_2
            state_spect_np1_approx[:] = (
                state_spect * diss + dt * diss2 * tendencies_2
            )

        tendencies_3 = compute_tendencies(
            state_spect_np1_approx, old=tendencies_2
        )
        del state_spect_np1_approx

        if ts.is_transpiled:
            ts.use_block("rk4_step3")
        else:
            # result using the 4 approximations
            # transonic block (
            #     A state_spect, state_spect_tmp, tendencies_3;
            #     float dt
            # )
            state_spect[:] = state_spect_tmp + dt / 6 * tendencies_3
