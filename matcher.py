from dataclasses import dataclass
from typing import Dict, Tuple
import itertools


@dataclass
class Person:
    # NAMES: ClassVar[List[str]] = ['A', 'B', 'C', 'D', 'E', 'F']

    # A: ClassVar[Dict[str, int]] = {'B': 2, 'C': 9, 'D' : 10, 'E': 0, 'F': 5}

    name: str
    preferences: Dict[str, int]


@dataclass(order=True)
class MatchedPair:
    score: int
    names: Tuple[str, str]

    @staticmethod
    def new(person1: Person, person2: Person):
        name1 = person1.name
        name2 = person2.name

        score1 = person2.preferences.get(name1, 0)
        score2 = person1.preferences.get(name2, 0)

        result = score1 * score2 + (score1 + score2)

        return MatchedPair(score=result, names=tuple(sorted((name1, name2))))  # type: ignore


def pairing(persons):
    matched_persons = itertools.combinations(persons, 2)
    matched_pairs = (MatchedPair.new(a, b) for a, b in matched_persons)
    matched_pairs_sorted = sorted(matched_pairs, key=lambda x: (-x.score, x.names))
    return matched_pairs_sorted


def pooling(persons):
    pool = set(x.name for x in persons)
    return pool


def create_round(matched_pairs_sorted, original_pool: set[str]):
    pool = original_pool.copy()
    new_round = []
    ignored_matches = []
    while len(new_round) < len(original_pool) // 2:
        if new_round:
            ignored = new_round.pop(0)
            ignored_matches.append(ignored.names)
            pool.add(ignored.names[0])
            pool.add(ignored.names[1])
        for pair in (pair for pair in matched_pairs_sorted if pair.names not in ignored_matches):
            a, b = pair.names
            if a in pool and b in pool:
                new_round.append(pair)
                pool.remove(a)
                pool.remove(b)
            if not pool:
                break
    round_cleaner(matched_pairs_sorted, new_round)
    return new_round


def round_cleaner(matched_pairs_sorted, a_round):
    for pair in a_round:
        matched_pairs_sorted.remove(pair)


if __name__ == '__main__':
    persons = [
        Person('A', {'B': 2, 'C': 1, 'D': 3, 'E': 4, 'F': 5}),
        # Dla litery B
        Person('B', {'A': 3, 'C': 1, 'D': 4, 'E': 2, 'F': 5}),

        # Dla litery C
        Person('C', {'A': 5, 'B': 2, 'D': 1, 'E': 4, 'F': 3}),

        # Dla litery D
        Person('D', {'A': 4, 'B': 2, 'C': 5, 'E': 4, 'F': 4}),

        # Dla litery E
        Person('E', {'A': 4, 'B': 2, 'C': 5, 'D': 1, 'F': 3}),

        # Dla litery F
        Person('F', {'A': 4, 'B': 2, 'C': 5, 'D': 1, 'E': 4})
    ]

    # todo
    # poprawić generowanie persons

    pairs = pairing(persons)
    pool = pooling(persons)
    no = 6

    for n in range(no):
        x = create_round(pairs, pool)
        print(x)

    # print(pairs)
    # print(pool)
    # print(create_round(pairs, pool))
