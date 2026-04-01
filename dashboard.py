import streamlit as st
import pandas as pd
import plotly.express as px
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import time
import logging
from typing import Tuple, Dict, List
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import configparser
import os
from dataclasses import dataclass
from enum import Enum

# --- CONFIGURATION & STYLE ---
st.set_page_config(
    page_title="RDHA Platform", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🚀"
)

# Custom CSS amélioré
st.markdown("""
    <style>
    .status-up { color: #28a745; font-weight: bold; animation: pulse 2s infinite; }
    .status-down { color: #dc3545; font-weight: bold; }
    .card { 
        border-radius: 10px; 
        border: 1px solid #ddd; 
        padding: 15px; 
        margin: 10px 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .card:hover { transform: translateY(-2px); }
    .metric-card {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .log-container {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        height: 300px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENUMS ET DATACLASSES ---
class ClusterType(Enum):
    SCHOLARSHIP = "Bourses"
    REGISTRATION = "Inscriptions"
    PAYMENT = "Paiements"

@dataclass
class ClusterInfo:
    name: str
    port: int
    type: ClusterType
    host: str = '127.0.0.1'

# --- CONFIGURATION ---
class Config:
    def __init__(self):
        self.clusters = [
            ClusterInfo("Cluster A", 9042, ClusterType.SCHOLARSHIP),
            ClusterInfo("Cluster B", 9043, ClusterType.REGISTRATION),
            ClusterInfo("Cluster C", 9044, ClusterType.PAYMENT)
        ]
        self.sftp_config = {
            'host': os.getenv('SFTP_HOST', 'localhost'),
            'port': int(os.getenv('SFTP_PORT', 22)),
            'username': os.getenv('SFTP_USER', 'user'),
            'password': os.getenv('SFTP_PASSWORD', 'password')
        }
        self.postgres_config = {
            'host': os.getenv('PG_HOST', 'localhost'),
            'port': int(os.getenv('PG_PORT', 5432)),
            'database': os.getenv('PG_DB', 'university'),
            'user': os.getenv('PG_USER', 'postgres'),
            'password': os.getenv('PG_PASSWORD', 'password')
        }
        self.api_config = {
            'url': os.getenv('API_URL', 'http://localhost:5000/api/payments'),
            'timeout': int(os.getenv('API_TIMEOUT', 30))
        }

config = Config()

# --- GESTION DES LOGS ---
class LogManager:
    def __init__(self):
        self.logs = []
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def add_log(self, msg: str, level: str = "INFO"):
        timestamp = time.strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {level}: {msg}"
        self.logs.append(log_entry)
        if level == "ERROR":
            logging.error(msg)
        else:
            logging.info(msg)
        return log_entry
    
    def get_logs(self) -> List[str]:
        return self.logs
    
    def clear_logs(self):
        self.logs = []

# --- FONCTIONS AMÉLIORÉES ---
def check_cluster_health(cluster_info: ClusterInfo) -> Tuple[str, str, float]:
    """Vérifie la santé d'un cluster avec temps de réponse"""
    try:
        start_time = time.time()
        cluster = Cluster([cluster_info.host], port=cluster_info.port, connect_timeout=2)
        session = cluster.connect()
        # Test simple de requête
        session.execute("SELECT release_version FROM system.local")
        response_time = time.time() - start_time
        cluster.shutdown()
        return "RUNNING", "✅", response_time
    except Exception as e:
        return "DOWN", "❌", 0.0

def check_all_clusters_parallel() -> Dict[str, Tuple[str, str, float]]:
    """Vérifie tous les clusters en parallèle"""
    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_cluster = {
            executor.submit(check_cluster_health, cluster): cluster.name 
            for cluster in config.clusters
        }
        for future in as_completed(future_to_cluster):
            cluster_name = future_to_cluster[future]
            try:
                results[cluster_name] = future.result()
            except Exception as e:
                results[cluster_name] = ("DOWN", "❌", 0.0)
    return results

def display_cluster_metrics(cluster_statuses: Dict[str, Tuple[str, str, float]]):
    """Affiche les métriques des clusters avec graphiques"""
    cols = st.columns(len(cluster_statuses))
    for idx, (cluster_name, (status, icon, response_time)) in enumerate(cluster_statuses.items()):
        with cols[idx]:
            color = "green" if status == "RUNNING" else "red"
            st.markdown(f"""
            <div class="metric-card">
                <h3>{icon} {cluster_name}</h3>
                <p style="color: {color};">{status}</p>
                <small>Temps réponse: {response_time:.2f}s</small>
            </div>
            """, unsafe_allow_html=True)

# --- ETL FUNCTIONS (SIMULATION) ---
async def run_etl_pipeline(pipeline_type: str, log_manager: LogManager):
    """Exécute un pipeline ETL de manière asynchrone"""
    try:
        log_manager.add_log(f"Démarrage du pipeline {pipeline_type}")
        
        # Simulation de différents temps de traitement
        processing_time = {
            'sftp': 2,
            'postgres': 1.5,
            'api': 1
        }.get(pipeline_type, 1)
        
        await asyncio.sleep(processing_time)
        
        # Logs de succès avec métriques
        if pipeline_type == 'sftp':
            log_manager.add_log(f"✅ Pipeline SFTP terminé en {processing_time}s - 2 fichiers traités")
        elif pipeline_type == 'postgres':
            log_manager.add_log(f"✅ Pipeline PostgreSQL terminé en {processing_time}s - 768 étudiants synchronisés")
        elif pipeline_type == 'api':
            log_manager.add_log(f"✅ Pipeline API terminé en {processing_time}s - Données paiement mises à jour")
            
        return True
    except Exception as e:
        log_manager.add_log(f"❌ Erreur pipeline {pipeline_type}: {str(e)}", "ERROR")
        return False

async def run_all_pipelines(log_manager: LogManager):
    """Exécute tous les pipelines en parallèle"""
    pipelines = ['sftp', 'postgres', 'api']
    tasks = [run_etl_pipeline(pipeline, log_manager) for pipeline in pipelines]
    results = await asyncio.gather(*tasks)
    return all(results)

# --- VALIDATION DES DONNÉES ---
def validate_student_data(nom: str, prenom: str, matricule: str, niveau: str) -> Tuple[bool, str]:
    """Valide les données d'un étudiant"""
    if not nom or not nom.strip():
        return False, "Le nom est requis"
    if not prenom or not prenom.strip():
        return False, "Le prénom est requis"
    if not matricule or not matricule.strip():
        return False, "Le matricule est requis"
    if not niveau:
        return False, "Le niveau est requis"
    
    # Validation du format du matricule
    if not matricule.startswith("ILD-") or len(matricule) < 10:
        return False, "Format de matricule invalide (ex: ILD-2024-001)"
    
    return True, "OK"

# --- INTERFACE UTILISATEUR ---
def page_presentation():
    """Page de présentation améliorée"""
    st.title("🚀 Resilient Data Hub & Analytics (RDHA)")
    st.info("Plateforme d'ingestion et d'analyse distribuée pour l'Université")
    
    # Métriques des clusters avec rafraîchissement automatique
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🏗️ Structure de l'Architecture
        Le projet repose sur 3 piliers fondamentaux :
        
        * **📥 Multi-Source :** Extraction de données **SQL** (Postgres), **JSON** (API Flask), **CSV** et **SFTP**
        * **⚙️ Orchestration :** Moteur ETL Python avec nettoyage et dénormalisation des données
        * **📦 Stockage Distribué :** 3 Clusters Cassandra indépendants pour Haute Disponibilité
        
        ### 📊 Technologies Utilisées
        - **Frontend:** Streamlit, Plotly, Custom CSS
        - **Backend:** Python, Cassandra, PostgreSQL
        - **ETL:** Asyncio, ThreadPoolExecutor
        - **Monitoring:** Logging personnalisé, métriques en temps réel
        """)
    
    with col2:
        st.subheader("🌐 État des Clusters (Live)")
        
        # Auto-refresh option
        auto_refresh = st.checkbox("Auto-refresh (30s)")
        
        cluster_statuses = check_all_clusters_parallel()
        display_cluster_metrics(cluster_statuses)
        
        if auto_refresh:
            time.sleep(30)
            st.experimental_rerun()

def page_ingestion():
    """Page d'ingestion améliorée avec logs détaillés"""
    st.header("🛰️ Orchestrateur de Flux")
    
    # Initialisation du log manager dans session state
    if 'log_manager' not in st.session_state:
        st.session_state.log_manager = LogManager()
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 🎮 Contrôles")
        if st.button("🔄 Lancer la Synchronisation Globale", type="primary"):
            with st.spinner("Exécution des pipelines ETL..."):
                # Exécution asynchrone
                async def run():
                    return await run_all_pipelines(st.session_state.log_manager)
                
                success = asyncio.run(run())
                
                if success:
                    st.success("✅ Tous les pipelines ont été exécutés avec succès !")
                    st.balloons()
                else:
                    st.error("❌ Certains pipelines ont échoué. Vérifiez les logs.")
        
        st.markdown("### ⚙️ Options")
        with st.expander("Options avancées"):
            st.checkbox("Mode debug")
            st.selectbox("Niveau de log", ["INFO", "DEBUG", "ERROR"])
            if st.button("🗑️ Effacer les logs"):
                st.session_state.log_manager.clear_logs()
                st.success("Logs effacés")
    
    with col2:
        st.markdown("### 📋 Console de Logs")
        logs = st.session_state.log_manager.get_logs()
        
        # Container avec hauteur fixe et défilement
        log_container = st.container()
        with log_container:
            if logs:
                log_text = "\n".join(logs)
                st.code(log_text, language="log")
            else:
                st.info("Aucun log pour le moment. Lancez une synchronisation.")
        
        # Métriques de performance
        st.markdown("### 📈 Métriques")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total pipelines", "3")
        with col_b:
            st.metric("Temps moyen", "~1.5s")
        with col_c:
            st.metric("Logs générés", len(logs))

def page_crud():
    """Page CRUD améliorée avec validation et feedback"""
    st.header("✍️ Gestion Manuelle des Données")
    
    # Formulaire d'ajout d'étudiant
    with st.form("add_student", clear_on_submit=True):
        st.subheader("➕ Ajouter un étudiant")
        
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom *", placeholder="Dupont")
            prenom = st.text_input("Prénom *", placeholder="Jean")
            niveau = st.selectbox("Niveau *", ["L1", "L2", "L3", "M1", "M2"])
        
        with col2:
            matricule = st.text_input("Matricule *", placeholder="ILD-2024-001")
            email = st.text_input("Email", placeholder="jean.dupont@univ.fr")
            telephone = st.text_input("Téléphone", placeholder="+33 6 12 34 56 78")
        
        submitted = st.form_submit_button("➕ Enregistrer dans Cassandra", type="primary")
        
        if submitted:
            # Validation
            is_valid, message = validate_student_data(nom, prenom, matricule, niveau)
            
            if not is_valid:
                st.error(f"❌ {message}")
            else:
                try:
                    # Simulation d'insertion dans Cassandra
                    # Ici tu mets ton code réel d'insertion
                    # session.execute("INSERT INTO students ...")
                    
                    st.balloons()
                    st.success(f"✅ L'étudiant {nom} {prenom} a été ajouté au Cluster B")
                    st.info(f"📧 Un email de confirmation sera envoyé à {email if email else 'l\'adresse fournie'}")
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'insertion: {str(e)}")
    
    # Section de recherche
    with st.expander("🔍 Rechercher des étudiants"):
        search_term = st.text_input("Rechercher par nom, prénom ou matricule")
        if search_term:
            st.info(f"Recherche de: {search_term} (simulation)")
            # Simulation de résultats
            st.dataframe(pd.DataFrame({
                'Nom': ['Dupont', 'Martin'],
                'Prénom': ['Jean', 'Marie'],
                'Matricule': ['ILD-2024-001', 'ILD-2024-002'],
                'Niveau': ['L3', 'M1']
            }))
    
    # Statistiques
    st.subheader("📊 Statistiques")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total étudiants", "1,234", "12")
    with col2:
        st.metric("Par niveau L3", "345", "5")
    with col3:
        st.metric("Nouveaux (30j)", "89", "15")

def page_dashboard():
    """Page de dashboard BI améliorée"""
    st.header("📊 Tableau de Bord BI")
    
    # Sélection du cluster
    cluster_selected = st.selectbox(
        "Sélectionner le cluster",
        ["Tous", "Bourses", "Inscriptions", "Paiements"]
    )
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Étudiants", "3,452", "12%")
    with col2:
        st.metric("💰 Bourses Allouées", "1.2M€", "5%")
    with col3:
        st.metric("📝 Inscriptions", "2,891", "8%")
    with col4:
        st.metric("💳 Paiements", "2.1M€", "3%")
    
    # Graphiques
    tab1, tab2, tab3 = st.tabs(["📈 Évolution", "📊 Distribution", "📉 Tendances"])
    
    with tab1:
        # Évolution des inscriptions
        df_evolution = pd.DataFrame({
            'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
            'Inscriptions': [120, 135, 150, 180, 210, 245],
            'Bourses': [85, 92, 98, 105, 112, 118]
        })
        fig = px.line(df_evolution, x='Mois', y=['Inscriptions', 'Bourses'],
                     title='Évolution des Inscriptions et Bourses')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Distribution par niveau
        df_distribution = pd.DataFrame({
            'Niveau': ['L1', 'L2', 'L3', 'M1', 'M2'],
            'Nombre': [450, 380, 320, 280, 210]
        })
        fig = px.pie(df_distribution, values='Nombre', names='Niveau',
                    title='Distribution des Étudiants par Niveau')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Performance de l'infrastructure
        df_perf = pd.DataFrame({
            'Cluster': ['Bourses', 'Inscriptions', 'Paiements'],
            'Latence (ms)': [45, 52, 48],
            'Taux succès (%)': [99.8, 99.9, 99.7]
        })
        fig = px.bar(df_perf, x='Cluster', y='Latence (ms)',
                    title='Latence par Cluster', color='Taux succès (%)')
        st.plotly_chart(fig, use_container_width=True)

# --- MAIN ---
def main():
    # Navigation sidebar améliorée
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
        st.title("RDHA Platform")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Présentation", "🛰️ Ingestion", "📊 Dashboard", "🛠️ CRUD"],
            format_func=lambda x: x.split(" ", 1)[1] if " " in x else x
        )
        
        st.markdown("---")
        st.caption(f"Version 2.0 | {time.strftime('%Y-%m-%d %H:%M')}")
    
    # Routing des pages
    pages = {
        "🏠 Présentation": page_presentation,
        "🛰️ Ingestion": page_ingestion,
        "📊 Dashboard": page_dashboard,
        "🛠️ CRUD": page_crud
    }
    
    pages[page]()

if __name__ == "__main__":
    main()