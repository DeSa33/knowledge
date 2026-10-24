"""Check archive metadata, generated files, text, and local documentation links."""

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

import catalog

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'README.md', 'CATALOG.md', 'catalog.json', 'AGENTS.md', 'CONTRIBUTING.md',
    'RIGHTS.md', 'docs/README.md', 'docs/MAP.md',
    '.github/workflows/repository-checks.yml',
)
TEXT_SUFFIXES = {'.md', '.py', '.yml', '.yaml', '.json', '.svg'}
SKIP_DIRS = {'.git', '.venv', 'venv', '__pycache__'}


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.anchors = [], set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if not value:
                continue
            if key in {'href', 'src'}:
                self.links.append(value)
            if key == 'id' or (tag == 'a' and key == 'name'):
                self.anchors.add(value)


def without_code(text, keep_inline=False):
    """Exclude fenced examples and inline code from link interpretation."""
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if fence:
            lines.append('')
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1]:
                fence = None
        elif match:
            fence = (match[1][0], len(match[1]))
            lines.append('')
        else:
            lines.append(line)
    return re.sub(r'(`+)(.+?)\1', r'\2' if keep_inline else '', '\n'.join(lines))


def destination(text, start):
    """Read an inline link destination, including balanced filename parentheses."""
    pos = start
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos < len(text) and text[pos] == '<':
        end = text.find('>', pos + 1)
        return text[pos + 1:end] if end >= 0 else ''
    begin, depth = pos, 0
    while pos < len(text):
        char = text[pos]
        if char == '\\':
            pos += 2
            continue
        if char == '(':
            depth += 1
        elif char == ')':
            if depth == 0:
                return text[begin:pos]
            depth -= 1
        elif char.isspace() and depth == 0:
            return text[begin:pos]
        pos += 1
    return ''


def markdown_links(text):
    definitions = {}
    for match in re.finditer(r'^\s{0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))', text, re.M):
        definitions[' '.join(match[1].casefold().split())] = match[2] or match[3]
    text = re.sub(r'^\s{0,3}\[[^\]]+\]:.*$', '', text, flags=re.M)
    links = list(definitions.values())
    for match in re.finditer(r'!?\[([^\]\n]*)\]', text):
        rest = text[match.end():]
        if rest.startswith('('):
            target = destination(text, match.end() + 1)
            if target:
                links.append(target)
        else:
            ref = re.match(r'^\[([^\]]*)\]', rest)
            key = (ref[1] or match[1]) if ref else match[1]
            key = ' '.join(key.casefold().split())
            if key in definitions:
                links.append(definitions[key])
    return links


def heading_slug(text):
    text = re.sub(r'(?<!\w)(?:\*{1,3}|_{1,3})(.+?)(?:\*{1,3}|_{1,3})(?!\w)', r'\1', text)
    text = re.sub(r'!?\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = unescape(re.sub(r'<[^>]*>', '', text)).strip().lower()
    text = ''.join(c for c in text if c in {'-', '_'} or not unicodedata.category(c).startswith(('P', 'S')))
    return re.sub(r'\s', '-', text)


def section_anchors(text):
    clean = without_code(text, keep_inline=True)
    parser = HTMLLinks()
    parser.feed(clean)
    anchors, seen = set(parser.anchors), {}
    lines = clean.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$', line)
        title = match[1] if match else None
        if title is None and index and re.fullmatch(r'\s{0,3}(?:=+|-+)\s*', line) and lines[index - 1].strip():
            title = lines[index - 1].strip()
        if title is not None:
            base = heading_slug(title)
            count = seen.get(base, 0)
            anchor = f'{base}-{count}' if count else base
            while anchor in anchors:
                count += 1
                anchor = f'{base}-{count}'
            seen[base] = count + 1
            anchors.add(anchor)
    return anchors


def check_links(root, path, text):
    root = Path(root).resolve()
    clean = without_code(text)
    parser = HTMLLinks()
    parser.feed(clean)
    errors, count = [], 0
    targets = markdown_links(clean) + parser.links
    for raw in targets:
        target = unescape(re.sub(r'\\([()\[\] ])', r'\1', raw))
        try:
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            count += 1
            if url.path.startswith('/') or '\\' in url.path:
                raise ValueError('use a repository-relative URL with forward slashes')
            dest = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
            if not dest.is_relative_to(root):
                raise ValueError('destination escapes the repository')
            if dest.is_dir():
                # GitHub opens directory links; validate a fragment against its README.
                if not url.fragment:
                    continue
                dest = dest / 'README.md'
            relative = dest.relative_to(root).as_posix()
            catalog.local_file(root, relative)
            fragment = unquote(url.fragment)
            if fragment and dest.suffix.lower() in {'.md', '.html', '.htm', '.svg'}:
                source = dest.read_text(encoding='utf-8')
                if fragment not in section_anchors(source):
                    raise ValueError(f'no section or ID #{fragment}')
        except (ValueError, OSError) as exc:
            errors.append(f'{path.relative_to(root)}: {raw}: {exc}')
    return errors, count


def verify(root=ROOT):
    root = Path(root).resolve()
    errors, checked_links = [], 0
    for name in REQUIRED:
        try:
            path = catalog.local_file(root, name)
            if path.stat().st_size == 0:
                errors.append(f'Empty required file: {name}')
        except ValueError as exc:
            errors.append(str(exc))
    try:
        entries = catalog.load_catalog(root)
        for name in catalog.check_outputs(root, entries):
            errors.append(f'Stale generated file: {name}; run python scripts/catalog.py --write')
    except (ValueError, TypeError, KeyError, OSError) as exc:
        errors.append(f'Catalog: {exc}')
    for path in sorted(root.rglob('*')):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts) or not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            if not path.resolve().is_relative_to(root):
                errors.append(f'File escapes repository: {path.relative_to(root)}')
                continue
            text = path.read_text(encoding='utf-8')
            if path.suffix.lower() == '.md':
                found, count = check_links(root, path, text)
                errors.extend(found)
                checked_links += count
        except (ValueError, OSError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    return errors, checked_links


def main():
    errors, links = verify()
    if errors:
        for error in errors:
            print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'PASS: catalog, generated indexes, artifact SHA-256, UTF-8 text, and {links} local links including Markdown/HTML sections')
    print('Scope: repository consistency and file integrity; external URLs and research claims are not verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
