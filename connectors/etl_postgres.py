"""
Module ETL : Migration PostgreSQL -> Cassandra Cluster B.
"""

import psycopg2
import pandas as pd
from cassandra.cluster import Cluster
from gevent import monkey
monkey.patch_all()

def run_postgres_etl():
    """
    Exécute l'extraction de university_sid et le chargement dans univ_sync.
    """
    print("🐘 Extraction Postgres en cours...")
    try:
        # 1. Extraction
        conn = psycopg2.connect(host='localhost', dbname='university_sid', user='postgres', password='1234')
        sql = """
            SELECT i.id_inscription, e.id_etudiant, i.matricule, e.nom, e.prenom, 
                   e.sexe, e.email, i.annee_academique, i.code_formation, 
                   i.cycle, i.niveau, i.type_etudiant, i.date_inscription
            FROM inscriptions i
            JOIN etudiants e ON i.id_etudiant = e.id_etudiant
        """
        df = pd.read_sql(sql, conn)

        # 2. Chargement
        cluster = Cluster(['127.0.0.1'], port=9043)
        session = cluster.connect('univ_sync')

        insert_stmt = session.prepare("""
            INSERT INTO etudiants_inscrits 
            (id_inscription, id_etudiant, matricule, nom, prenom, sexe, email, 
             annee_academique, code_formation, cycle, niveau, type_etudiant, date_inscription)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)

        for _, row in df.iterrows():
            session.execute(insert_stmt, (
                int(row['id_inscription']), int(row['id_etudiant']), str(row['matricule']),
                str(row['nom']), str(row['prenom']), str(row['sexe']), str(row['email']),
                str(row['annee_academique']), str(row['code_formation']), str(row['cycle']),
                str(row['niveau']), str(row['type_etudiant']), row['date_inscription']
            ))

        print(f"🚀 {len(df)} lignes synchronisées dans le Cluster B.")
        cluster.shutdown()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erreur ETL Postgres : {e}")
        return False

if __name__ == "__main__":
    run_postgres_etl()