import math
from dataclasses import dataclass

from model import parse_input

import matplotlib.pyplot as plt
import numpy as np

# plt.hist(x)
# plt.show()

@dataclass
class ProblemStats:
    amm: int
    density: float
    pillars: int
    problem_id: int
    score: float


def get_stats():
    pid2stats = {}
    ps = []
    amms = []
    ds = []
    total_filtered_a = 0
    total_filtered_p = 0
    for i in range(90):
        room = parse_input(f"./problems/{i+1}.json")
        a = len(room.attendees)
        m = len(room.musicians)
        p = len(room.pillars)
        total_filtered_a += room.filtered_attendees()
        total_filtered_p += room.filtered_pillars()

        amm = a * m * m
        amms.append(amm)
        density = (m * math.pi * 100) / (room.stage.width * room.stage.height)
        ds.append(density)
        stats = ProblemStats(amm, density, len(room.pillars), i + 1, 0)
        ps.append(stats)
        pid2stats[i+1] = stats

    print(f"Statistics: attendees filtered={total_filtered_a}, pillars filtered={total_filtered_p}")

    print(f"amm-sorted list: {[p.problem_id for p in sorted(ps, key=lambda p: p.amm)]}")
    print(f"density-sorted list: {[p.problem_id for p in sorted(ps, key=lambda p: p.density)]}")
    print(f"pillars-sorted list: {[p.problem_id for p in sorted(ps, key=lambda p: p.pillars)]}")

    print(f"amm-sorted list[no pillars]: {[p.problem_id for p in sorted(filter(lambda p: p.pillars == 0, ps), key=lambda p: p.amm)]}")
    print(f"amm-sorted list[with pillars]: {[p.problem_id for p in sorted(filter(lambda p: p.pillars > 0, ps), key=lambda p: p.amm)]}")
    return pid2stats


if __name__ == "__main__":
    get_stats()

    # plt.hist(ds, bins=12)
    # plt.show()
