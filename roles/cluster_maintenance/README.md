# degitag.proxmox.cluster_maintenance

Setzt oder beendet den Proxmox-HA-Wartungsmodus für einen Knoten. Das Play
umfasst genau den betroffenen Knoten. `proxmox_maintenance_cluster` und
`proxmox_maintenance_node` geben die erwarteten Namen an.
`proxmox_maintenance_state` ist `enabled` oder `disabled`.

Die Rolle prüft Quorum, HA-Dienste und die Zeitstempel des HA-Managers und
des lokalen Resource Managers. Sie wartet auf den bestätigten LRM-Modus
und beim Eintritt außerdem darauf, dass keine aktiven HA-Ressourcen mehr
dem Knoten zugeordnet sind. Ein Wiederholungslauf prüft den Zustand ohne
erneute Anforderung. Check-Modus führt die lesenden Voraussetzungen aus.

Vor einem Shutdown oder Neustart sind zusätzlich lokal laufende VMs ohne
HA, die verbleibenden Corosync-Stimmen und der Zustand gemeinsam genutzter
Storage-Systeme zu prüfen.
