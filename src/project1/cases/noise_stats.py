"""Summarize the observation noise and arena size across the generated test cases.

Reads every case*.json in a directory (this file's own directory by default),
pulls the following fields out of each case's _args, and reports the per-case
values along with a summary across all cases:
    noise_sigma_x, noise_sigma_y    max and mean
    arena_x_bounds, arena_y_bounds  overall range, plus the range of each end

Usage:
    python noise_stats.py [case_dir]
"""
import json
import os
import re
import sys

SIGMA_KEYS = ('noise_sigma_x', 'noise_sigma_y')
BOUNDS_KEYS = ('arena_x_bounds', 'arena_y_bounds')


def case_sort_key(filename):
    """Sort case10.json after case9.json instead of after case1.json."""
    match = re.search(r'(\d+)', filename)
    return (int(match.group(1)) if match else -1, filename)


def load_cases(case_dir):
    """Return a list of (filename, args) for every case file.

    args is the case's _args dict, or an empty dict if the case has none, so a
    missing field reads as None via args.get().
    """
    filenames = [f for f in os.listdir(case_dir)
                 if f.startswith('case') and f.endswith('.json')]
    filenames.sort(key=case_sort_key)

    cases = []
    for filename in filenames:
        with open(os.path.join(case_dir, filename)) as case_file:
            case = json.load(case_file)
        cases.append((filename, case.get('_args') or {}))
    return cases


def summarize_sigmas(values):
    """Return (max, mean) of the non-missing values, or (None, None)."""
    present = [v for v in values if v is not None]
    if not present:
        return None, None
    return max(present), sum(present) / len(present)


def summarize_bounds(bounds):
    """Return (overall, lowers, uppers) for a list of [lower, upper] bounds.

    Each is a [min, max] pair: overall runs from the smallest lower to the
    largest upper (the span every case fits inside), while lowers and uppers
    are the range each end of the bounds takes. Missing bounds are skipped; if
    all of them are missing, all three are None.
    """
    present = [b for b in bounds if b is not None]
    if not present:
        return None, None, None
    lowers = [b[0] for b in present]
    uppers = [b[1] for b in present]
    return ([min(lowers), max(uppers)],
            [min(lowers), max(lowers)],
            [min(uppers), max(uppers)])


def format_value(value):
    """Format a number or a [lower, upper] pair; None reads as 'missing'."""
    if value is None:
        return 'missing'
    if isinstance(value, (list, tuple)):
        return '[{}]'.format(', '.join('{:g}'.format(v) for v in value))
    return '{:g}'.format(value)


def main():
    case_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
        os.path.abspath(__file__))

    cases = load_cases(case_dir)
    if not cases:
        print('No case*.json files found in {}'.format(case_dir))
        return

    keys = SIGMA_KEYS + BOUNDS_KEYS
    row = '{:<14}' + '{:>16}' * len(keys)
    print(row.format('case', *keys))
    for filename, args in cases:
        print(row.format(filename, *(format_value(args.get(k)) for k in keys)))

    print('')
    print('{} case file(s)'.format(len(cases)))
    for key in SIGMA_KEYS:
        max_value, mean_value = summarize_sigmas(
            [a.get(key) for _, a in cases])
        print('{:<16}max = {}  mean = {}'.format(
            key, format_value(max_value), format_value(mean_value)))
    for key in BOUNDS_KEYS:
        overall, lowers, uppers = summarize_bounds(
            [a.get(key) for _, a in cases])
        print('{:<16}range = {}  lower in {}  upper in {}'.format(
            key, format_value(overall), format_value(lowers),
            format_value(uppers)))


if __name__ == '__main__':
    main()
