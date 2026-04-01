"""
connectors.api_source

Rôle (EXTRACT):
- Appeler des APIs JSON (GET/POST) et normaliser la réponse.
- Gérer timeouts, headers et erreurs réseau de base.
"""

from __future__ import annotations

from typing import Any, Optional

import requests


def get_json(
    url: str,
    *,
    headers: Optional[dict[str, str]] = None,
    params: Optional[dict[str, Any]] = None,
    timeout_s: float = 30.0,
) -> Any:
    """Appel GET et retourne le JSON décodé."""
    resp = requests.get(url, headers=headers, params=params, timeout=timeout_s)
    resp.raise_for_status()
    return resp.json()


def post_json(
    url: str,
    *,
    headers: Optional[dict[str, str]] = None,
    payload: Optional[dict[str, Any]] = None,
    timeout_s: float = 30.0,
) -> Any:
    """Appel POST JSON et retourne le JSON décodé."""
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout_s)
    resp.raise_for_status()
    return resp.json()

