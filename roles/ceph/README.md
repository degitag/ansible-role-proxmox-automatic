# degitag.proxmox.ceph

Installiert Ceph Tentacle auf Proxmox VE und richtet die IPv6-Konfiguration,
Monitore und Manager ein. Das Play umfasst sämtliche Ceph-Knoten in einem
linearen Durchlauf. Der erste Eintrag in `proxmox_ceph_nodes` initialisiert
die gemeinsame Konfiguration. Die Rolle prüft vor Änderungen das Quorum und
die aktiven lokalen Adressen für Public- und Replikationsnetz.

`proxmox_ceph_public_network` und `proxmox_ceph_replication_network` sind
IPv6-Präfixe. Je Host werden `proxmox_ceph_public_address` und
`proxmox_ceph_replication_address` gesetzt. `proxmox_ceph_cluster_name`
benennt den erwarteten Proxmox-Cluster. Das Repository wird über
`proxmox_ceph_repository` gewählt. Bei einem vorhandenen Ceph-Cluster müssen
die konfigurierten Netze mit den Sollwerten übereinstimmen.

Der Einstieg deckt die Paketinstallation und die Monitor-/Manager-Dienste
ab. Die Bereitstellung von OSDs, Pools und Proxmox-Storage folgt separat.
