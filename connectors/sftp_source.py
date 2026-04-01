"""
connectors.sftp_source

Rôle (EXTRACT):
- Se connecter à un serveur SFTP et télécharger des fichiers sources.
- Isoler les détails SFTP (auth, chemins distants, etc.) du reste du pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class SftpConfig:
    """Configuration SFTP (squelette)."""

    host: str
    port: int = 22
    username: str = ""
    password: Optional[str] = None
    private_key_path: Optional[str] = None


def download_file(
    cfg: SftpConfig,
    remote_path: str,
    local_path: str | Path,
) -> Path:
    """
    Télécharge un fichier depuis SFTP vers `local_path`.

    Implémentation attendue:
    - Utiliser `paramiko` ou une lib SFTP de votre choix.
    """
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # Placeholder: à remplacer par la vraie implémentation SFTP.
    raise NotImplementedError("Implémenter le téléchargement SFTP (ex: paramiko).")

