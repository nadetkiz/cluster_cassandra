"""
ORCHESTRATEUR GLOBAL - Projet RDHA
Ce fichier est le point d'entrée unique pour synchroniser 
PostgreSQL (Cluster B) et l'API JSON (Cluster C).
"""
# Import des configurations (Setup)
from connectors.setup_postgres_dest import init_cassandra_b
from connectors.setup_analytics_dest import init_cassandra_c
from connectors.setup_boursiers_dest import init_cassandra_a
from connectors.etl_sftp import run_sftp_etl

# Import des moteurs de transfert (ETL)
from connectors.etl_postgres import run_postgres_etl
from connectors.etl_json import run_json_etl

def main():
    print("🚀 --- DÉMARRAGE DE LA PIPELINE DÉCISIONNELLE --- 🚀\n")

    # --- ÉTAPE 1 : POSTGRESQL -> CLUSTER B ---
    print("1️⃣ Traitement des données Étudiants...")
    # On crée la table, et si ça réussit, on lance l'ETL
    if init_cassandra_b():
        run_postgres_etl()
    else:
        print("⚠️ Échec de l'étape 1 : Impossible de configurer le Cluster B.")

    print("-" * 50)

    # --- ÉTAPE 2 : API JSON -> CLUSTER C ---
    print("2️⃣ Traitement des données Paiements (via Flask)...")
    # On crée la table, et si ça réussit, on lance l'ETL
    if init_cassandra_c():
        run_json_etl()
    else:
        print("⚠️ Échec de l'étape 2 : Impossible de configurer le Cluster C.")

    print("\n🏁 --- TOUTES LES SOURCES SONT SYNCHRONISÉES --- 🏁")

    # --- ÉTAPE 3 : SFTP CSV -> CLUSTER A ---
    print("3️⃣ Traitement des données Boursiers (SFTP)...")
    if init_cassandra_a():
        run_sftp_etl()

if __name__ == "__main__":
    main()