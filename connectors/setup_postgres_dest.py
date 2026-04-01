"""
Module de configuration pour le Cluster B (SQL Sync).
Initialise le Keyspace et la table dénormalisée.
"""

from gevent import monkey
monkey.patch_all()
from cassandra.cluster import Cluster

def init_cassandra_b():
    """
    Crée le Keyspace 'univ_sync' et la table 'etudiants_inscrits' sur le Cluster B.
    Port : 9043.
    """
    try:
        cluster = Cluster(['127.0.0.1'], port=9043)
        session = cluster.connect()

        # Création du Keyspace
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS univ_sync 
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3}
        """)
        
        session.set_keyspace('univ_sync')

        # Création de la table
        session.execute("""
            CREATE TABLE IF NOT EXISTS etudiants_inscrits (
                id_inscription int PRIMARY KEY,
                id_etudiant int,
                matricule text,
                nom text,
                prenom text,
                sexe text,
                email text,
                annee_academique text,
                code_formation text,
                cycle text,
                niveau text,
                type_etudiant text,
                date_inscription date
            )
        """)
        print("✅ Configuration Cluster B : OK")
        cluster.shutdown()
        return True # Pour informer l'orchestrateur du succès
    except Exception as e:
        print(f"❌ Erreur Setup Cluster B : {e}")
        return False

# Ce bloc permet de tester le fichier SEUL si besoin, 
# mais il ne se lancera pas lors d'un 'import'
if __name__ == "__main__":
    init_cassandra_b()