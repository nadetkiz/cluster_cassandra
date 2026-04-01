"""
Module ETL : Simulation SFTP (Fichiers CSV) -> Cassandra Cluster A.
"""
import pandas as pd
import os
from cassandra.cluster import Cluster
from gevent import monkey
monkey.patch_all()

def run_sftp_etl(folder_path="data_sources/sftp/"):
    """
    Lit les fichiers CSV dans le dossier simulé et les injecte dans le Cluster A.
    """
    print(f"📁 Lecture du dossier SFTP : {folder_path}...")
    
    try:
        # Liste tous les fichiers CSV dans le dossier
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        
        if not files:
            print("⚠️ Aucun fichier CSV trouvé dans le dossier SFTP.")
            return True

        cluster = Cluster(['127.0.0.1'], port=9042)
        session = cluster.connect('univ_boursiers')

        insert_stmt = session.prepare("""
            INSERT INTO boursiers 
            (id_bourse, nom, prenom, sexe, date_naissance, annee_academique, 
             type_bourse, code_formation, cycle, niveau)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)

        total_rows = 0
        for file in files:
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            
            for _, row in df.iterrows():
                session.execute(insert_stmt, (
                    int(row['id_bourse']),
                    str(row['nom']),
                    str(row['prenom']),
                    str(row['sexe']),
                    pd.to_datetime(row['date_naissance']).date(),
                    str(row['annee_academique']),
                    str(row['type_bourse']),
                    str(row['code_formation']),
                    str(row['cycle']),
                    str(row['niveau'])
                ))
            total_rows += len(df)
            print(f"📑 Fichier traité : {file} ({len(df)} lignes)")

        print(f"🚀 Fin de synchro SFTP : {total_rows} boursiers ajoutés au Cluster A.")
        cluster.shutdown()
        return True

    except Exception as e:
        print(f"❌ Erreur ETL SFTP : {e}")
        return False

if __name__ == "__main__":
    run_sftp_etl()