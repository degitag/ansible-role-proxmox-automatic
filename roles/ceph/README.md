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

Mit `proxmox_ceph_wait_for_chrony: true` aktiviert die Rolle den
vorhandenen Dienst `chrony-wait.service`. Voraussetzung ist ein laufender
Chrony mit erreichbaren Zeitquellen. Beim Boot wartet systemd vor
`time-sync.target` bis zu 90 Sekunden auf eine verbleibende lokale
Zeitabweichung unter 20 ms. Ceph-Monitore starten nach diesem Ziel.
Der Rollenlauf prüft die Synchronisierung auch auf bereits laufenden Hosts.

Je Host benennt `proxmox_ceph_osd_devices` die vorgesehenen ganzen Datenträger
unter `/dev/disk/by-id/`. Die Rolle akzeptiert leere Datenträger sowie bereits
zum aktiven Ceph-FSID gehörige OSDs. Bei fremden Signaturen oder Partitionen
bricht sie ab. Der optionale `proxmox_ceph_rbd_pool` konfiguriert einen
replizierten Pool mit drei Kopien und Mindestgröße zwei und registriert ihn als
Proxmox-Storage. Anschließend prüft die Rolle OSDs und Placement Groups.
