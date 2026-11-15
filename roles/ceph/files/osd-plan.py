import json
from pathlib import Path
import subprocess
import sys

def read_json(*argv):
    return json.loads(subprocess.check_output(argv, text=True))

fsid, *paths = sys.argv[1:]
osds = read_json("ceph-volume", "lvm", "list", "--format", "json")
new_devices = []
existing_ids = []
seen = set()
for path in paths:
    device = Path(path)
    if device.parent != Path("/dev/disk/by-id") or not device.is_symlink():
        sys.exit(f"Use a persistent /dev/disk/by-id symlink: {path}")
    real = device.resolve(strict=True)
    if real in seen:
        sys.exit(f"Duplicate OSD device: {path}")
    seen.add(real)
    disk, = read_json("lsblk", "--json", "--paths", "--output",
                      "NAME,TYPE,MOUNTPOINTS", str(real))["blockdevices"]
    if disk["type"] != "disk":
        sys.exit(f"OSD target is not a whole disk: {path}")
    matches = [
        (int(osd_id), volume["tags"])
        for osd_id, volumes in osds.items()
        for volume in volumes
        if volume["type"] == "block"
        and real in (Path(name).resolve() for name in volume["devices"])
    ]
    if matches:
        if len(matches) != 1 or matches[0][1]["ceph.cluster_fsid"] != fsid:
            sys.exit(f"OSD device has foreign or ambiguous Ceph metadata: {path}")
        existing_ids.append(matches[0][0])
        continue
    signatures = read_json("wipefs", "--no-act", "--json", str(real))["signatures"]
    if signatures or disk.get("children") or any(disk["mountpoints"] or []):
        sys.exit(f"Refusing to provision a nonempty OSD device: {path}")
    new_devices.append(str(real))
print(json.dumps({"create": new_devices, "existing_ids": existing_ids}))
