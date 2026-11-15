# degitag.proxmox.openfabric

Konfiguriert ein IPv6-OpenFabric über die Proxmox-SDN-API. Das lineare Play
umfasst alle Mitglieder des quoraten Clusters. Jedes Mitglied benötigt eine
eigene Fabric-Adresse und bereits stabil benannte Netzwerkschnittstellen.
Die Rolle installiert FRR, aktiviert IPv6-Forwarding und legt Fabric und Nodes
an. Sie meldet Abweichungen an vorhandenen Fabric-Objekten.

Mit `proxmox_openfabric_apply: true` wird die **gesamte** ausstehende
SDN-Konfiguration von Proxmox angewendet. Diese Option eignet sich für einen
dedizierten Cluster oder einen koordinierten SDN-Rollout. Anschließend prüft
die Rolle die IPv6-Erreichbarkeit von jeder Fabric-Adresse zu allen Peers.
Die Bereitstellung persistenter Thunderbolt-Interfaces und Ethernet-Fallbacks
erfolgt vor beziehungsweise nach dem Fabric-Aufbau.
