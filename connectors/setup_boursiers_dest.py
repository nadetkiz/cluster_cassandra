"""
Module de configuration pour le Cluster A (Boursiers).
Initialise le Keyspace et la table pour les données SFTP.
"""
from gevent import monkey
monkey.patch_all()
from cassandra.cluster import Cluster

def init_cassandra_a():
    """Prépare le Cluster A (Port 9042) pour les données boursiers."""
    try:
        cluster = Cluster(['127.0.0.1'], port=9042)
        session = cluster.connect()

        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS univ_boursiers 
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3}
        """)
        session.set_keyspace('univ_boursiers')

        # Table basée sur la structure de ton CSV
        session.execute("""
            CREATE TABLE IF NOT EXISTS boursiers (
                id_bourse int PRIMARY KEY,
                nom text,
                prenom text,
                sexe text,
                date_naissance date,
                annee_academique text,
                type_bourse text,
                code_formation text,
                cycle text,
                niveau text
            )
        """)
        print("✅ Configuration Cluster A (Boursiers) : OK")
        cluster.shutdown()
        return True
    except Exception as e:
        print(f"❌ Erreur Setup Cluster A : {e}")
        return False

if __name__ == "__main__":
    init_cassandra_a()