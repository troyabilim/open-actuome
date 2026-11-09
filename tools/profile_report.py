#!/usr/bin/env python3
"""Create a provenance-labelled Markdown report from a valid local profile."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_actuome import load_json, validate_profile


def cell(value):
    if value is None:
        return 'Unknown'
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\n', ' ').replace('\r', ' ')


def make_report(profile):
    result = validate_profile(profile)
    if not result['valid']:
        raise ValueError('; '.join(result['errors']))
    lines = [f"# OpenActuome profile: {cell(profile['profile_id'])}", '',
             f"Data status: **{cell(profile['data_status'])}**. Coverage: **{cell(profile['coverage'])}**.",
             f"Described actuated DoF: {len(profile['axes'])} / {profile['platform']['total_actuated_dof']}.", '',
             'Structure and consistency passed. Physical measurements have NOT been independently verified.', '',
             '| Axis | Basis | Continuous effort | Peak / duration | Max speed | Median / p95 latency | Boundary |',
             '|---|---|---|---|---|---|---|']
    for axis in profile['axes']:
        limits, latency = axis['limits'], axis['latency']
        row = [axis['axis_id'], axis['evidence']['basis'],
               f"{cell(limits['continuous_effort'])} {axis['effort_unit']}",
               f"{cell(limits['peak_effort'])} {axis['effort_unit']} / {cell(limits['peak_duration_s'])} s",
               f"{cell(limits['max_velocity'])} {axis['velocity_unit']}",
               f"{cell(latency['median_ms'])} / {cell(latency['p95_ms'])} ms", latency['boundary']]
        lines.append('| ' + ' | '.join(cell(x) for x in row) + ' |')
    lines += ['', '## Evidence and conditions', '']
    for axis in profile['axes']:
        evidence = axis['evidence']
        lines += [f"### {cell(axis['axis_id'])}", '', f"Method: {cell(evidence['method'])}", '',
                  f"Sources: {cell(', '.join(evidence['source_refs']) or 'None')}", '',
                  f"Latency boundary: {cell(axis['latency']['boundary_detail'])}", '']
        for key, value in evidence['conditions'].items():
            lines.append(f"- {key}: {cell(value)}")
        lines.append('')
    lines += ['## Source registry', '']
    for source in profile['sources']:
        lines.append(f"- {cell(source['source_id'])}: {cell(source['title'])} — {cell(source['locator'])}")
    if not profile['sources']:
        lines.append('No sources supplied.')
    lines += ['', 'No aggregate score or cross-platform ranking is calculated.', '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        report = make_report(load_json(args.profile))
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding='utf-8', newline='\n')
        else:
            print(report)
    except (OSError, ValueError, OverflowError, RecursionError) as exc:
        print(f'Cannot export: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
