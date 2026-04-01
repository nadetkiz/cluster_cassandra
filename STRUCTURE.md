# RDHA_PROJECT — Structure du projet

Cette structure sépare clairement:
- **Interface** (Streamlit) → `app.py`
- **Moteur / cœur** (connexions, utilitaires) → `core/`
- **Extraction des sources** → `connectors/`
- **Transformation & chargement** → `data_marts/`
- **Infrastructure** → `docker/`
- **Documentation** → `docs/` (un fichier par partie)

## Arborescence

```
RDHA_PROJECT/
│
├── app.py                 # Le fichier MAÎTRE (Streamlit) : UI + orchestration
│
├── core/                  # La logique interne (Le moteur)
│   ├── connections.py     # Initialisation Cassandra & PostgreSQL
│   └── utils.py           # Helpers (dates, UUID, etc.)
│
├── connectors/            # La couche EXTRACT (Sources)
│   ├── sql_source.py      # Lecture PostgreSQL
│   ├── api_source.py      # Appels API JSON
│   ├── sftp_source.py     # Connexion & téléchargement SFTP
│   └── file_source.py     # Lecture des CSV
│
├── data_marts/            # La couche TRANSFORM & LOAD
│   ├── transform.py       # Dénormalisation / aplatissement
│   └── loaders.py         # Insert/Update dans Cassandra
│
├── docker/                # Infrastructure
│   └── docker-compose.yml # Définition services
│
├── docs/                  # Documentation (par partie)
│   ├── core/
│   ├── connectors/
│   ├── data_marts/
│   └── docker/
│
└── requirements.txt       # Dépendances Python
```

## Convention d’utilisation

- `connectors/*` ne fait que **lire** (pas de transformation métier).
- `data_marts/transform.py` applique les **règles métier** et prépare le format cible.
- `data_marts/loaders.py` exécute les **écritures** (Cassandra).
- `core/connections.py` centralise les **initialisations** de connexions (évite duplication).
- `docs/` contient la documentation de référence (ex: comment configurer, exemples d’usage).

