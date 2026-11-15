# degitag.proxmox.host_install_media

Erzeugt ein unbeaufsichtigtes Proxmox-VE-Installationsmedium für einen
bestimmten Host. Die Rolle läuft auf einem Linux-Buildhost mit
`proxmox-auto-install-assistant` und `xorriso`. Die offizielle Quell-ISO wird
über ihren gepinnten SHA-256 geprüft. Der Installer erhält eine statische
Management-Adresse, einen Root-Passworthash und SSH-Public-Keys. Das
Zielsystemlaufwerk wird anhand des exakten Udev-Werts `ID_SERIAL_SHORT`
ausgewählt. Der Managementport wird anhand seiner MAC identifiziert.

Vor dem Booten prüft `tasks_from: verify_hardware` auf dem Zielhost mit
dem nativen `device-match`, ob die Filter jeweils genau ein Gerät ergeben. Ein Boot vom generierten Medium installiert Proxmox auf dem
angegebenen Systemlaufwerk. Das Medium lässt sich über USB, virtuelle
Medien oder eine Test-VM bereitstellen. Host-VLANs und Cluster-Aufbau
folgen nach dem ersten Start.

Der Pfad des erzeugten Mediums steht in `proxmox_host_installer_image`.
Das Medium enthält einen Passwort-Hash. Übergabe und Aufbewahrung
erfordern einen geschützten Pfad. Der Build hält die Datei auf Modus 0600
und entfernt temporäre Antwortdateien nach dem Lauf. Bei identischen
Inputs wird das vorhandene Medium erneut geprüft und wiederverwendet.
