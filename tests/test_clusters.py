# 1. CES 3 LIGNES DOIVENT ÊTRE LES TOUTES PREMIÈRES
from gevent import monkey
monkey.patch_all()
import cassandra

# 2. ENSUITE TU FAIS TES IMPORTS NORMAUX
from cassandra.cluster import Cluster
import sys

def test_connection(name, port):
    print(f"--- Test de connexion au {name} (Port {port}) ---")
    try:
        # On force l'utilisation du loop de gevent pour Python 3.12
        cluster = Cluster(['127.0.0.1'], port=port, connect_timeout=10)
        session = cluster.connect()
        
        row = session.execute("SELECT cluster_name FROM system.local").one()
        print(f"✅ SUCCÈS ! Connecté au cluster : {row.cluster_name}")
        
        cluster.shutdown()
    except Exception as e:
        print(f"❌ ÉCHEC pour {name} : {e}")
    print("\n")

if __name__ == "__main__":
    print("🚀 Démarrage des tests (Mode Compatibilité Python 3.12)...\n")
    test_connection("Cluster A (Staging)", 9042)
    test_connection("Cluster B (SQL Sync)", 9043)
    test_connection("Cluster C (Analytics)", 9044)