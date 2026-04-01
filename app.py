"""
RDHA - Application Streamlit (fichier maître).

Rôle:
- Point d'entrée de l'interface utilisateur.
- Orchestre l'extraction (connectors), la transformation/chargement (data_marts)
  et l'accès aux services (core).
"""

from __future__ import annotations

import streamlit as st


def main() -> None:
    """Lance l'interface Streamlit."""
    st.set_page_config(page_title="RDHA", layout="wide")
    st.title("RDHA_PROJECT")
    st.caption("Interface Streamlit — squelette prêt à compléter.")

    st.info(
        "Structure initialisée. Ajoutez vos écrans, formulaires, et déclencheurs ETL ici."
    )


if __name__ == "__main__":
    main()

