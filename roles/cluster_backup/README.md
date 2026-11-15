# degitag.proxmox.cluster_backup

Erzeugt auf dem quoraten Proxmox-Knoten einen konsistenten SQLite-Snapshot
von pmxcfs. Das private Archiv enthält außerdem Corosync-Authentifizierung,
Hostnamen, Hostauflösung, Netzwerkdatei und vorhandene SDN-/Thunderbolt-Dateien.

`proxmox_backup_cluster`, `proxmox_backup_node` und ein absoluter
`proxmox_backup_path` werden pro Zielknoten gesetzt. Für einen neuen Snapshot
einen neuen Archivnamen wählen. Ein bereits vorhandenes Archiv am gleichen
Pfad wird geprüft und wiederverwendet. `proxmox_backup_action: verify`
verifiziert Archivstruktur, Cluster- und Knotenzuordnung, SHA-256 und den
SQLite-Inhalt. Diese Prüfung lässt sich auch im Check-Modus ausführen.

Das Archiv enthält private Clusterschlüssel und ist lokal nur für root lesbar.
Für die externe Aufbewahrung einen verschlüsselten Sicherungskanal verwenden.
Die Rolle schreibt beim Verifizieren nur in ein temporäres Verzeichnis und
ändert die laufende Clusterkonfiguration dabei nicht.

`proxmox_backup_action: stage_restore` prüft das Archiv erneut und legt die
Originalpfade relativ zum privaten Geschwisterverzeichnis
`<Archivpfad>.restore` ab. Ein identischer Verzeichnisbaum wird wiederverwendet.
Abweichende Inhalte, fremde Dateien und unsichere Dateirechte führen zum Abbruch.
Der Check-Modus legt keine Wiederherstellungsdateien an.

Für die eigentliche Wiederherstellung einen isolierten Ersatzhost mit passender
Proxmox-Version und getrenntem Zugriff auf Cluster- und Storage-Netze verwenden.
Die Wiederherstellung der Datenbank und die Prüfung der Knotenidentität erfolgen
nach dem offiziellen Proxmox-Recovery-Verfahren. Das Archiv sichert die
Clusterkonfiguration. Gastdaten und Ceph-Daten benötigen eigene Sicherungen.

[Proxmox VE Administration Guide](https://pve.proxmox.com/pve-docs/pve-admin-guide.pdf)
