"""
data_marts.loaders

Rôle (LOAD):
- Insérer/mettre à jour les données transformées dans Cassandra.
- Centraliser les requêtes CQL (INSERT/UPDATE) et stratégies de batch.
"""

from __future__ import annotations

from typing import Any, Iterable


def insert_rows(
    cassandra_session: Any,
    cql: str,
    rows: Iterable[dict[str, Any]],
) -> int:
    """
    Insère une liste de lignes dans Cassandra.

    Attendu:
    - `cassandra_session` provient de `cassandra-driver`.
    - `cql` est une requête paramétrée.
    """
    # Placeholder: à remplacer par session.prepare + execute.
    count = 0
    for _row in rows:
        # cassandra_session.execute(prepared, _row)
        count += 1
    return count

