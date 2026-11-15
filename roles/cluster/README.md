# degitag.proxmox.cluster

Liest den lokalen Proxmox-Clusterzustand und prüft bei vorgegebener Solltopologie
Clustername, Mitglieder, Online-Status und Quorum. Die Rolle läuft per SSH auf
den Proxmox-Knoten und braucht `become` für den lokalen Aufruf von `pvesh`.

Ohne Solltopologie liefert der Lauf einen Bericht pro Host. Mit
`proxmox_cluster_name` und `proxmox_cluster_nodes` schlägt er bei Abweichungen
fehl. Der Check-Modus führt dieselben lesenden Prüfungen aus.

```yaml
- name: Verify the cluster from every member
  hosts: proxmox_nodes
  gather_facts: false
  roles:
    - role: degitag.proxmox.cluster
      vars:
        proxmox_cluster_name: example
        proxmox_cluster_nodes: [pve01, pve02, pve03]
```
