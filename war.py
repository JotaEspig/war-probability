from random import randint
from typing import Dict, List, Tuple


RUNS_AMOUNT = 100_000;


def dice() -> int:
    return randint(1, 6)


def get_dice_results(amount: int) -> List[int]:
    r = list()
    for _ in range(amount):
        r.append(dice())
    r.sort(reverse=True)
    return r


def simulate_attack(a: int, b: int) -> Tuple[int, int]:
    attack = get_dice_results(a)
    defense = get_dice_results(b)

    len_min = min(len(attack), len(defense))
    attacker_wins = defenser_wins = i = 0
    last = 0
    while i < len_min:
        if attack[i] > defense[i]:
            attacker_wins += 1
            last = 1
        else:
            defenser_wins += 1
            last = 0

        i += 1

    if last:
        attacker_wins = len(attack) - defenser_wins
    else:
        defenser_wins = len(defense) - attacker_wins

    return (attacker_wins, defenser_wins)


def attack_with_against(atk: int, d: int) -> bool:
    while atk > 1 and d > 0:
        r = simulate_attack(min(atk, 3), min(d, 3))
        atk -= r[1]
        d -= r[0]

    return atk > d


def simple_attacks_statistics() -> Dict:
    results = dict()
    for i in range(1, 4):
        attacker = i
        for j in range(1, 4):
            defenser = j
            key = f"{i}{j}"
            for _ in range(RUNS_AMOUNT):
                prev = results.get(key)
                if prev == None:
                    prev = (0, 0)

                a_wins, d_wins = simulate_attack(attacker, defenser)
                results[key] = (prev[0] + a_wins, prev[1] + d_wins)

            r = results.get(key)
            if r == None:
                r = (0, 0)

            results[key] = (r[0] / (RUNS_AMOUNT), r[1] / (RUNS_AMOUNT))

    return results


def attack_with_against_statistics(atk: int, d: int) -> float:
    wins = 0
    for _ in range(RUNS_AMOUNT):
        wins += int(attack_with_against(atk, d))

    return wins / RUNS_AMOUNT


def print_simple_attacks_statistics():
    results = simple_attacks_statistics()
    for k in results.keys():
        beautiful_key = f"{k[0]}x{k[1]}"
        print(f"{beautiful_key}: {results[k]}")


if __name__ == "__main__":
    # just some tests
    print_simple_attacks_statistics()
    print(attack_with_against_statistics(130, 70))
