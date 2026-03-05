# STRATEGY DOMINANCE ANALYSER - BEGINNER
# Checks if any strategy is strictly dominated

players = ["Prisoner 1", "Prisoner 2"]
strategies = ["Cooperate", "Defect"]
payoff_matrix = {
    ("Cooperate", "Cooperate"): (-1, -1),
    ("Cooperate", "Defect"):    (-3,  0),
    ("Defect",    "Cooperate"): ( 0, -3),
    ("Defect",    "Defect"):    (-2, -2),
}

def display_game(players, strategies, payoff_matrix):
    print("\n"+"  "  + "=" * 60)
    print(f"{'STRATEGY DOMINANCE ANALYSER':^60}")
    print("  " + "=" * 60)
    print(f"\n{'':22}", end="")
    for s2 in strategies:
        print(f"{s2:>16} P2", end="")
    print()
    print("  " + "-" * 60)
    for s1 in strategies:
        print(f"P1  {s1:<20}", end="")
        for s2 in strategies:
            payoff = payoff_matrix[(s1, s2)]
            cell = f"({payoff[0]}, {payoff[1]})"
            print(f"{cell:>16}", end="")
        print()
    print("  " + "-" * 60)

def check_strict_dominance_p1(strategies, payoff_matrix):
    # Check if there is any one strategy that always gives strictly higher payoff than another
    # for Player 1, across ALL of Player 2's strategies
    print("\n  P1 STRICT DOMINANCE CHECK")
    print("  " + "-" * 60)
    dominated = []

    for s1 in strategies:
        for s1_other in strategies:
            if s1 == s1_other:
                continue   # skip comparing a strategy to itself

            # Check if s1_other strictly dominates s1
            # i.e. s1_other always gives MORE than s1 for every P2 strategy
            is_dominated = True
            for s2 in strategies:
                p1_payoff      = payoff_matrix[(s1,       s2)][0]
                p1_other_payoff = payoff_matrix[(s1_other, s2)][0]

                if p1_other_payoff <= p1_payoff:
                    # s1_other does NOT dominate s1 here
                    is_dominated = False
                    break   # no need to check further

            if is_dominated:
                dominated.append((s1, s1_other))
                print(f"  '{s1}' is STRICTLY DOMINATED by '{s1_other}' for {players[0]}")
                print(f"   Reason: '{s1_other}' always gives higher payoff than '{s1}'")

                # Show the comparison explicitly
                for s2 in strategies:
                    p1 = payoff_matrix[(s1, s2)][0]
                    p1o = payoff_matrix[(s1_other, s2)][0]
                    print(f"     vs P2='{s2}': {s1}={p1} vs {s1_other}={p1o} -> {s1_other} wins")

    if not dominated:
        print(f"  No strictly dominated strategies found for {players[0]}")

def check_strict_dominance_p2(strategies, payoff_matrix):
    print("\n  P2 STRICT DOMINANCE CHECK")
    print("  " + "-" * 60)
    dominated = []

    for s2 in strategies:
        for s2_other in strategies:
            if s2 == s2_other:
                continue

            is_dominated = True
            for s1 in strategies:
                p2_payoff       = payoff_matrix[(s1, s2)][1]
                p2_other_payoff = payoff_matrix[(s1, s2_other)][1]

                if p2_other_payoff <= p2_payoff:
                    is_dominated = False
                    break

            if is_dominated:
                dominated.append((s2, s2_other))
                print(f"  '{s2}' is STRICTLY DOMINATED by '{s2_other}' for {players[1]}")
                for s1 in strategies:
                    p2  = payoff_matrix[(s1, s2)][1]
                    p2o = payoff_matrix[(s1, s2_other)][1]
                    print(f"    vs P1='{s1}': {s2}={p2} vs {s2_other}={p2o} -> {s2_other} wins")

    if not dominated:
        print(f"  No strictly dominated strategies found for {players[1]}")

    print("  " + "=" * 60)


display_game(players, strategies, payoff_matrix)
check_strict_dominance_p1(strategies, payoff_matrix)
check_strict_dominance_p2(strategies, payoff_matrix)