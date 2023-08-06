"""
Wavefunction simulator device
=============================

**Module name:** :mod:`pennylane_forest.wavefunction`

.. currentmodule:: pennylane_forest.wavefunction

This module contains the :class:`~.WavefunctionDevice` class, a PennyLane device that allows
evaluation and differentiation of Rigetti's WavefunctionSimulator using PennyLane.


Auxiliary functions
-------------------

.. autosummary::
    spectral_decomposition_qubit


Classes
-------

.. autosummary::
   WavefunctionDevice

Code details
~~~~~~~~~~~~
"""
import itertools

import numpy as np
from numpy.linalg import eigh

from pyquil.api import WavefunctionSimulator

from .device import ForestDevice
from ._version import __version__


I = np.identity(2)
X = np.array([[0, 1], [1, 0]])  #: Pauli-X matrix
Y = np.array([[0, -1j], [1j, 0]])  #: Pauli-Y matrix
Z = np.array([[1, 0], [0, -1]])  #: Pauli-Z matrix
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # Hadamard matrix


observable_map = {"PauliX": X, "PauliY": Y, "PauliZ": Z, "Identity": I, "Hadamard": H}


class WavefunctionDevice(ForestDevice):
    r"""Wavefunction simulator device for PennyLane.

    Args:
        wires (int): the number of qubits to initialize the device in
        shots (int): Number of circuit evaluations/random samples used
            to estimate expectation values of observables.

    Keyword args:
        forest_url (str): the Forest URL server. Can also be set by
            the environment variable ``FOREST_SERVER_URL``, or in the ``~/.qcs_config``
            configuration file. Default value is ``"https://forest-server.qcs.rigetti.com"``.
        qvm_url (str): the QVM server URL. Can also be set by the environment
            variable ``QVM_URL``, or in the ``~/.forest_config`` configuration file.
            Default value is ``"http://127.0.0.1:5000"``.
        compiler_url (str): the compiler server URL. Can also be set by the environment
            variable ``COMPILER_URL``, or in the ``~/.forest_config`` configuration file.
            Default value is ``"http://127.0.0.1:6000"``.
    """
    name = "Forest Wavefunction Simulator Device"
    short_name = "forest.wavefunction"

    observables = {"PauliX", "PauliY", "PauliZ", "Hadamard", "Hermitian", "Identity"}

    def __init__(self, wires, *, shots=1000, analytic=True, **kwargs):
        super().__init__(wires, shots, analytic, **kwargs)
        self.qc = WavefunctionSimulator(connection=self.connection)
        self.state = None

    def pre_measure(self):
        self.state = self.qc.wavefunction(self.prog).amplitudes

        # pyQuil uses the convention that the first qubit is the least significant
        # qubit. Here, we reverse this to make it the last qubit, matching PennyLane convention.
        self.state = self.state.reshape([2] * len(self.active_wires)).T.flatten()
        self.expand_state()

    def expand_state(self):
        """The pyQuil wavefunction simulator initializes qubits dymnically as they are requested.
        This method expands the state to the full number of wires in the device."""

        if len(self.active_wires) == self.num_wires:
            # all wires in the device have been initialised
            return

        # there are some wires in the device that have not yet been initialised
        inactive_wires = set(range(self.num_wires)) - self.active_wires

        # place the inactive subsystems in the vacuum state
        other_subsystems = np.zeros([2 ** len(inactive_wires)])
        other_subsystems[0] = 1

        # expand the state of the device into a length-num_wire state vector
        expanded_state = np.kron(self.state, other_subsystems).reshape([2] * self.num_wires)
        expanded_state = np.moveaxis(
            expanded_state, range(len(self.active_wires)), self.active_wires
        )
        expanded_state = expanded_state.flatten()

        self.state = expanded_state

    def expval(self, observable, wires, par):
        if observable == "Hermitian":
            A = par[0]
        else:
            A = observable_map[observable]

        if self.analytic:
            # exact expectation value
            ev = self.ev(A, wires)
        else:
            # estimate the ev
            ev = np.mean(self.sample(observable, wires, par))

        return ev

    def var(self, observable, wires, par):
        if observable == "Hermitian":
            A = par[0]
        else:
            A = observable_map[observable]

        if self.analytic:
            # exact variance value
            var = self.ev(A @ A, wires) - self.ev(A, wires)**2
        else:
            # estimate the variance
            var = np.var(self.sample(observable, wires, par))

        return var

    def sample(self, observable, wires, par):
        n = self.shots

        if observable == "Hermitian":
            A = par[0]
        else:
            A = observable_map[observable]

        # Calculate the probability p of observing
        # eigenvalue a for the observable A.
        a, P = self.spectral_decomposition(A)

        p = np.zeros(a.shape)

        for idx, Pi in enumerate(P):
            p[idx] = self.ev(Pi, wires)

        # randomly sample from the eigenvalues of A
        # according to the computed probabilities
        return np.random.choice(a, n, p=p)

    def ev(self, A, wires):
        r"""Evaluates an expectation in the current state.

        Args:
          A (array): :math:`2^N\times 2^N` Hermitian matrix corresponding to the expectation
          wires (Sequence[int]): target subsystem

        Returns:
          float: expectation value :math:`\left\langle{A}\right\rangle = \left\langle{\psi}\mid A\mid{\psi}\right\rangle`
        """
        # Expand the Hermitian observable over the entire subsystem
        As = self.mat_vec_product(A, self.state, wires)
        return np.vdot(self.state, As).real

    @staticmethod
    def spectral_decomposition(A):
        r"""Spectral decomposition of a Hermitian matrix.

        Args:
            A (array): Hermitian matrix

        Returns:
            (vector[float], list[array[complex]]): (a, P): eigenvalues and Hermitian projectors
                such that :math:`A = \sum_k a_k P_k`.
        """
        d, v = eigh(A)
        P = []
        for k in range(d.shape[0]):
            temp = v[:, k]
            P.append(np.outer(temp, temp.conj()))
        return d, P
