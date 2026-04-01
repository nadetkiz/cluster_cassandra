"""
Module de configuration pour le Cluster C (Analytique).
Initialise le Keyspace et la table pour les paiements (ID en format Texte).
"""
from gevent import monkey
monkey.patch_all()
from cassandra.cluster import Cluster

def init_cassandra_c():
    """Prépare le Cluster C (Port 9044) avec id_paiement en type TEXT."""
    try:
        cluster = Cluster(['127.0.0.1'], port=9044)
        session = cluster.connect()

        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS univ_analytics 
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3}
        """)
        session.set_keyspace('univ_analytics')

        # Suppression nécessaire car on change le type de la Primary Key
        session.execute("DROP TABLE IF EXISTS paiements_etudiants")

        # id_paiement passe en 'text'
        session.execute("""
            CREATE TABLE IF NOT EXISTS paiements_etudiants (
                id_paiement text PRIMARY KEY,
                matricule text,
                type_paiement text,
                montant float,
                date_paiement timestamp
            )
        """)
        print("✅ Configuration Cluster C (Analytics) mise à jour en format TEXT.")
        cluster.shutdown()
        return True
    except Exception as e:
        print(f"❌ Erreur Setup Cluster C : {e}")
        return False

if __name__ == "__main__":
    init_cassandra_c()