import ipaddress
import json
from pathlib import Path
import subprocess
import sys


def ip_json(*args):
    return json.loads(subprocess.check_output(["ip", "-j", *args], text=True))


def require(test, message):
    if not test:
        sys.exit(message)


config = json.loads(sys.argv[1])
management = config["management"]
port = management["interface"]
bridge = config["bridge"]
bond = config["bond"]
vids = set()
for spec in config["bridge_vids"].split():
    bounds = [int(vid) for vid in spec.split("-")]
    require(2 <= bounds[0] <= bounds[-1] <= 4094, f"Invalid bridge VLAN range: {spec}")
    vids.update(range(bounds[0], bounds[-1] + 1))
addresses = {
    port: [ipaddress.IPv4Interface(management["ipv4"]), ipaddress.IPv6Interface(management["ipv6"])]
}
gateways = {
    4: ipaddress.IPv4Address(management["ipv4_gateway"]),
    6: ipaddress.IPv6Address(management["ipv6_gateway"]),
}
for address in addresses[port]:
    gateway = gateways[address.version]
    require(gateway in address.network or gateway.is_link_local,
            f"Gateway {gateway} is outside {address.network}")
for vlan in config["vlans"]:
    require(vlan["id"] in vids, f"VLAN {vlan['id']} is not permitted on {bridge}")
    name = f"{bridge}.{vlan['id']}"
    require(len(name) <= 15, f"VLAN interface name is too long: {name}")
    addresses[name] = [ipaddress.IPv6Interface(vlan["ipv6"])]
for name in [port, *config["ports"]]:
    require((Path("/sys/class/net") / name).is_dir(), f"Physical interface missing: {name}")

if sys.argv[2] == "runtime":
    interfaces = {row["ifname"]: row for row in ip_json("address", "show", "up") if "ifname" in row}
    for name, expected in addresses.items():
        live = interfaces.get(name, {}).get("addr_info", [])
        observed = {ipaddress.ip_interface(f"{row['local']}/{row['prefixlen']}")
                    for row in live if not row.get("tentative")}
        require(set(expected) <= observed, f"Expected address missing on {name}: {expected}")

    for family, gateway in gateways.items():
        routes = ip_json(f"-{family}", "route", "show", "default")
        require(any(route.get("dev") == port and route.get("gateway") == str(gateway) for route in routes),
                f"Default gateway {gateway} missing on {port}")

    require(interfaces.get(bond, {}).get("master") == bridge, f"{bond} is not attached to {bridge}")
    for name in [*config["ports"], bond, bridge, *(name for name in addresses if name != port)]:
        require(interfaces.get(name, {}).get("mtu") == config["mtu"],
                f"Expected live MTU {config['mtu']} on {name}")
    for name in config["ports"]:
        require(interfaces.get(name, {}).get("master") == bond, f"{name} is not enslaved to {bond}")
    bond_mode = (Path("/sys/class/net") / bond / "bonding/mode").read_text().split()[0]
    require(bond_mode == "802.3ad", f"{bond} is not using LACP")
