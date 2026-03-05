# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

# ============================================================
# STRATEGY DOMINANCE ANALYSER - ADVANCED
# Adds: mixed strategy dominance check using numpy
# A pure strategy can be dominated by a MIXTURE of strategies
# ============================================================

players = ["Prisoner 1", "Prisoner 2"]
strategies = ["Cooperate", "Defect"]
payoff_matrix = {
    ("Cooperate", "Cooperate"): (-1, -1),
    ("Cooperate", "Defect"):    (-3,  0),
    ("Defect",    "Cooperate"): ( 0, -3),
    ("Defect",    "Defect"):    (-2, -2),
}

def build_matrices(strategies, payoff_matrix):
    n = len(strategies)
    p1_matrix = np.zeros((n, n), dtype=float)
    p2_matrix = np.zeros((n, n), dtype=float)
    for i, s1 in enumerate(strategies):
        for j, s2 in enumerate(strategies):
            p1_matrix[i][j] = payoff_matrix[(s1, s2)][0]
            p2_matrix[i][j] = payoff_matrix[(s1, s2)][1]
    return p1_matrix, p2_matrix

def display_game(players, strategies, payoff_matrix):
    print("\n" + "=" * 55)
    print("      STRATEGY DOMINANCE ANALYSER - ADVANCED")
    print("=" * 55)
    print(f"\n{'':22}", end="")
    for s2 in strategies:
        print(f"{s2:>16}", end="")
    print()
    print("  " + "-" * 52)
    for s1 in strategies:
        print(f"  {s1:<20}", end="")
        for s2 in strategies:
            payoff = payoff_matrix[(s1, s2)]
            cell = f"({payoff[0]}, {payoff[1]})"
            print(f"{cell:>16}", end="")
        print()
    print("  " + "-" * 52)
    print("=" * 55)

def is_strictly_dominated_p1(s1, s1_other, active_s2, payoff_matrix):
    for s2 in active_s2:
        if payoff_matrix[(s1_other, s2)][0] <= payoff_matrix[(s1, s2)][0]:
            return False
    return True

def is_strictly_dominated_p2(s2, s2_other, active_s1, payoff_matrix):
    for s1 in active_s1:
        if payoff_matrix[(s1, s2_other)][1] <= payoff_matrix[(s1, s2)][1]:
            return False
    return True

def check_mixed_dominance_p1(strategies, payoff_matrix):
    # Check if a pure strategy is dominated by a MIXTURE of other strategies
    # For each strategy s1, we try all probability combos (p, 1-p)
    # over the OTHER strategies and see if any mixture always beats s1
    p1_matrix, _ = build_matrices(strategies, payoff_matrix)
    n = len(strategies)
    print("\n P1 MIXED STRATEGY DOMINANCE CHECK")
    print("-" * 55)

    for i, s1 in enumerate(strategies):
        dominated_by_mix = False
        # Try probabilities in steps of 0.01 from 0 to 1
        # np.arange(0, 1.01, 0.01) → [0.0, 0.01, 0.02, ..., 1.0]
        for p in np.arange(0, 1.01, 0.01):
            # Mix between the OTHER two strategies (for 2x2 game)
            other_indices = [j for j in range(n) if j != i]
            if len(other_indices) < 1:
                continue

            # For 2 strategies: mixture is p * s_other[0] + (1-p) * s_other[1]
            # For simplicity in 2x2: just one other strategy, p=1 means full weight
            j = other_indices[0]

            # Expected payoff of mixture vs each of P2's strategies
            mix_beats_s1 = True
            for k in range(n):
                mix_payoff = p * p1_matrix[j][k]   # weighted payoff of other strategy
                s1_payoff  = p1_matrix[i][k]
                if mix_payoff <= s1_payoff:
                    mix_beats_s1 = False
                    break

            if mix_beats_s1:
                dominated_by_mix = True
                print(f"  '{s1}' is dominated by a mixture (p={round(p,2)}) of other strategies")
                break

        if not dominated_by_mix:
            print(f"  '{s1}' is NOT dominated by any mixture")

def iterated_elimination(players, strategies, payoff_matrix):
    print("\n ITERATED ELIMINATION (IEDS)")
    print("-" * 55)
    active_s1 = list(strategies)
    active_s2 = list(strategies)
    round_num = 1
    eliminated = True

    while eliminated:
        eliminated = False
        print(f"\n  Round {round_num}:")
        print(f"    Active P1: {active_s1}  |  Active P2: {active_s2}")

        for s1 in list(active_s1):
            for s1_other in active_s1:
                if s1 == s1_other:
                    continue
                if is_strictly_dominated_p1(s1, s1_other, active_s2, payoff_matrix):
                    print(f"    Eliminating P1's '{s1}' (dominated by '{s1_other}')")
                    active_s1.remove(s1)
                    eliminated = True
                    break

        for s2 in list(active_s2):
            for s2_other in active_s2:
                if s2 == s2_other:
                    continue
                if is_strictly_dominated_p2(s2, s2_other, active_s1, payoff_matrix):
                    print(f"    Eliminating P2's '{s2}' (dominated by '{s2_other}')")
                    active_s2.remove(s2)
                    eliminated = True
                    break

        round_num += 1

    print(f"\n  Final remaining strategies:")
    print(f"    {players[0]}: {active_s1}")
    print(f"    {players[1]}: {active_s2}")
    if len(active_s1) == 1 and len(active_s2) == 1:
        print(f"\n  ** Rational outcome: ({active_s1[0]}, {active_s2[0]})")
    print("=" * 55)

if __name__ == "__main__":
    display_game(players, strategies, payoff_matrix)
    check_mixed_dominance_p1(strategies, payoff_matrix)
    iterated_elimination(players, strategies, payoff_matrix)
    print("\n Advanced dominance analyser complete!\n")