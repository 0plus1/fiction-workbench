#!/usr/bin/env python3
"""Check literal prose constraints. Exit 1 for hard matches, 2 for input errors."""
import argparse
import json
from pathlib import Path
import re
from repetition_scan import prose_paragraphs


def load_profile(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    required = {'name', 'hard', 'review'}
    if (not isinstance(data, dict) or not required <= set(data)
            or set(data) - required - {'metadata'}):
        raise ValueError('Profile must contain name, hard and review, with optional metadata.')
    if 'metadata' in data and not isinstance(data['metadata'], dict):
        raise ValueError('Profile metadata must be an object.')
    if not isinstance(data['name'], str) or not data['name'].strip():
        raise ValueError('Profile name must be a nonempty string.')
    seen = set()
    for mode in ('hard', 'review'):
        if not isinstance(data[mode], list):
            raise ValueError(f'{mode} must be an array of literal strings.')
        for term in data[mode]:
            if not isinstance(term, str) or not term.strip():
                raise ValueError(f'{mode} entries must be nonempty strings.')
            key = ' '.join(term.casefold().replace('’', "'").split())
            if key in seen:
                raise ValueError(f'Duplicate constraint: {term}')
            seen.add(key)
    return data


def pattern(term):
    # Literal matching: flexible whitespace and apostrophe style, no user regex.
    parts = []
    for part in term.strip().split():
        escaped = re.escape(part.replace('’', "'"))
        parts.append(escaped.replace("'", "['’]"))
    return re.compile(r'(?<!\w)' + r'\s+'.join(parts) + r'(?!\w)', re.IGNORECASE)


def check(path, profile):
    compiled = [(mode, term, pattern(term)) for mode in ('hard', 'review')
                for term in profile[mode]]
    matches = []
    for group in prose_paragraphs(path.read_text(encoding='utf-8')):
        paragraph = '\n'.join(line for _, line in group)
        for mode, term, regex in compiled:
            for match in regex.finditer(paragraph):
                line = group[paragraph[:match.start()].count('\n')][0]
                matches.append({'mode': mode, 'term': term, 'line': line,
                                'paragraph_start_line': group[0][0],
                                'paragraph_end_line': group[-1][0],
                                'matched_text': match.group()})
    matches.sort(key=lambda item: (item['line'], item['term']))
    return {'path': str(path.resolve()), 'profile': profile['name'],
            'hard_matches': sum(m['mode'] == 'hard' for m in matches),
            'review_matches': sum(m['mode'] == 'review' for m in matches),
            'matches': matches,
            'notice': 'Literal constraints only; no probability control or prose-quality verdict. Input unchanged.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path)
    parser.add_argument('--profile', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = check(args.target, load_profile(args.profile))
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f'Cannot check constraints: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if result['hard_matches'] else 0)


if __name__ == '__main__':
    main()
