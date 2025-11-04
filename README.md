# Quantum Annealing Simulation with D-Wave Ocean

**Simulate quantum annealing on a classical computer** using D-Wave’s open-source **Ocean SDK**.  
This repository solves a tiny **Quadratic Assignment Problem (QAP)** with **simulated annealing** – a perfect starting point for learning, teaching, or building a portfolio project.

---

## Why This Stack?

| Feature | Reason |
|---------|--------|
| **Python** | Easy syntax, huge scientific ecosystem |
| **D-Wave Ocean (`dimod`, `neal`)** | Industry-standard tools for formulating and sampling quadratic models |
| **Simulated Annealing (`neal`)** | Fast, high-quality classical analog of quantum annealing |
| **Seamless upgrade path** | Same code runs on real D-Wave quantum hardware (just add an API token) |

---

## Project Structure

```
.
├── quantum_annealing_sim.py   # Main script (fixed & robust)
├── requirements.txt           # Python dependencies
└── README.md                  # You are here
```

---

## Recommended Workflow – Use a Virtual Environment

Isolating dependencies guarantees the code works the same on any machine (your laptop, a CI runner, a colleague’s PC, etc.).

```bash
# 1. Clone the repo
git clone https://github.com/yourname/quantum-annealing-sim.git
cd quantum-annealing-sim

# 2. Create a clean virtual environment
python3 -m venv .venv

# 3. Activate it
#    macOS / Linux
source .venv/bin/activate
#    Windows PowerShell
# .venv\Scripts\Activate.ps1

# 4. Install dependencies inside the venv
pip install --upgrade pip
pip install -r requirements.txt
```

> **Never** install packages globally when sharing code. The `.venv` folder is git-ignored by default (add `*.venv` to `.gitignore` if you create one).

---

## Run the Example

```bash
python quantum_annealing_sim.py
```

**Sample output**

```
Best energy: 24.0
Assignment (facility → location):
  Facility 0 → Location 1
  Facility 1 → Location 2
  Facility 2 → Location 0

Validation:
  Facility 0: assigned to 1 location → True
  Facility 1: assigned to 1 location → True
  Facility 2: assigned to 1 location → True
  All locations used once → True
```

---

## Experiment & Extend

| Idea | One-liner change |
|------|------------------|
| **Tabu search** | `from dwave.tabu import TabuSampler; sampler = TabuSampler()` |
| **Exact solver (tiny problems)** | `from dimod import ExactSolver; sampler = ExactSolver()` |
| **Hybrid classical/quantum** | `from dwave.system import LeapHybridSampler` (needs D-Wave account) |
| **Larger QAP** | Replace `D` and `F` with bigger NumPy matrices |
| **Visualization** | Add `matplotlib` plots of energy vs. iteration |

Feel free to fork, add notebooks, or benchmark different samplers!

---

## Contributing

1. Fork → create a feature branch  
2. Keep the **virtual-env** workflow in your PR description  
3. Add tests (optional but welcome)  
4. Open a Pull Request  

---

*Happy annealing!*  
If you hit any snag, open an issue – the community (and the maintainer) will gladly help.
```

---
