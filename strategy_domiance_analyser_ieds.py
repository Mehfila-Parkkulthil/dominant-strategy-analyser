# STRATEGY DOMINANCE ANALYSER 
# Checks strict AND weak dominance for both players
# + Iterated Elimination of Dominated Strategies (IEDS)

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

players = ["Prisoner 1", "Prisoner 2"]
strategies = ["Cooperate", "Defect"]
payoff_matrix = {
    ("Cooperate", "Cooperate"): (-1, -1),
    ("Cooperate", "Defect"):    (-3,  0),
    ("Defect",    "Cooperate"): ( 0, -3),
    ("Defect",    "Defect"):    (-2, -2),
}

def display_game(players, strategies, payoff_matrix):
    print("\n" + "=" * 60)
    print(f"{'STRATEGY DOMINANCE ANALYSER':^60}")
    print(" "+"=" * 60)
    print(f"\n{'':22}", end="")
    for s2 in strategies:
        print(f"{s2:>16}", end="")
    print()
    print("  " + "-" * 60)
    for s1 in strategies:
        print(f"  {s1:<20}", end="")
        for s2 in strategies:
            payoff = payoff_matrix[(s1, s2)]
            cell = f"({payoff[0]}, {payoff[1]})"
            print(f"{cell:>16}", end="")
        print()
    print("  " + "-" * 60)


def is_strictly_dominated_p1(s1, s1_other, active_s2, payoff_matrix):
    # Returns True if s1_other strictly dominates s1 for P1
    # Only checks against currently active P2 strategies
    for s2 in active_s2:
        if payoff_matrix[(s1_other, s2)][0] <= payoff_matrix[(s1, s2)][0]:
            return False
    return True

def is_weakly_dominated_p1(s1, s1_other, active_s2, payoff_matrix):
    # Returns True if s1_other weakly dominates s1 for P1
    # >= in all cases AND > in at least one case
    at_least_one_strict = False
    for s2 in active_s2:
        p1       = payoff_matrix[(s1,       s2)][0]
        p1_other = payoff_matrix[(s1_other, s2)][0]
        if p1_other < p1:
            return False   # s1_other is worse here, not even weakly dominant
        if p1_other > p1:
            at_least_one_strict = True
    return at_least_one_strict

def is_strictly_dominated_p2(s2, s2_other, active_s1, payoff_matrix):
    for s1 in active_s1:
        if payoff_matrix[(s1, s2_other)][1] <= payoff_matrix[(s1, s2)][1]:
            return False
    return True

def is_weakly_dominated_p2(s2, s2_other, active_s1, payoff_matrix):
    at_least_one_strict = False
    for s1 in active_s1:
        p2       = payoff_matrix[(s1, s2)][1]
        p2_other = payoff_matrix[(s1, s2_other)][1]
        if p2_other < p2:
            return False
        if p2_other > p2:
            at_least_one_strict = True
    return at_least_one_strict

def check_dominance(players, strategies, payoff_matrix):
    print("\n  FULL DOMINANCE ANALYSIS")
    print(" "+"-" * 60)

    for s1 in strategies:
        for s1_other in strategies:
            if s1 == s1_other:
                continue
            if is_strictly_dominated_p1(s1, s1_other, strategies, payoff_matrix):
                print(f"  {players[0]}: '{s1}' STRICTLY dominated by '{s1_other}'")
            elif is_weakly_dominated_p1(s1, s1_other, strategies, payoff_matrix):
                print(f"  {players[0]}: '{s1}' WEAKLY dominated by '{s1_other}'")

    for s2 in strategies:
        for s2_other in strategies:
            if s2 == s2_other:
                continue
            if is_strictly_dominated_p2(s2, s2_other, strategies, payoff_matrix):
                print(f"  {players[1]}: '{s2}' STRICTLY dominated by '{s2_other}'")
            elif is_weakly_dominated_p2(s2, s2_other, strategies, payoff_matrix):
                print(f"  {players[1]}: '{s2}' WEAKLY dominated by '{s2_other}'")

def iterated_elimination(players, strategies, payoff_matrix):
    # IEDS: keep removing strictly dominated strategies
    # until no more can be removed
    print("\n ITERATED ELIMINATION OF DOMINATED STRATEGIES (IEDS)")
    print(" " +"-"*60)

    # active strategies start as full list — we remove from these
    active_s1 = list(strategies)   # copy so we don't modify original
    active_s2 = list(strategies)

    round_num = 1
    eliminated = True

    while eliminated:
        eliminated = False
        print(f"\n  Round {round_num}:")
        print(f"    Active P1 strategies: {active_s1}")
        print(f"    Active P2 strategies: {active_s2}")

        # Check P1's strategies
        for s1 in list(active_s1):   # list() makes a copy to loop over safely
            for s1_other in active_s1:
                if s1 == s1_other:
                    continue
                if is_strictly_dominated_p1(s1, s1_other, active_s2, payoff_matrix):
                    print(f"    Eliminating P1's '{s1}' (dominated by '{s1_other}')")
                    active_s1.remove(s1)
                    eliminated = True
                    break

        # Check P2's strategies
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

    print(f"\n  Remaining after IEDS:")
    print(f"    {players[0]}: {active_s1}")
    print(f"    {players[1]}: {active_s2}")

    if len(active_s1) == 1 and len(active_s2) == 1:
        print(f"\n  So: ({active_s1[0]}, {active_s2[0]})")
        print(f"     This is the predicted rational outcome!")
    print(" "+"=" * 60)


display_game(players, strategies, payoff_matrix)
check_dominance(players, strategies, payoff_matrix)
iterated_elimination(players, strategies, payoff_matrix)