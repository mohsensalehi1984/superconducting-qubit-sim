# qubit_sim.py
import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
from scipy.constants import h, hbar

# ==============================
# Transmon Qubit Parameters
# ==============================

omega = 5.0 * 2 * np.pi  # Qubit frequency in GHz → rad/ns
alpha = -0.3 * 2 * np.pi  # Anharmonicity in GHz → rad/ns (negative!)
N = 5                     # Number of levels (transmon: weakly anharmonic)

# Operators
a = qt.destroy(N)
n = qt.num(N)

# Hamiltonian: Duffing oscillator model
H = omega * (a.dag() * a + 0.5) - (alpha / 2.0) * (a.dag() * a.dag() * a * a)

# ==============================
# Energy Levels
# ==============================

energies = H.eigenenergies()
print("Energy levels (GHz):")
for i, E in enumerate(energies[:3]):
    print(f"  |{i}⟩: {E / (2*np.pi):.3f} GHz")

# Transition frequency |0> → |1>
f01 = (energies[1] - energies[0]) / (2 * np.pi)
print(f"\nf01 = {f01:.3f} GHz")

# Anharmonicity: f12 - f01
f12 = (energies[2] - energies[1]) / (2 * np.pi)
anharm = f12 - f01
print(f"Anharmonicity = {anharm:.3f} GHz")

# ==============================
# Time Evolution: Rabi Drive
# ==============================

# Drive Hamiltonian: H_d = ε(t) (a + a†)
epsilon = 0.02 * 2 * np.pi  # Drive strength in GHz
omega_d = f01                # Resonant drive

# Time-dependent drive
def drive(t, args):
    return epsilon * np.cos(omega_d * t)

H_drive = [[a + a.dag(), drive]]

# Total Hamiltonian
H_total = [H, H_drive]

# Initial state |0>
psi0 = qt.basis(N, 0)

# Time array
tlist = np.linspace(0, 100, 1000)  # ns

# Solve dynamics
result = qt.mesolve(H_total, psi0, tlist, [], [n])

# ==============================
# Plotting
# ==============================

plt.figure(figsize=(10, 6))
plt.plot(tlist, result.expect[0], label="⟨n⟩")
plt.xlabel("Time (ns)")
plt.ylabel("⟨n⟩")
plt.title("Rabi Oscillations in Transmon Qubit")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("plots/rabi_oscillations.png")
plt.show()

# ==============================
# Quantum Gates
# ==============================

# X-gate via pi-pulse
T_pi = np.pi / (epsilon)  # Pi pulse duration
print(f"\nPi-pulse duration: {T_pi:.2f} ns")

# Apply X gate
times_gate = np.linspace(0, T_pi, 100)
result_x = qt.mesolve(H_total, psi0, times_gate, [], [qt.basis(N,0).proj(), qt.basis(N,1).proj()])

p0 = [res[0][0,0].real for res in result_x.expect]
p1 = [res[1][1,1].real for res in result_x.expect]

plt.figure(figsize=(8,5))
plt.plot(times_gate, p0, label="|0⟩")
plt.plot(times_gate, p1, label="|1⟩")
plt.xlabel("Time (ns)")
plt.ylabel("Population")
plt.title("X-Gate (π-pulse)")
plt.legend()
plt.grid()
plt.savefig("plots/x_gate.png")
plt.show()

# Bloch sphere visualization
b = qt.Bloch()
state_final = result_x.states[-1]
b.add_states(state_final.ptrace(0))  # Project to qubit subspace
b.show()
