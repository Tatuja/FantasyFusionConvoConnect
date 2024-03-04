import csv
import itertools
import random
import sys
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class Person:
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


def parse_csv(path) -> tuple[list[Person], set[str]]:
    with open(path, newline='') as input_file:
        csvreader = csv.reader(input_file, delimiter=',')
        header = next(csvreader)
        names_pool = header[1:]
        persons = []
        for row in csvreader:
            name = row[0]

            preferences = {}
            for idx, rating in enumerate(row[1:]):
                rated_name = names_pool[idx]
                if rated_name == name:
                    continue
                else:
                    preferences[rated_name] = int(rating)

            persons.append(Person(name, preferences))
        return persons, set(names_pool)


def pairing(persons):
    matched_persons = itertools.combinations(persons, 2)
    matched_pairs = (MatchedPair.new(a, b) for a, b in matched_persons)
    matched_pairs_sorted = sorted(matched_pairs, key=lambda x: (-x.score, x.names))
    return matched_pairs_sorted


def create_round(matched_pairs_sorted, original_pool: set[str]):
    pool = original_pool.copy()
    new_round = []
    iteration = 0
    max_iteration = 3 * len(pool)
    while len(new_round) < len(original_pool) // 2 and iteration < max_iteration:
        if len(pairs) < len(original_pool) // 2:
            last_round = pairs.copy()
            pairs.clear()
            return last_round
        ignored = None
        if new_round and pairs:
            ignored = new_round.pop(random.randrange(0, len(new_round)))
            pool.add(ignored.names[0])
            pool.add(ignored.names[1])
        for pair in (pair for pair in matched_pairs_sorted if
                     pair != ignored):
            a, b = pair.names
            if a in pool and b in pool:
                new_round.append(pair)
                pool.remove(a)
                pool.remove(b)
            if not pool:
                break
        iteration += 1
    round_cleaner(matched_pairs_sorted, new_round)
    return new_round


def round_cleaner(matched_pairs_sorted, a_round):
    for pair in a_round:
        matched_pairs_sorted.remove(pair)


if __name__ == '__main__':
    try:
        persons, pool = parse_csv(sys.argv[1])
        no = int(sys.argv[2])
    except:
        print('Wrong parameters.')
        print('Expected csv file path and number of round, eg:\n    ./matcher.py path/data.csv 5')
        exit(-1)

    pairs = pairing(persons)

    for n in range(no):
        x = create_round(pairs, pool)
        print(f'Round {n+1}')
        for pair in x:
            print(f'{pair.names[0]} - {pair.names[1]}, score: {pair.score}')
        print('')
