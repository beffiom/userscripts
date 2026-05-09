#!/usr/bin/env python3
"""
clean_srt.py — Fix YouTube auto-generated SRT subtitle overlap.

YouTube auto-captions give each cue an end time that extends past the next
cue's start time. This causes two cues to display simultaneously — the old
line stays on screen while the new line appears above it, and the old line
only disappears one cue later.

The fix is simple: trim each cue's end time to the next cue's start time.
This makes cues non-overlapping so only one line displays at a time.

Also drops zero/negative-duration cues that result from the trimming.

Usage: python3 clean_srt.py <file.srt> [file2.srt ...]
Edits files in-place.
"""

import sys
import re


def tc_to_ms(tc: str) -> int:
    tc = tc.strip().replace(',', '.')
    h, m, s = tc.split(':')
    return int((int(h) * 3600 + int(m) * 60 + float(s)) * 1000)


def ms_to_tc(ms: int) -> str:
    h  = ms // 3_600_000; ms %= 3_600_000
    m  = ms //    60_000; ms %=    60_000
    s  = ms //     1_000; ms %=     1_000
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def parse_srt(text: str):
    entries = []
    for block in re.split(r'\n\n+', text.strip()):
        lines = block.strip().splitlines()
        tc_idx = next((i for i, l in enumerate(lines) if '-->' in l), None)
        if tc_idx is None:
            continue
        try:
            start_s, end_s = [t.strip() for t in lines[tc_idx].split('-->')]
        except ValueError:
            continue
        body = '\n'.join(lines[tc_idx + 1:]).strip()
        if body:
            entries.append((start_s, end_s, body))
    return entries


def clean(entries):
    if not entries:
        return entries

    cleaned = []
    for i, (start, end, text) in enumerate(entries):
        s_ms = tc_to_ms(start)
        e_ms = tc_to_ms(end)

        # Trim end time to next cue's start time to eliminate overlap.
        # This is the core fix for the YouTube double-line display bug.
        if i + 1 < len(entries):
            next_start_ms = tc_to_ms(entries[i + 1][0])
            e_ms = min(e_ms, next_start_ms)

        # Drop cues that became zero or negative duration after trimming
        if e_ms <= s_ms:
            continue

        cleaned.append((ms_to_tc(s_ms), ms_to_tc(e_ms), text))

    return cleaned


def write_srt(entries) -> str:
    blocks = []
    for idx, (start, end, text) in enumerate(entries, 1):
        blocks.append(f'{idx}\n{start} --> {end}\n{text}')
    return '\n\n'.join(blocks) + '\n'


def process(path: str):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()

    entries = parse_srt(raw)
    if not entries:
        print(f'  {path}: no cues found, skipping.')
        return

    original_count = len(entries)
    cleaned = clean(entries)
    removed = original_count - len(cleaned)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(write_srt(cleaned))

    name = path.split('/')[-1]
    print(f'  Cleaned {name}: {original_count} -> {len(cleaned)} cues ({removed} dropped)')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <file.srt> [file2.srt ...]')
        sys.exit(1)
    for path in sys.argv[1:]:
        process(path)
