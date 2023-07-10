from time import sleep

import contest_api as ca


def do_submit_solution(problem_id, contents, debug=False):
    ca.make_post("submission", {},
                 {'problem_id': problem_id, 'contents': contents})
    if debug:
        from time import sleep
        sleep(1)
        get_all_submissions(problem_id)


if __name__ == "__main__":
    do_submit_solution(51, '{"placements": [{"x": 1737.6871337890625, "y": 1172.0}, {"x": 567.16748046875, "y": 1172.0}], "volumes": [10, 10]}')

