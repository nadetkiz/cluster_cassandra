"""
core.utils

Rôle:
- Fonctions utilitaires partagées (dates, UUID, validations simples).
- Éviter de dupliquer de petites fonctions dans plusieurs modules.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4


def utc_now() -> datetime:
    """Retourne la date/heure courante en UTC (timezone-aware)."""
    return datetime.now(timezone.utc)


def new_uuid() -> UUID:
    """Génère un UUID v4."""
    return uuid4()


def isoformat_utc(dt: datetime) -> str:
    """Formate une datetime en ISO 8601 (UTC)."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()

