from dataclasses import dataclass

import contest_api as ca
from check_size import get_stats

from collections import defaultdict



def get_all_submissions(problem_id=None):
    args = {"offset": 0, "limit": 1000}
    if problem_id is not None:
        args['problem_id'] = problem_id
    subm = ca.make_get("submissions", args)
    import json
    res = json.loads(subm)
    if 'Failure' in res:
        print(f"Failed: {res['Failure']}")
        return
    print(f"You have {len(res['Success'])} submissions, graaatz!")

    scores = defaultdict(float)
    for s in res['Success']:
        if 'Success' in s['score']:
            scores[s['problem_id']] = max(scores[s['problem_id']], s['score']['Success'])
    for s in res['Success'][0:15]:
        print(s)

    total_score = 0.0
    for score in scores.values():
        total_score += score
    print(f">> Total score: {total_score}")

    print(f"Problems solved={len(scores.keys())}, ids={sorted(scores.keys())}")

    prev = None
    me = None
    for i, user in enumerate(json.loads(ca.make_get("scoreboard"))['scoreboard']):
        if 'Thelamon' in user['username']:
            me = user
            print(f"index={i-1}, need to win: {prev['score'] - user['score']}")
            print(f"index={i}, {user}. To next user: {round((prev['score'] - user['score']) / user['score'] * 100.0, 3)}%")
            break
        prev = user
    for s in res['Success'][0:5]:
        if 'Success' not in s['score']:
            continue
        print(f"[problem_id={s['problem_id']}] Added percent={round(s['score']['Success'] / me['score'] * 100.0, 4)}%")

    pid2stats = get_stats()
    for pid, stats in pid2stats.items():
        stats.score = scores[pid]

    import pprint
    pprint.pprint(sorted(pid2stats.values(), key=lambda st: st.score))

if __name__ == "__main__":
    get_all_submissions()