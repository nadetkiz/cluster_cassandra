"""
connectors.file_source

Rôle (EXTRACT):
- Lire des fichiers plats (CSV) depuis disque/local ou répertoires partagés.
- Offrir des helpers de parsing (séparateur, encodage, schémas).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pandas as pd


def read_csv(
    path: str | Path,
    *,
    sep: str = ",",
    encoding: Optional[str] = "utf-8",
    dtype: Optional[dict[str, Any]] = None,
) -> pd.DataFrame:
    """Charge un CSV dans un DataFrame."""
    return pd.read_csv(Path(path), sep=sep, encoding=encoding, dtype=dtype)

