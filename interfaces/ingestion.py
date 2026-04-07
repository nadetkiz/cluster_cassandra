import streamlit as st
import time

def show():
    st.title("🚀 Console d'Ingestion & Monitoring")
    st.markdown("Gérez vos flux de données et surveillez l'état des clusters en temps réel.")

    # --- SECTION 1 : DASHBOARD DE FLUX (METRICS) ---
    st.subheader("📊 Statistiques Globales des Données")
    
    # Création des 5 colonnes pour les widgets
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        st.metric(label="👨‍🎓 Étudiants", value="1,240", delta="Total")
    with m2:
        st.metric(label="📝 Inscriptions", value="850", delta="Cluster B", delta_color="normal")
    with m3:
        st.metric(label="💰 Paiements", value="42M FG", delta="Cluster C")
    with m4:
        st.metric(label="🎓 Formations", value="12", delta="Actives")
    with m5:
        st.metric(label="🎗️ Boursiers", value="156", delta="Cluster A", delta_color="normal")

    st.divider()

    # --- SECTION 2 : PILOTAGE DES PIPELINES ---
    st.subheader("⚙️ Exécution des Pipelines ETL")

    # Pipeline 1 : PostgreSQL
    with st.expander("🐘 Source : PostgreSQL (Scolarité)", expanded=True):
        col_t, col_b = st.columns([3, 1])
        with col_t:
            st.write("**Cible :** `cluster-b-node1` | **Keyspace :** `univ_sync`")
            st.caption("Synchronisation des données d'inscription et des niveaux d'études.")
        with col_b:
            if st.button("Lancer Sync SQL", key="btn_sql", use_container_width=True):
                run_pipeline("PostgreSQL", "B")

    # Pipeline 2 : API JSON
    with st.expander("🌐 Source : API JSON (Paiements Live)"):
        col_t, col_b = st.columns([3, 1])
        with col_t:
            st.write("**Cible :** `cluster-c-node1` | **Keyspace :** `analytics`")
            st.caption("Récupération des flux financiers via l'API Flask.")
        with col_b:
            if st.button("Lancer Sync API", key="btn_api", use_container_width=True):
                run_pipeline("API JSON", "C")

    # Pipeline 3 : SFTP / CSV
    with st.expander("📁 Source : SFTP & CSV (Bourses Externes)"):
        col_t, col_b = st.columns([3, 1])
        with col_t:
            st.write("**Cible :** `cluster-a-node1` | **Keyspace :** `staging`")
            st.caption("Traitement des fichiers plats pour la gestion des bourses.")
        with col_b:
            if st.button("Lancer Sync Fichiers", key="btn_files", use_container_width=True):
                run_pipeline("SFTP/CSV", "A")

def run_pipeline(source_name, cluster_letter):
    """Logique d'affichage des logs et de la progression"""
    st.markdown(f"**Action :** Ingestion depuis {source_name} vers Cluster {cluster_letter}...")
    progress_bar = st.progress(0)
    log_area = st.empty()
    
    logs = []
    def log(msg):
        logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        log_area.code("\n".join(logs))

    # Étapes simulées (à lier à tes connecteurs plus tard)
    log("Initialisation du pipeline...")
    time.sleep(0.5)
    progress_bar.progress(25)
    
    log(f"Extraction des données source ({source_name})...")
    time.sleep(0.8)
    progress_bar.progress(50)
    
    log(f"Dénormalisation et injection dans Cassandra (Port 904{cluster_letter.lower()})...")
    time.sleep(1)
    progress_bar.progress(85)
    
    log("Finalisation et indexation...")
    time.sleep(0.5)
    progress_bar.progress(100)
    
    st.success(f"Pipeline {source_name} terminé avec succès !")
    st.balloons() # Petit effet visuel pour le succès