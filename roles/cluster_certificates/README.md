# degitag.proxmox.cluster_certificates

Verwaltet die Web- und API-Zertifikate eines Proxmox-Clusters. Das Play sollte
mit `serial: 1` laufen, damit die Proxys nacheinander neu laden und die gemeinsam
genutzten ACME-Objekte seriell angelegt werden. Je Host sind Clustername,
Proxmox-Knotenname und DNS-Name des HTTPS-Endpunkts anzugeben.

- `proxmox_cert_source: custom` importiert eine PEM-Kette und den passenden
  Schlüssel von Controller-Pfaden. Bei privater PKI dient
  `proxmox_cert_ca_path` zur Validierung der Kette und des erreichbaren Servers.
  Der Controller und das Ziel prüfen den erwarteten Hostnamen. Eine andere
  vorhandene Zertifikatsidentität erfordert `proxmox_cert_replace: true`.
- `proxmox_cert_source: acme` verwendet einen vorhandenen Account oder
  registriert ihn mit dem hinterlegten Kontakt und den bereits akzeptierten
  aktuellen CA-Bedingungen (`proxmox_cert_tos_url`). Für DNS-01 kann die Rolle
  einen fehlenden Plugin-Eintrag mit DNS-Treiber und Vault-geschütztem
  `proxmox_cert_dns_data` anlegen. Für HTTP-01 verwendet sie `standalone`.
  Die spätere Erneuerung übernimmt der Proxmox-Timer `pve-daily-update.timer`.

Die Rolle prüft nach der Anwendung den HTTPS-Endpunkt mit aktivierter
Zertifikatsprüfung. DNS, Routing und die beim jeweiligen ACME-Verfahren
erforderliche öffentliche Erreichbarkeit müssen vorhanden sein.
