"""Summarize the observation noise sigmas across the generated test cases.

Reads every case*.json in a directory (this file's own directory by default),
pulls _args.noise_sigma_x and _args.noise_sigma_y out of each one, and reports
the per-case values along with the max and mean of each sigma.

Usage:
    python noise_stats.py [case_dir]
"""
import json
import os
import re
import sys


def case_sort_key(filename):
    """Sort case10.json after case9.json instead of after case1.json."""
    match = re.search(r'(\d+)', filename)
    return (int(match.group(1)) if match else -1, filename)


def load_sigmas(case_dir):
    """Return a list of (filename, sigma_x, sigma_y) for every case file.

    A sigma is None when the case file has no _args or is missing that key.
    """
    filenames = [f for f in os.listdir(case_dir)
                 if f.startswith('case') and f.endswith('.json')]
    filenames.sort(key=case_sort_key)

    sigmas = []
    for filename in filenames:
        with open(os.path.join(case_dir, filename)) as case_file:
            case = json.load(case_file)
        args = case.get('_args') or {}
        sigmas.append((filename,
                       args.get('noise_sigma_x'),
                       args.get('noise_sigma_y')))
    return sigmas


def summarize(values):
    """Return (max, mean) of the non-missing values, or (None, None)."""
    present = [v for v in values if v is not None]
    if not present:
        return None, None
    return max(present), sum(present) / len(present)


def main():
    case_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
        os.path.abspath(__file__))

    sigmas = load_sigmas(case_dir)
    if not sigmas:
        print('No case*.json files found in {}'.format(case_dir))
        return

    print('{:<16}{:>16}{:>16}'.format('case', 'noise_sigma_x', 'noise_sigma_y'))
    for filename, sigma_x, sigma_y in sigmas:
        print('{:<16}{:>16}{:>16}'.format(
            filename,
            'missing' if sigma_x is None else '{:g}'.format(sigma_x),
            'missing' if sigma_y is None else '{:g}'.format(sigma_y)))

    max_x, mean_x = summarize([s[1] for s in sigmas])
    max_y, mean_y = summarize([s[2] for s in sigmas])

    print('')
    print('{} case file(s)'.format(len(sigmas)))
    print('noise_sigma_x  max = {:g}  mean = {:g}'.format(max_x, mean_x))
    print('noise_sigma_y  max = {:g}  mean = {:g}'.format(max_y, mean_y))


if __name__ == '__main__':
    main()
