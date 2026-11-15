#!/usr/bin/python3
"""Keep Ceph fallback routes and discovered Thunderbolt links configured.

Never reset controllers or cycle a working link. Encode a high FRR distance as
well as a high Linux metric, so both Zebra and the kernel prefer OpenFabric.
"""
import argparse
import fcntl
import ipaddress
import json
import os
from pathlib import Path
import subprocess
import time

# Zebra imports the top byte as administrative distance. OpenFabric uses 115.
FALLBACK_METRIC = (250 << 24) + 32760


def run(*args):
    return subprocess.check_output(args, text=True, timeout=15)


def reconcile(config, check=False):
    rows, errors = [], []
    changed = False
    def metric(name, value, interface=None):
        label = '{interface=' + json.dumps(interface) + '}' if interface else ''
        rows.append(f'lenmail_thunderbolt_{name}{label} {value}')
    for link in config['links']:
        name = link['name']
        try:
            control = Path('/sys/bus/pci/devices') / link['pci'] / 'power/control'
            if control.read_text().strip() != 'on':
                if check:
                    raise RuntimeError('controller runtime suspend is enabled')
                control.write_text('on')
                changed = True
            # USB4 host routers have their own runtime PM, independent of NHI PCI.
            pci = Path('/sys/bus/pci/devices') / link['pci']
            for router_control in pci.glob('domain*/*-0/power/control'):
                if router_control.read_text().strip() != 'on':
                    if check:
                        raise RuntimeError('USB4 host router runtime suspend is enabled')
                    router_control.write_text('on')
                    changed = True
            net = Path('/sys/class/net') / name
            present = net.exists()
            metric('present', int(present), name)
            if present:
                addresses = json.loads(run('ip', '-j', '-6', 'addr', 'show', 'dev', name))
                interface = next(iter(addresses), {})
                expected = ipaddress.ip_interface(link['address']).ip
                addressed = any(ipaddress.ip_address(address['local']) == expected
                                for address in interface.get('addr_info', []))
                up = 'UP' in interface.get('flags', [])
                if not addressed or not up or int((net / 'mtu').read_text()) != config['mtu']:
                    if check:
                        raise RuntimeError('interface configuration drift')
                    run('/usr/sbin/ifup', '--force', name)
                    changed = True
            try:
                carrier = int((net / 'carrier').read_text()) if present else 0
            except OSError:
                carrier = 0
            metric('carrier', carrier, name)
            peer = link['peer_ceph_sync_ipv6']
            routes = json.loads(run('ip', '-j', '-6', 'route', 'show', 'exact', peer + '/128'))
            fallback = any(r.get('metric') == FALLBACK_METRIC and r.get('protocol', 'boot') == 'boot'
                           and r.get('gateway') == link['gateway']
                           and r.get('dev') == config['fallback_interface']
                           and r.get('prefsrc') == config['source'] for r in routes)
            if not fallback:
                if check:
                    raise RuntimeError('fallback route missing or incorrect')
                run('ip', '-6', 'route', 'replace', peer + '/128', 'via', link['gateway'],
                    'dev', config['fallback_interface'], 'src', config['source'],
                    'proto', 'boot', 'metric', str(FALLBACK_METRIC))
                changed = True
            # Replace only our initial incident route, after its successor exists.
            legacy = any(r.get('metric') == 32760 and r.get('gateway') == link['gateway']
                         and r.get('dev') == config['fallback_interface']
                         and r.get('prefsrc') == config['source'] for r in routes)
            if legacy:
                if check:
                    raise RuntimeError('legacy fallback distance would override OpenFabric')
                run('ip', '-6', 'route', 'del', peer + '/128', 'via', link['gateway'],
                    'dev', config['fallback_interface'], 'metric', '32760')
                changed = True
            selected = json.loads(run('ip', '-j', '-6', 'route', 'get', peer))[0]
            metric('ethernet_fallback', int(selected.get('dev') == config['fallback_interface']), name)
        except (OSError, ValueError, KeyError, subprocess.SubprocessError, RuntimeError) as exc:
            errors.append(f'{name}: {exc}')
    metric('reconcile_success', int(not errors))
    metric('timestamp_seconds', int(time.time()))
    if not check:
        target = Path('/var/lib/prometheus/node-exporter/lenmail-thunderbolt.prom')
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix('.tmp')
        tmp.write_text('\n'.join(rows) + '\n')
        tmp.chmod(0o644)
        os.replace(tmp, target)
    if errors:
        raise RuntimeError('; '.join(errors))
    print('changed' if changed else 'ok')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    with open('/run/lock/pve-thunderbolt-reconcile.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        reconcile(json.loads(Path('/etc/pve-thunderbolt.json').read_text()), args.check)
