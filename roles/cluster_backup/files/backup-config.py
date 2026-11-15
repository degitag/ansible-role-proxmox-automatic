import hashlib
import io
import json
import os
from pathlib import Path
import sqlite3
import stat
import sys
import tarfile
import tempfile

REQUIRED_FILES = (
    "var/lib/pve-cluster/config.db",
    "etc/corosync/authkey",
    "etc/network/interfaces",
    "etc/hosts",
)
OPTIONAL_FILES = ("etc/hostname", "etc/pve-thunderbolt.json", "etc/network/interfaces.d/sdn")


def integrity(database):
    with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
        if connection.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise ValueError("pmxcfs SQLite integrity check failed")
        if not connection.execute("SELECT 1 FROM tree WHERE name='corosync.conf'").fetchone():
            raise ValueError("pmxcfs snapshot has no Corosync configuration")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(archive, cluster, node, work):
    metadata = archive.lstat()
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != 0 or metadata.st_mode & 0o077:
        raise ValueError("Backup must be a root-owned private regular file")
    with tarfile.open(archive, "r:gz") as bundle:
        entries = bundle.getmembers()
        names = {entry.name for entry in entries}
        if len(names) != len(entries) or not all(entry.isfile() for entry in entries):
            raise ValueError("Archive contains non-regular or duplicate entries")
        if not set(REQUIRED_FILES) | {"manifest.json"} <= names:
            raise ValueError("Backup is missing required configuration")
        if names - set(REQUIRED_FILES) - set(OPTIONAL_FILES) - {"manifest.json"}:
            raise ValueError("Archive contains unexpected entries")
        manifest = json.load(bundle.extractfile("manifest.json"))
        if manifest["cluster"] != cluster or manifest["node"] != node:
            raise ValueError("Archive belongs to a different cluster or node")
        for name in names - {"manifest.json"}:
            data = bundle.extractfile(name).read()
            if digest(data) != manifest["sha256"][name]:
                raise ValueError(f"Archive checksum failed for {name}")
            if name == REQUIRED_FILES[0]:
                db = work / "verified.db"
                db.write_bytes(data)
                integrity(db)


def create(archive, cluster, node, work):
    snapshot = work / "snapshot.db"
    source = Path("/") / REQUIRED_FILES[0]
    with sqlite3.connect(source.as_uri() + "?mode=ro", uri=True) as live, sqlite3.connect(snapshot) as backup:
        live.backup(backup)
    integrity(snapshot)
    content = {REQUIRED_FILES[0]: snapshot.read_bytes()}
    for name in REQUIRED_FILES[1:] + OPTIONAL_FILES:
        path = Path("/") / name
        if name in REQUIRED_FILES or path.is_file():
            content[name] = path.read_bytes()
    manifest = {"cluster": cluster, "node": node, "sha256": {name: digest(data) for name, data in content.items()}}
    content["manifest.json"] = json.dumps(manifest).encode()
    prepared = work / "archive.tar.gz"
    with tarfile.open(prepared, "w:gz") as bundle:
        for name, data in content.items():
            entry = tarfile.TarInfo(name)
            entry.size = len(data)
            entry.mode = 0o600
            bundle.addfile(entry, io.BytesIO(data))
    verify(prepared, cluster, node, work)
    os.link(prepared, archive)


def main():
    action, name, cluster, node = sys.argv[1:]
    archive = Path(name)
    if not archive.is_absolute() or archive.parent.is_symlink():
        raise ValueError("Backup path must reside in an absolute, private directory")
    os.umask(0o077)
    if action == "create":
        archive.parent.mkdir(mode=0o700, exist_ok=True)
    directory = archive.parent.stat()
    if directory.st_uid != 0 or directory.st_mode & 0o077:
        raise ValueError("The backup directory must be root-owned and private")
    created = action == "create" and not archive.exists()
    with tempfile.TemporaryDirectory(prefix=".pve-config-", dir=archive.parent) as name:
        work = Path(name)
        if created:
            create(archive, cluster, node, work)
        else:
            verify(archive, cluster, node, work)
    print(json.dumps({"archive": str(archive), "cluster": cluster, "node": node, "created": created,
                      "sqlite_integrity": "ok"}))


if __name__ == "__main__":
    main()
