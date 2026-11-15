# degitag.proxmox.cluster_auth

Verwaltet OIDC-Realms, Benutzer, Gruppen, Gruppenmitgliedschaften und ACLs
auf einem Administrationsknoten des quoraten Proxmox-Clusters. Die Rolle
prüft den vorgesehenen Clusternamen vor dem ersten Schreibzugriff.

`proxmox_auth_oidc_realms` enthält Realm-ID, Issuer und Client-ID. Den
optionalen vertraulichen Client-Schlüssel aus Ansible Vault oder einem
Secret-Store übergeben. `username_claim` wird beim Erstellen gesetzt und
bei vorhandenen Realms geprüft. Automatische Benutzeranlage ist
standardmäßig deaktiviert. Der Identity Provider benötigt die exakten
Proxmox-Origins einschließlich Port 8006 als erlaubte Redirect-URIs.

Die Rolle legt in `proxmox_auth_users` genannte Benutzerkonten an. Lokale
Passwörter und MFA werden unabhängig davon eingerichtet. Mit
`proxmox_auth_memberships` werden Gruppen zu den vorhandenen
Mitgliedschaften ergänzt. `proxmox_auth_group_acls` vergibt vorhandene
Proxmox-Rollen an Gruppen. Bestehende zusätzliche Zugriffe bleiben erhalten.

Mit `proxmox_auth_roles` können eigene Proxmox-Rollen vor der ACL-Zuweisung
angelegt und verwaltet werden. Je Rolle wird die vollständige Liste
`privileges` angegeben. Änderungen an dieser Liste wirken sich auf alle
vorhandenen ACLs mit derselben Rolle aus. Eingebaute Proxmox-Rollen sind
geschützt.
