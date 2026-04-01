"""
core.connections

Rôle:
- Centraliser l'initialisation des connexions aux services externes.
- Préparer les 3 clusters Cassandra + la connexion PostgreSQL.

Note:
- Ce fichier est un squelette. Les secrets (hosts, users, mots de passe) ne doivent
  pas être commités en clair: utiliser variables d'environnement ou un vault.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class CassandraClusterConfig:
    """Configuration minimale d'un cluster Cassandra."""

    name: str
    contact_points: list[str]
    port: int = 9042
    keyspace: Optional[str] = None


@dataclass(frozen=True)
class PostgresConfig:
    """Configuration minimale PostgreSQL."""

    host: str
    port: int
    database: str
    user: str
    password: str


def init_cassandra_clusters(configs: list[CassandraClusterConfig]) -> dict[str, Any]:
    """
    Initialise les sessions/clients Cassandra (3 clusters attendus).

    Retour:
    - dict {cluster_name: session/client}
    """
    # À compléter avec cassandra-driver:
    # from cassandra.cluster import Cluster
    # cluster = Cluster(contact_points=..., port=...)
    # session = cluster.connect(keyspace)
    clients: dict[str, Any] = {}
    for cfg in configs:
        clients[cfg.name] = None  # placeholder
    return clients


def init_postgres_connection(cfg: PostgresConfig) -> Any:
    """
    Initialise une connexion PostgreSQL.

    Retour:
    - connexion/engine (selon psycopg2 ou SQLAlchemy)
    """
    # À compléter, ex psycopg2:
    # import psycopg2
    # return psycopg2.connect(...)
    return None

