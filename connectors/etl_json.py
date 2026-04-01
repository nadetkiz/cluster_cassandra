"""
Module ETL : API Flask -> Cassandra Cluster C.
Gère les IDs de paiement alphanumériques.
"""
import requests
import pandas as pd
from cassandra.cluster import Cluster
from gevent import monkey
monkey.patch_all()

def run_json_etl(api_url="http://127.0.0.1:5001/paiements"):
    """Récupère le JSON et l'insère sans conversion entière sur l'ID."""
    print(f"🌐 Extraction depuis l'API : {api_url}...")
    try:
        # 1. Extraction
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        # 2. Chargement (Port 9044)
        cluster = Cluster(['127.0.0.1'], port=9044)
        session = cluster.connect('univ_analytics')

        insert_stmt = session.prepare("""
            INSERT INTO paiements_etudiants 
            (id_paiement, matricule, type_paiement, montant, date_paiement)
            VALUES (?, ?, ?, ?, ?)
        """)

        for _, row in df.iterrows():
            session.execute(insert_stmt, (
                str(row['id_paiement']),  
                str(row['matricule']),
                str(row['type_paiement']),
                float(row['montant']),
                pd.to_datetime(row['date_paiement'])
            ))

        print(f"🚀 {len(df)} paiements synchronisés (IDs Texte) dans le Cluster C.")
        cluster.shutdown()
        return True
    except Exception as e:
        print(f"❌ Erreur ETL JSON : {e}")
        return False

if __name__ == "__main__":
    run_json_etl()