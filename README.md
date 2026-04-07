# RDHA Platform

Plateforme d’ingestion et de visualisation (Cassandra, sources multiples, interface Streamlit).

## Prérequis

- **Python 3** avec un environnement virtuel recommandé
- **Docker** et Docker Compose (pour les nœuds Cassandra locaux)
- Dépendances Python : à la racine du projet, après activation du venv :

```bash
pip install -r requirements.txt
```

### Pipeline complète (`connector_main.py`)

Le fichier `connector_main.py` enchaîne trois étapes :

1. **PostgreSQL → Cassandra (cluster B, port 9043)** : une instance PostgreSQL doit être accessible sur `localhost`, base `university_sid`, utilisateur `postgres` (mot de passe configuré dans `connectors/etl_postgres.py`). Sans cette base, l’étape 1 échouera (les étapes suivantes peuvent quand même s’exécuter selon le code).
2. **API JSON → Cassandra (cluster C, port 9044)** : le serveur Flask décrit ci-dessous doit tourner sur le port **5001**.
3. **CSV locaux → Cassandra (cluster A, port 9042)** : les fichiers CSV sont lus depuis `data_sources/sftp/`. S’il n’y a aucun CSV, l’étape se termine sans erreur bloquante.

Pour un premier lancement centré sur **Cassandra + API JSON + Streamlit**, suivez l’ordre ci-dessous ; ajoutez PostgreSQL et les CSV si vous voulez toute la synchronisation.

## Lancer le projet (ordre recommandé)

### 1. Démarrer Cassandra (Docker)

À la racine du dépôt :

```bash
docker compose -f docker/docker-compose.yml up -d
```

Trois conteneurs démarrent (ports **9042**, **9043**, **9044**). Attendre environ **30 à 60 secondes** (voire plus au premier démarrage) que les nœuds soient prêts avant de lancer les connecteurs.

Arrêt des conteneurs :

```bash
docker compose -f docker/docker-compose.yml down
```

### 2. Démarrer la source de données API JSON (Flask)

Le serveur est le fichier `app.py` dans **`data_sources/api_json/`** (il écoute sur le port **5001**).

```bash
cd data_sources/api_json
python app.py
```

Laisser ce terminal ouvert. Sous **Windows PowerShell**, depuis la racine du projet :

```powershell
cd data_sources\api_json
python app.py
```

### 3. Lancer la synchronisation (connecteurs / ETL)

Dans un **nouveau** terminal, à la **racine du projet** :

```bash
python connector_main.py
```

Ce script initialise les keyspaces / tables Cassandra selon les connecteurs et exécute les ETL (PostgreSQL, API JSON, dossier CSV simulé SFTP selon la configuration du code).

### 4. Lancer l’interface Streamlit

Dans un **autre** terminal, toujours à la **racine du projet** :

```bash
streamlit run main_app.py
```

Ouvrir l’URL affichée dans le terminal (en général `http://localhost:8501`).

## Récapitulatif des terminaux

| Étape | Commande (exemple) | Rôle |
|--------|-------------------|------|
| 1 | `docker compose -f docker/docker-compose.yml up -d` | Cassandra (3 clusters locaux) |
| 2 | `python app.py` dans `data_sources/api_json/` | API JSON des paiements |
| 3 | `python connector_main.py` | Ingestion vers Cassandra |
| 4 | `streamlit run main_app.py` | Interface web RDHA |

Documentation complémentaire sur Docker : `docs/docker/README.md`.
