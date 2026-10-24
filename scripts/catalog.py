"""Validate archive metadata, build the catalog, or search it without dependencies."""
from pathlib import Path
from datetime import date
from urllib.parse import quote
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def load_catalog(root=ROOT):
    root = Path(root).resolve()
    data = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported catalog schema_version')
    entries = data.get('collections')
    if not isinstance(entries, list) or not entries:
        raise ValueError('collections must be a nonempty list')
    ids = set()
    for item in entries:
        for key in ('id', 'title', 'summary', 'kind', 'version', 'date', 'status', 'landing', 'provenance'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f'Missing/non-text collection field: {key}')
            if '\n' in item[key] or '|' in item[key]:
                raise ValueError(f'Catalog field contains unsupported newline or pipe: {key}')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item['id']):
            raise ValueError('Collection ID must be a lowercase slug')
        if item['id'] in ids:
            raise ValueError(f'Duplicate collection ID: {item["id"]}')
        ids.add(item['id'])
        date.fromisoformat(item['date'])
        topics = item.get('topics')
        if not isinstance(topics, list) or not topics or any(not isinstance(t, str) or not re.fullmatch(r'[A-Za-z0-9]+(?:[ -][A-Za-z0-9]+)*', t) for t in topics):
            raise ValueError('topics must contain simple nonempty topic names')
        if len({t.casefold() for t in topics}) != len(topics):
            raise ValueError('Duplicate topic in collection')
        def existing_file(value):
            if not isinstance(value, str) or not value or '\\' in value or Path(value).is_absolute():
                raise ValueError('Catalog path must be repository-relative')
            target = (root / value).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                raise ValueError(f'Missing or escaping catalog path: {value}')
            return target
        existing_file(item['landing'])
        existing_file(item['provenance'])
        artifacts = item.get('artifacts')
        if not isinstance(artifacts, list) or not artifacts:
            raise ValueError('Each collection needs an artifact')
        paths = set()
        for artifact in artifacts:
            for key in ('label', 'path', 'format', 'sha256'):
                if not isinstance(artifact.get(key), str) or not artifact[key].strip():
                    raise ValueError(f'Missing artifact field: {key}')
            if artifact['path'] in paths:
                raise ValueError('Duplicate artifact path in collection')
            paths.add(artifact['path'])
            target = existing_file(artifact['path'])
            if not re.fullmatch('[0-9a-f]{64}', artifact['sha256']):
                raise ValueError('Malformed artifact SHA-256')
            if hashlib.sha256(target.read_bytes()).hexdigest() != artifact['sha256']:
                raise ValueError(f'Artifact SHA-256 mismatch: {artifact["path"]}')
    return entries


def slug(text):
    return re.sub(r'[ -]+', '-', text.casefold())


def link(label, path):
    return f'[{label}]({quote(path, safe="/.-_")})'


def render_catalog(entries):
    entries = sorted(entries, key=lambda e: e['title'].casefold())
    topics = sorted({t for e in entries for t in e['topics']}, key=str.casefold)
    lines = [
        '# Catalog', '',
        'Browse original papers, project files, and supporting material published in **knowledge**.', '',
        '> Generated from `catalog.json`. Edit the metadata, then run `python scripts/catalog.py --write`.', '',
        '## Browse by topic', '',
        ' · '.join(f'[{t}](#{slug(t)})' for t in topics), '',
        '## All collections', '',
        '| Collection | Type | Edition | Status | Files |',
        '| --- | --- | --- | --- | --- |',
    ]
    for e in entries:
        files = ' · '.join(link(a['format'], a['path']) for a in e['artifacts'])
        lines.append(f'| {link(e["title"], e["landing"])} | {e["kind"]} | v{e["version"]} · {e["date"]} | {e["status"]} | {files} |')
    lines += ['', '## Collection summaries', '']
    for e in entries:
        lines += [f'### {e["title"]}', '', e['summary'], '', f'{link("Open collection", e["landing"])} · {link("Provenance", e["provenance"])}', '']
    lines += ['## Topic index', '']
    for topic in topics:
        lines += [f'### {topic}', '']
        for e in entries:
            if topic in e['topics']:
                lines.append(f'- {link(e["title"], e["landing"])} — {e["kind"]}; {e["status"].lower()}.')
        lines.append('')
    lines += ['## Status and reuse', '',
              'Status describes the artifact, not an endorsement of its claims. See each collection for authorship, review status, limitations, and citation details.', '',
              '[Add a collection](docs/ADDING_FILES.md) · [Verify files](scripts/README.md) · [Rights and permissions](RIGHTS.md)', '']
    return '\n'.join(lines)


def select(entries, query='', topic='', kind='', status=''):
    return [e for e in entries
            if (not query or query.casefold() in json.dumps(e, ensure_ascii=False).casefold())
            and (not topic or any(topic.casefold() == t.casefold() for t in e['topics']))
            and (not kind or kind.casefold() == e['kind'].casefold())
            and (not status or status.casefold() == e['status'].casefold())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='Regenerate CATALOG.md')
    mode.add_argument('--check', action='store_true', help='Fail if metadata or generated catalog is stale')
    parser.add_argument('--query', default='')
    parser.add_argument('--topic', default='')
    parser.add_argument('--type', dest='kind', default='')
    parser.add_argument('--status', default='')
    parser.add_argument('--json', action='store_true', help='Output selected records as JSON')
    args = parser.parse_args()
    try:
        entries = load_catalog()
        rendered = render_catalog(entries)
        if args.write:
            (ROOT / 'CATALOG.md').write_text(rendered, encoding='utf-8')
            print('Wrote CATALOG.md from catalog.json')
        elif args.check:
            if (ROOT / 'CATALOG.md').read_text(encoding='utf-8') != rendered:
                raise ValueError('CATALOG.md is stale; run python scripts/catalog.py --write')
            print(f'PASS: {len(entries)} collection(s), metadata, artifact digests, and generated catalog')
        else:
            chosen = select(entries, args.query, args.topic, args.kind, args.status)
            if args.json:
                print(json.dumps(chosen, indent=2, ensure_ascii=False))
            elif not chosen:
                print('No matching collections.')
            else:
                for e in chosen:
                    print(f'{e["id"]}: {e["title"]} | {e["kind"]} | v{e["version"]} | {e["status"]}\n  {e["landing"]}')
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
