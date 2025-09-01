
# Projet 1 — Tracker revenus livreur (CLI Python)

## Installation
- Python 3.10+ recommandé.
- `pip install matplotlib` pour le graphique.

## Commandes (exemples)
```bash
python tracker.py init
python tracker.py add --date 2025-09-01 --plateforme uber --heures 3.2 --km 31 --euros 44.50 --pourboires 6
python tracker.py summary --from 2025-08-29 --to 2025-09-04
python tracker.py plot --from 2025-08-29 --to 2025-09-04 --output out/revenus_hebdo.png
```
