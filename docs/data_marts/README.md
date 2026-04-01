# `data_marts/`

## Rôle

Couche **TRANSFORM & LOAD**.

- `transform.py`: transforme/denormalise les données (format cible).
- `loaders.py`: écrit dans Cassandra (INSERT/UPDATE), éventuellement batch.

## Conseils

- Centraliser les règles métier dans `transform.py`.
- Valider les schémas (colonnes obligatoires, types) avant le LOAD.

