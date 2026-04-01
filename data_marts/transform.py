"""
data_marts.transform

Rôle (TRANSFORM):
- Appliquer la logique de transformation/dénormalisation ("aplatir" les données).
- Préparer des tables/collections prêtes pour l'insertion (LOAD) dans Cassandra.
"""

from __future__ import annotations

import pandas as pd


def flatten(df: pd.DataFrame) -> pd.DataFrame:
    """
    Exemple de point d'entrée transformation.

    À compléter:
    - normalisation de colonnes
    - jointures
    - enrichissements
    - règles métier
    """
    # Squelette: retourner la même table pour l'instant.
    return df.copy()

