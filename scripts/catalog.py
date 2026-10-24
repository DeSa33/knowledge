"""Validate collection metadata, generate indexes, and search this archive."""

import argparse
from datetime import date
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- catalog:start -->'
END = '<!-- catalog:end -->'
COLLECTION_KEYS = {
    'id', 'title', 'subtitle', 'summary', 'kind', 'version', 'date', 'status',
    'topics', 'landing', 'provenance', 'artifacts',
}
ARTIFACT_KEYS = {'label', 'path', 'format', 'sha256', 'pages'}


def digest_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def local_file(root, value, allow_directory=False):
    """Resolve exact-case POSIX paths consistently on Linux and Windows."""
    if not isinstance(value, str) or not value or any(c in value for c in '\\:#?\r\n\x00'):
        raise ValueError(f'Invalid repository-relative path: {value!r}')
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {'', '.', '..'} for p in value.split('/')):
        raise ValueError(f'Invalid repository-relative path: {value!r}')
    target = Path(root).resolve()
    for part in path.parts:
        if not target.is_dir() or part not in {p.name for p in target.iterdir()}:
            raise ValueError(f'Missing file or wrong filename case: {value}')
        target = target / part
    allowed_type = target.is_file() or (allow_directory and target.is_dir())
    if not target.resolve().is_relative_to(Path(root).resolve()) or not allowed_type:
        raise ValueError(f'Missing or escaping file: {value}')
    return target


def text_field(record, key, where):
    value = record.get(key)
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError(f'{where}.{key}: expected nonempty text without outer whitespace')
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError(f'{where}.{key}: control characters are not allowed')
    return value


def topic_anchor(topic):
    words = topic.casefold().replace('+', ' plus ').replace('#', ' sharp ')
    return 'topic-' + re.sub(r'[^\w]+', '-', words, flags=re.UNICODE).strip('-')


def load_catalog(root=ROOT):
    root = Path(root).resolve()
    data = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
    if not isinstance(data, dict) or set(data) != {'schema_version', 'collections'}:
        raise ValueError('catalog.json must contain schema_version and collections only')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('schema_version must be the integer 1')
    entries = data['collections']
    if not isinstance(entries, list):
        raise ValueError('collections must be a list')
    ids, anchors = set(), {}
    for index, item in enumerate(entries):
        where = f'collections[{index}]'
        if not isinstance(item, dict) or set(item) - COLLECTION_KEYS:
            raise ValueError(f'{where}: expected an object with known collection fields')
        for key in ('id', 'title', 'summary', 'kind', 'status', 'landing', 'provenance'):
            text_field(item, key, where)
        if 'subtitle' in item:
            text_field(item, 'subtitle', where)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item['id']):
            raise ValueError(f'{where}.id: use a lowercase slug')
        if item['id'] in ids:
            raise ValueError(f'Duplicate collection ID: {item["id"]}')
        ids.add(item['id'])
        for key in ('date', 'version'):
            if key not in item:
                raise ValueError(f'{where}.{key}: supply a value or null if unknown')
            if item[key] is not None:
                text_field(item, key, where)
        if item['date'] is not None:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['date']):
                raise ValueError(f'{where}.date: use YYYY-MM-DD or null')
            date.fromisoformat(item['date'])
        topics = item.get('topics')
        if not isinstance(topics, list) or not topics:
            raise ValueError(f'{where}.topics: expected a nonempty list')
        seen_topics = set()
        for topic in topics:
            text_field({'topic': topic}, 'topic', where)
            anchor = topic_anchor(topic)
            if anchor == 'topic-':
                raise ValueError(f'{where}.topics: topic needs letters or digits')
            if topic.casefold() in seen_topics:
                raise ValueError(f'{where}.topics: duplicate topic {topic!r}')
            seen_topics.add(topic.casefold())
            if anchor in anchors and anchors[anchor] != topic.casefold():
                raise ValueError(f'Topic anchor collision: {topic!r}; use distinct topic names')
            anchors[anchor] = topic.casefold()
        local_file(root, item['landing'])
        local_file(root, item['provenance'])
        artifacts = item.get('artifacts')
        if not isinstance(artifacts, list) or not artifacts:
            raise ValueError(f'{where}.artifacts: expected a nonempty list')
        seen_paths = set()
        for number, artifact in enumerate(artifacts):
            location = f'{where}.artifacts[{number}]'
            if not isinstance(artifact, dict) or set(artifact) - ARTIFACT_KEYS:
                raise ValueError(f'{location}: expected an object with known artifact fields')
            for key in ('label', 'path', 'format', 'sha256'):
                text_field(artifact, key, location)
            target = local_file(root, artifact['path'])
            if artifact['path'] in seen_paths:
                raise ValueError(f'{location}: duplicate artifact path')
            seen_paths.add(artifact['path'])
            if 'pages' in artifact and (type(artifact['pages']) is not int or artifact['pages'] < 1):
                raise ValueError(f'{location}.pages: expected a positive integer')
            if not re.fullmatch(r'[0-9a-f]{64}', artifact['sha256']):
                raise ValueError(f'{location}.sha256: expected 64 lowercase hexadecimal characters')
            if digest_file(target) != artifact['sha256']:
                raise ValueError(f'Artifact SHA-256 mismatch: {artifact["path"]}; inspect the file before updating metadata')
            if artifact['format'].casefold() == 'pdf':
                with target.open('rb') as stream:
                    if stream.read(5) != b'%PDF-':
                        raise ValueError(f'{location}: declared PDF has no PDF header')
    return sorted(entries, key=lambda item: (item['title'].casefold(), item['id']))


def markdown(text):
    escaped = html.escape(text, quote=False)
    return re.sub(r'([\\`*_{\[\]}|])', r'\\\1', escaped)


def link(label, path):
    return f'[{markdown(label)}]({quote(path, safe="/.-_")})'


def edition(item):
    version = f'v{item["version"]}' if item['version'] is not None else 'Unversioned'
    return version + (f' · {item["date"]}' if item['date'] is not None else ' · Date not recorded')


def topics_for(entries):
    topics = {}
    for item in entries:
        for topic in sorted(item['topics'], key=lambda t: (t.casefold(), t)):
            topics.setdefault(topic.casefold(), topic)
    return sorted(topics.values(), key=str.casefold)


def render_featured(entries):
    if not entries:
        return 'No files have been published yet.\n'
    lines = ['| Paper or project | Edition | Files |', '| --- | --- | --- |']
    for item in entries:
        files = ' · '.join(link(a['label'], a['path']) for a in item['artifacts'])
        lines.append(f'| **{link(item["title"], item["landing"])}** | {markdown(edition(item))}<br>{markdown(item["status"])} | {files} |')
    lines += ['', '[All my work](CATALOG.md) · Browse by topic: ' + ' · '.join(
        f'[{markdown(t)}](CATALOG.md#{quote(topic_anchor(t))})' for t in topics_for(entries))]
    return '\n'.join(lines) + '\n'


def render_catalog(entries):
    lines = ['# Catalog', '', 'My papers, project files, and supporting material. [Back to the repo](README.md).', '',
             '<!-- Generated from catalog.json with python scripts/catalog.py --write. -->', '']
    if not entries:
        return '\n'.join(lines + ['No collections have been published yet.', ''])
    lines += ['## Collections', '']
    for item in entries:
        lines += [f'<a id="collection-{item["id"]}"></a>', f'### {markdown(item["title"])}', '',
                  markdown(item['summary']), '',
                  f'**{markdown(item["kind"])} · {markdown(edition(item))} · {markdown(item["status"])}**', '',
                  link('Project page', item['landing']) + ' · ' + ' · '.join(link(a['label'], a['path']) for a in item['artifacts']) + ' · ' + link('Provenance', item['provenance']), '']
    lines += ['## Topics', '']
    for topic in topics_for(entries):
        lines += [f'<a id="{topic_anchor(topic)}"></a>', f'### {markdown(topic)}', '']
        for item in entries:
            if any(topic.casefold() == t.casefold() for t in item['topics']):
                lines.append('- ' + link(item['title'], item['landing']))
        lines.append('')
    lines += ['[Working with the files](docs/README.md) · [Rights and permissions](RIGHTS.md)', '']
    return '\n'.join(lines)


def generated_files(root, entries):
    root = Path(root)
    readme = (root / 'README.md').read_text(encoding='utf-8')
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) >= readme.index(END):
        raise ValueError('README.md must contain one ordered catalog:start / catalog:end marker pair')
    before, rest = readme.split(START)
    _, after = rest.split(END)
    hashes = {}
    for item in entries:
        for artifact in item['artifacts']:
            hashes[artifact['path']] = artifact['sha256']
    sums = ''.join(f'{hashes[path]}  {path}\n' for path in sorted(hashes))
    return {
        'README.md': before + START + '\n' + render_featured(entries) + END + after,
        'CATALOG.md': render_catalog(entries),
        'SHA256SUMS': sums,
    }


def check_outputs(root, entries):
    stale = []
    for name, expected in generated_files(root, entries).items():
        path = Path(root) / name
        if not path.is_file() or path.read_text(encoding='utf-8') != expected:
            stale.append(name)
    return stale


def select(entries, query='', topic='', kind='', status=''):
    return [item for item in entries
            if (not query or query.casefold() in json.dumps(item, ensure_ascii=False).casefold())
            and (not topic or any(topic.casefold() == t.casefold() for t in item['topics']))
            and (not kind or kind.casefold() == item['kind'].casefold())
            and (not status or status.casefold() == item['status'].casefold())]


def main(argv=None, root=ROOT):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--write', action='store_true', help='Regenerate the catalog, checksum manifest, and README collection block')
    modes.add_argument('--check', action='store_true', help='Check metadata, hashes, and generated outputs')
    parser.add_argument('--query', default='')
    parser.add_argument('--topic', default='')
    parser.add_argument('--type', dest='kind', default='')
    parser.add_argument('--status', default='')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if (args.write or args.check) and (args.query or args.topic or args.kind or args.status or args.json):
        parser.error('Search filters and --json cannot be combined with --write or --check')
    try:
        entries = load_catalog(root)
        if args.write:
            outputs = generated_files(root, entries)
            for name, content in outputs.items():
                with (Path(root) / name).open('w', encoding='utf-8', newline='\n') as stream:
                    stream.write(content)
            print('Updated CATALOG.md, SHA256SUMS, and the README collection block')
        elif args.check:
            stale = check_outputs(root, entries)
            if stale:
                raise ValueError('Stale output: ' + ', '.join(stale) + '; run python scripts/catalog.py --write')
            print(f'PASS: {len(entries)} collection(s), artifact hashes, and generated indexes')
        else:
            chosen = select(entries, args.query, args.topic, args.kind, args.status)
            if args.json:
                print(json.dumps(chosen, indent=2, ensure_ascii=False))
            elif not chosen:
                print('No matching collections.')
            else:
                for item in chosen:
                    print(f'{item["id"]}: {item["title"]} | {edition(item)} | {item["status"]}\n  {item["landing"]}')
        return 0
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
