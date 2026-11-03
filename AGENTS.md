# AGENTS.md

Dieses Repository pflegt `degitag.proxmox`: Proxmox-Provisionierung, deklarative Firewall-Verwaltung und Gastintegration. Die allgemeine Host-Baseline gehört zu `degitag.infrastructure`. Den bestehenden Remote-Namen `ansible-role-proxmox-automatic` nicht implizit ändern.

Vor Proxmox-Eingriffen API-Rechte, Ressourcenidentität, Storage, Netzwerk und Gastzugriff prüfen. Bestehende VMs, Daten und fremde Firewall-Objekte erhalten. Destruktive Neuinstallation, Clusteränderungen und Migrationen brauchen einen ausdrücklich beauftragten Umfang. Plattform- und Controllergrenzen aus README und Rollenvertrag übernehmen; keine Linux-Matrix anderer Collections pauschal übertragen. Echte Proxmox-/Gasttests benötigen ausdrücklich freigegebene dedizierte Systeme.

## Änderungsvertrag und Abnahme

- Wiederverwendbare Rollen und Module pflegen; kundenspezifische Hostwerte, Ziele und Secrets gehören in nutzende Inventories beziehungsweise deren Secret-Store.
- Öffentliche Variablen dokumentieren, sinnvoll und sicher vorbelegen sowie typisiert validieren. Fachlich erforderliche Eingaben vor Eingriffen prüfen. Bei kompatiblen Änderungen bestehende Nutzer und Variablenverträge erhalten; notwendige Inkompatibilitäten ausdrücklich mit Migrationsweg dokumentieren.
- Änderungen gegen die deklarierte Distributions- und Ansible-Supportmatrix aus README, Metadaten und Preflight prüfen; keine Unterstützung allein aus einem Syntaxlauf ableiten. Rollenbezogene Einschränkungen bleiben bestehen.
- Idempotenz auf geeigneten Testsystemen durch einen unveränderten zweiten Lauf mit `changed=0` nachweisen. Check-Modus soweit unterstützt berücksichtigen und seine Grenzen benennen. Echtes Dienstverhalten einschließlich systemd/journald auf geeigneten Systemen prüfen; Container allein belegen diese Funktion nicht.
- Den gemeinsamen Prüfeinstieg `bash tests/run_checks.sh` für Implementierungsänderungen und die zur Änderung passenden zusätzlichen Tests verwenden. Bei reinen Arbeitsanweisungsänderungen Markdown, Diff und Konsistenz prüfen und die ausgelöste erforderliche CI vollständig abwarten; keine künstlichen Implementierungs- oder Hosttests dafür anlegen.
- Changelog und Version passend zu funktionaler Änderung und Kompatibilität pflegen. Collection bauen und Artefakt prüfen; bei tatsächlichen Releases die Release-Prüfungen bis zum erfolgreichen Endzustand verfolgen. Reine Anweisungsänderungen begründen keinen Release-Tag. Eine Collection-Veröffentlichung autorisiert keinen Rollout auf nutzende Systeme.

## Auftragsabschluss und Dokumentation

Der globale Abschlussstandard gilt auch hier: Eigene Änderungen committen, pushen und per Pull Request (bei GitLab Merge Request) nach erfolgreichen erforderlichen Prüfungen integrieren; auftragsrelevante Nach-Merge-Prüfungen abwarten und erst danach eigene integrierte Arbeitsbranches bereinigen. Bestehende unabhängige Änderungen, Branches und Worktrees erhalten. Schutzregeln und erforderliche Reviews nicht umgehen; echte Blocker mit offenem Schritt benennen.

Repository-Integration, Veröffentlichung und produktiver Betrieb sind getrennte Ergebnisse. Eine erfolgreiche Prüfung oder ein Merge erteilt keine zusätzliche Produktionsfreigabe. Bestehende konkrete Freigaberegeln bleiben verbindlich; eine pauschale automatische Produktionsfreigabe wird hier nicht eingeführt.

In Anleitungen `vim` verwenden. Dokumentation aus Sicht von DevOps und Systemarchitektur schreiben. Technische Nachweise im Repository und bestehende Betriebsdokumentation in Outline erhalten; Outline nur im beauftragten Umfang bearbeiten. Secrets aus geschützten Variablenquellen beziehen, niemals ausgeben oder ins Repository übernehmen.
