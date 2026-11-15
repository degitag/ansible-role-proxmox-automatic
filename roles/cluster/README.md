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

Für einen neuen Cluster `tasks_from: bootstrap` mit der linearen Strategie und
allen Knoten im selben Play verwenden. Je Knoten die lokalen
`proxmox_cluster_links` angeben. `proxmox_cluster_seed` benennt den Seed im
Inventory. `proxmox_cluster_seed_address` ist dessen SSH-Ziel. Standalone-Knoten
benötigen einen geprüften SSH-Hostschlüssel für dieses Ziel und vorab
eingerichteten nichtinteraktiven Root-Zugriff auf den Seed.

Der Bootstrap stoppt bei widersprüchlicher Mitgliedschaft, fehlendem Quorum
oder Gästen auf einem Beitrittskandidaten. Im Check-Modus laufen die
Voraussetzungsprüfungen.
