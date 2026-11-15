import ipaddress
import json
import subprocess
import sys

public, replication = map(ipaddress.IPv6Network, sys.argv[1:3])
public_address, replication_address = map(ipaddress.IPv6Address, sys.argv[3:5])
if public.overlaps(replication):
    sys.exit("Ceph public and replication networks overlap")
interfaces = json.loads(subprocess.check_output(["ip", "-j", "address", "show", "up"]))
local = {
    ipaddress.IPv6Address(address["local"])
    for interface in interfaces
    for address in interface.get("addr_info", [])
    if address["family"] == "inet6" and not address.get("tentative")
}
for network, address in ((public, public_address), (replication, replication_address)):
    if address not in network or address not in local:
        sys.exit(f"Ceph address {address} is not active locally in {network}")
