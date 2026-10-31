"""Verify the manifest export allowlist and all packaged bytes (stdlib only)."""
from pathlib import Path, PurePosixPath
import json
import sys
import tarfile

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "library.json").read_text(encoding="utf-8"))
expected = {p.relative_to(root).as_posix(): p.read_bytes()
            for pattern in manifest["export"]["include"]
            for p in root.glob(pattern) if p.is_file()}
assert expected, "Empty package allowlist"
with tarfile.open(sys.argv[1], "r:gz") as archive:
    actual = {}
    for member in archive.getmembers():
        if member.isdir():
            continue
        assert member.isfile(), f"Unexpected package entry: {member.name}"
        name = PurePosixPath(member.name).as_posix()
        while name.startswith("./"):
            name = name[2:]
        assert name not in actual, f"Duplicate entry: {name}"
        actual[name] = archive.extractfile(member).read()
assert actual.keys() == expected.keys(), (
    f"Extra: {actual.keys() - expected.keys()}; missing: {expected.keys() - actual.keys()}")
assert actual == expected, "Packaged bytes differ from allowlisted source"
print(f"Verified {len(actual)} allowlisted files; no development-only contents")
