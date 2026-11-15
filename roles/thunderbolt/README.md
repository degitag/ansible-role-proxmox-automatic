# degitag.proxmox.thunderbolt

Die Rolle hält Thunderbolt-Netzwerknamen über den PCI-Pfad stabil, lädt den
Treiber beim Boot und aktiviert die von Proxmox konfigurierten Schnittstellen
bei Hotplug. `proxmox_thunderbolt_links` enthält je Host `name` und `path`.
`proxmox_thunderbolt_mtu` ist standardmäßig 9000. Neue Namen für bereits
vorhandene Geräte greifen bei der nächsten Geräteerkennung oder beim Boot.

Nach dem OpenFabric-Aufbau richtet `tasks_from: fallback` den Ethernet-Pfad
ein. Dazu kommen je Link `address` (lokale Linkadresse mit Präfix),
`peer_ceph_sync_ipv6` und `gateway` (Ethernet-Adresse des Peers).
`proxmox_thunderbolt_source` ist die lokale Fabric-Adresse und
`proxmox_thunderbolt_fallback_interface` das lokale Ethernet-Interface.
Ein systemd-Timer gleicht die Routen alle 30 Sekunden ab. Die Metriken
behalten aus Kompatibilitätsgründen das Präfix `lenmail_thunderbolt_`.
