# Superconducting Qubit Simulator (Transmon)

A Python project to simulate a **transmon superconducting qubit** using the **quantum Hamiltonian** and **QuTiP**.

## Features
- Define transmon Hamiltonian
- Compute energy levels
- Simulate time evolution (Rabi oscillations)
- Apply quantum gates (X, Hadamard)
- Visualize Bloch sphere & population dynamics

## Requirements
```bash
pip install -r requirements.txt
```

## Usage
```bash
python qubit_sim.py
```

Or explore interactively:
```bash
jupyter notebook notebooks/Transmon_Simulation.ipynb
```

## Physics
The transmon is modeled as a weakly anharmonic oscillator:

$$
\hat{H} = 4E_C (\hat{n} - n_g)^2 - E_J \cos(\hat{\phi})
$$

Approximated in the phase basis or truncated charge basis.

We use the **Duffing oscillator approximation**:

$$
\hat{H} \approx \hbar \omega_q (\hat{a}^\dagger \hat{a} + \frac{1}{2}) - \frac{\alpha}{2} \hat{a}^\dagger \hat{a}^\dagger \hat{a} \hat{a}
$$

where:
- $\omega_q$: qubit frequency
- $\alpha$: anharmonicity (~ -200 MHz)

---

Made with ❤️ for quantum computing enthusiasts.

---

## Output (Example)

```
Energy levels (GHz):
  |0⟩: 0.000 GHz
  |1⟩: 5.000 GHz
  |2⟩: 9.700 GHz

f01 = 5.000 GHz
Anharmonicity = -0.300 GHz

Pi-pulse duration: 25.00 ns
```

Generates:
- `plots/rabi_oscillations.png`
- `plots/x_gate.png`
- Bloch sphere

---

## Future Extensions

- Add readout (cavity coupling)
- Add noise (T1, T2)
- Control pulses with DRAG
- Multi-qubit coupling
- Export to OpenQASM

---

Enjoy simulating **quantum superconductors**! ⚛️
