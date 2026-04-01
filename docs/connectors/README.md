# `connectors/`

## Rôle

La couche **EXTRACT**: lecture des données depuis différentes sources.

## Modules

- `sql_source.py`: exécution de requêtes PostgreSQL et retour DataFrame.
- `api_source.py`: appels HTTP (GET/POST) et décodage JSON.
- `sftp_source.py`: téléchargement de fichiers via SFTP (à implémenter).
- `file_source.py`: lecture de fichiers CSV depuis le disque.

## Règles

- Pas de logique métier ici (elle va dans `data_marts/transform.py`).
- Toujours gérer erreurs/timeouts côté I/O.

