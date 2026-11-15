# degitag.proxmox.cluster_reboot

Startet Proxmox-Knoten einzeln neu. Das Play verwendet `serial: 1`.
`proxmox_reboot_cluster` und `proxmox_reboot_nodes` geben den erwarteten
Cluster und alle Online-Mitglieder an. Die Rolle prüft vor dem Neustart
die verbleibenden Corosync-Stimmen und wartet auf den bestätigten
HA-Wartungsmodus. Lokal laufende VMs oder Container blockieren den Reboot.

Mit `proxmox_reboot_ceph: true` prüft die Rolle die Verfügbarkeit von
Monitorquorum und Daten während des geplanten Stopps. Nach dem Start
wartet sie auf Proxmox, alle Corosync-Mitglieder und -Links, Ceph-Gesundheit
und die ursprünglichen lokalen OSDs. Erst dann hebt sie den von diesem
Lauf gesetzten Wartungsmodus auf. Ein bereits zuvor angeforderter
Wartungsmodus bleibt wirksam.

Jeder reguläre Aufruf ist ein neuer Reboot-Auftrag. Der Check-Modus
führt die lesenden Voraussetzungen aus, ohne den Knoten neu zu starten.
