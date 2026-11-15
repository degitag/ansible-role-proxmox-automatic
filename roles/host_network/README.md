# degitag.proxmox.host_network

Verwaltet `/etc/network/interfaces` auf Proxmox-Hosts mit dedizierter,
statischer IPv4-/IPv6-Managementschnittstelle und einem Linux-LACP-Bond
unter einer VLAN-fähigen Bridge. Weitere IPv6-Adressen können auf
getaggten VLANs eingerichtet werden. Die Includes in
`/etc/network/interfaces.d/` bleiben für Proxmox SDN eingebunden.

Das Play läuft hostweise mit `serial: 1`. Die Zielknoten benötigen ifupdown2
und die vorgesehenen physischen Ports. Beide Managementadressen müssen vom
Ansible-Controller auf TCP-Port 22 erreichbar sein. Die Rolle validiert die
neue Datei vor dem Reload, sichert die vorherige Konfiguration und setzt
einen unabhängigen systemd-Rollback. Nach erfolgreicher SSH- und
Laufzeitprüfung wird der Rollback abgebrochen. Der Check-Modus prüft
Eingaben und Hostidentität und lädt das Netzwerk nicht neu.
