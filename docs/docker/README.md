# `docker/`

## Rôle

- Fournir une infrastructure locale reproductible (PostgreSQL, Cassandra, etc.).

## Fichiers

- `docker-compose.yml`: squelette des services à adapter (ports, volumes, clusters/nœuds).

## Exécution (exemple)

Depuis la racine du projet:

```bash
docker compose -f docker/docker-compose.yml up -d
```

