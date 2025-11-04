# quantum_annealing_sim.py
"""
Quantum Annealing Simulation: Quadratic Assignment Problem (QAP)
Fixed version with proper variable unpacking
"""

from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler
import numpy as np
import re

def create_qap_bqm(distances, flows, penalty=50):
    """
    Create BQM for QAP using binary variables x[i,p] = 1 if facility i at location p
    """
    n = len(distances)
    bqm = BinaryQuadraticModel('BINARY')

    # Variables: x_{i,p} represented as string 'i_p'
    def var(i, p): return f"{i}_{p}"

    # Objective: sum_{i,j,p,q} flow[i][j] * dist[p][q] * x[i,p] * x[j,q]
    for i in range(n):
        for j in range(n):
            if i == j: continue
            for p in range(n):
                for q in range(n):
                    if p == q: continue
                    cost = flows[i][j] * distances[p][q]
                    bqm.add_quadratic(var(i, p), var(j, q), cost)

    # Constraint 1: Each facility to exactly one location
    for i in range(n):
        terms = [(var(i, p), 1.0) for p in range(n)]
        bqm.add_linear_equality_constraint(terms, constant=-1, lagrange_multiplier=penalty)

    # Constraint 2: Each location gets exactly one facility
    for p in range(n):
        terms = [(var(i, p), 1.0) for i in range(n)]
        bqm.add_linear_equality_constraint(terms, constant=-1, lagrange_multiplier=penalty)

    return bqm

def parse_solution(sample):
    """Convert sample dict with 'i_p' keys into assignment list"""
    assignment = {}
    pattern = re.compile(r"(\d+)_(\d+)")
    for var, val in sample.items():
        if val == 1:
            match = pattern.match(var)
            if match:
                i, p = int(match.group(1)), int(match.group(2))
                assignment[i] = p
    return assignment

# === Example: 3x3 QAP ===
D = np.array([[0, 1, 2],
              [1, 0, 3],
              [2, 3, 0]])  # Distances between locations

F = np.array([[0, 5, 2],
              [5, 0, 3],
              [2, 3, 0]])  # Flows between facilities

# Build and solve
bqm = create_qap_bqm(D, F, penalty=100)
sampler = SimulatedAnnealingSampler()
sampleset = sampler.sample(bqm, num_reads=1000)

best = sampleset.first
print(f"Best energy: {best.energy}")
print("Assignment (facility → location):")

assignment = parse_solution(best.sample)
for facility, location in sorted(assignment.items()):
    print(f"  Facility {facility} → Location {location}")

# Optional: validate constraints
print("\nValidation:")
for i in assignment:
    locs = [loc for f, loc in assignment.items() if f == i]
    print(f"  Facility {i}: assigned to 1 location → {len(locs) == 1}")

used_locs = list(assignment.values())
print(f"  All locations used once → {len(set(used_locs)) == len(used_locs)}")
