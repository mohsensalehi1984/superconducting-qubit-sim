# quantum_annealing_sim.py
"""
Quantum Annealing Simulation using D-Wave Ocean
Example: Solving a small Quadratic Assignment Problem (QAP)
"""

from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler
import numpy as np

def create_qap_bqm(facilities, locations):
    """
    Create BQM for Quadratic Assignment Problem
    facilities: distance matrix between facilities
    locations: flow matrix between locations
    """
    n = len(facilities)
    bqm = BinaryQuadraticModel('BINARY')

    # Linear terms (encourage one assignment per facility/location)
    for i in range(n):
        for p in range(n):
            var = (i, p)
            bqm.add_variable(var, 0)

    # Constraint: each facility assigned to exactly one location
    for i in range(n):
        bqm.add_linear_equality_constraint(
            [(f'f{i}_l{p}', 1.0) for p in range(n)], constant=-1, lagrange_multiplier=10
        )

    # Constraint: each location gets exactly one facility
    for p in range(n):
        bqm.add_linear_equality_constraint(
            [(f'f{i}_l{p}', 1.0) for i in range(n)], constant=-1, lagrange_multiplier=10
        )

    # Objective: minimize cost = sum flow[i][j] * distance[p][q] * x[i,p] * x[j,q]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for p in range(n):
                for q in range(n):
                    if p == q:
                        continue
                    cost = facilities[i][j] * locations[p][q]
                    bqm.add_quadratic(f'f{i}_l{p}', f'f{j}_l{q}', cost)

    return bqm

# Example: 3 facilities, 3 locations
D = np.array([[0, 1, 2],
              [1, 0, 3],
              [2, 3, 0]])  # Distance between facilities

F = np.array([[0, 5, 2],
              [5, 0, 3],
              [2, 3, 0]])  # Flow between locations

# Create BQM
bqm = create_qap_bqm(D, F)

# Use simulated annealing
sampler = SimulatedAnnealingSampler()
sampleset = sampler.sample(bqm, num_reads=1000)

# Get best solution
best = sampleset.first.sample
energy = sampleset.first.energy

print("Best energy:", energy)
print("Assignment (facility i -> location p):")
for (i, p), val in best.items():
    if val == 1:
        print(f"Facility {i} -> Location {p}")
