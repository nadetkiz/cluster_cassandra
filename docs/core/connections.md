# `core/connections.py`

## Rôle

- Centralise l'initialisation des connexions **Cassandra** et **PostgreSQL**.
- Évite la duplication de configuration/initialisation dans l'UI ou les traitements.

## À compléter

- **Cassandra**: implémenter `init_cassandra_clusters` avec `cassandra-driver`.
- **PostgreSQL**: implémenter `init_postgres_connection` avec `psycopg2` ou `SQLAlchemy`.

## Bonnes pratiques

- Ne pas commiter de secrets (utiliser variables d'environnement).
- Prévoir des timeouts et une stratégie de retry côté clients.

