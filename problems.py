import contest_api as ca

import glob

PROBLEMS_DIR = "./problems"
FORCE_UPDATE = False


def get_problems_count():
    problems = ca.make_get("problems")
    import json
    res = json.loads(problems)
    return res['number_of_problems']


remote_count = get_problems_count()
print(f"Found {remote_count} problems using API")

local_count = len(glob.glob(f"{PROBLEMS_DIR}/*.json"))
print(f"Found {local_count} problems at local directory {PROBLEMS_DIR}")

if FORCE_UPDATE or local_count != remote_count:
    print("Updating local problems, please wait...")
    for i in range(remote_count):
        data = ca.make_cdn_get(f"problems/{i + 1}.json")
        open(f"./problems/{i + 1}.json", "wb").write(data)
        print(f"Problem {i + 1} updated!")
