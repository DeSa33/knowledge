"""Verify research-repository packaging; no mathematical claims are tested."""

from pathlib import Path
import hashlib
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PDF = "BroadSematnicGenralzation(BSG).pdf"
REQUIRED = (
    PDF, "README.md", "CATALOG.md", "docs/ADDING_FILES.md", "docs/bsg/README.md", "docs/bsg/MAP.md", "PROJECT_MAP.md", "AGENTS.md", "CONTRIBUTING.md",
    "CITATION.cff", "CHANGELOG.md", "RIGHTS.md", "SECURITY.md",
    "CODE_OF_CONDUCT.md", "SHA256SUMS", "docs/README.md", "docs/MAP.md",
    "docs/bsg/PROBLEM_INDEX.md", "docs/bsg/EVALUATION.md", "docs/bsg/PROVENANCE.md",
    "docs/bsg/ROADMAP.md", "scripts/README.md", "scripts/MAP.md",
    ".github/ISSUE_TEMPLATE/research_review.yml",
    ".github/ISSUE_TEMPLATE/experiment.yml",
    ".github/pull_request_template.md", ".github/CODEOWNERS",
    ".github/workflows/repository-checks.yml",
)


def verify(root=ROOT):
    root = Path(root).resolve()
    errors = []
    for name in REQUIRED:
        path = root / name
        if not path.is_file() or not path.stat().st_size:
            errors.append(f"Missing or empty required file: {name}")

    manifest = root / "SHA256SUMS"
    recorded = set()
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if not match:
                errors.append(f"Malformed checksum entry: {line}")
                continue
            digest, name = match.groups()
            path = (root / name).resolve()
            if not path.is_relative_to(root) or Path(name).is_absolute():
                errors.append(f"Checksum path escapes repository: {name}")
                continue
            if name in recorded:
                errors.append(f"Duplicate checksum entry: {name}")
            recorded.add(name)
            if not path.is_file():
                errors.append(f"Checksummed file missing: {name}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f"Checksum mismatch: {name}")
    if PDF not in recorded:
        errors.append("Canonical PDF missing from checksum manifest")
    pdf = root / PDF
    if pdf.is_file() and not pdf.read_bytes().startswith(b"%PDF-"):
        errors.append("Canonical manuscript has no PDF header")

    checked_links = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.relative_to(root).parts:
            continue
        if path.suffix not in {".md", ".py", ".yml", ".cff"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"Invalid UTF-8: {path.relative_to(root)}")
            continue
        if path.suffix != ".md":
            continue
        # Repository Markdown uses inline links with URL-encoded parentheses.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            checked_links += 1
            if not dest.is_relative_to(root) or not dest.exists():
                errors.append(f"Broken local link in {path.relative_to(root)}: {target}")

    cff = root / "CITATION.cff"
    if cff.is_file():
        text = cff.read_text(encoding="utf-8")
        for field in ("cff-version:", "message:", "title:", "authors:", "repository-code:"):
            if not re.search(rf"^{re.escape(field)}", text, re.M):
                errors.append(f"Citation field missing: {field}")
    for name in ("research_review.yml", "experiment.yml"):
        path = root / ".github" / "ISSUE_TEMPLATE" / name
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for field in ("name:", "description:", "body:"):
                if not re.search(rf"^{field}", text, re.M):
                    errors.append(f"Issue form {name} missing {field}")
            ids = re.findall(r"^\s+id: (\S+)", text, re.M)
            if len(ids) != len(set(ids)):
                errors.append(f"Duplicate field IDs in {name}")
    return errors, checked_links


def main():
    errors, links = verify()
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(REQUIRED)} required files, {links} local links, UTF-8 text, metadata essentials, and PDF SHA-256")
    print("Scope: repository packaging only; mathematical claims and experiments are not verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
