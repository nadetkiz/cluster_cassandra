import streamlit as st
import docker
import time

# Initialisation du client Docker
try:
    client = docker.from_env()
except Exception as e:
    st.error("Impossible de se connecter à Docker Desktop. Assurez-vous qu'il est lancé.")

# --- CONFIGURATION EXACTE SELON TON YAML ---
NODES = [
    {"name": "Cluster A (Staging)", "port": 9042, "container": "cluster-a-node1", "icon": "📁"},
    {"name": "Cluster B (SQL Sync)", "port": 9043, "container": "cluster-b-node1", "icon": "🗄️"},
    {"name": "Cluster C (Analytics)", "port": 9044, "container": "cluster-c-node1", "icon": "💳"}
]

def get_status(container_name):
    """Récupère le statut sans planter si le conteneur n'existe pas encore"""
    try:
        container = client.containers.get(container_name)
        return container.status
    except docker.errors.NotFound:
        return "not_created"
    except Exception:
        return "error"

def show():
    st.title("🏠 Accueil & Topologie Cluster")
    st.markdown("### Contrôle de l'infrastructure distribuée RDHA")
    st.divider()

    cols = st.columns(3)

    for i, node in enumerate(NODES):
        with cols[i]:
            status = get_status(node["container"])
            
            # --- CAS 1 : LE NOEUD TOURNE ---
            if status == "running":
                st.success(f"### {node['icon']} {node['name']}")
                st.markdown("**Status :** :green[🟢 EN LIGNE]")
                st.caption(f"Port Externe : {node['port']}")
                
                if st.button(f"Arrêter {node['container']}", key=f"stop_{i}"):
                    with st.spinner("Arrêt en cours..."):
                        client.containers.get(node["container"]).stop()
                        st.rerun()

            # --- CAS 2 : LE NOEUD EST ARRÊTÉ ---
            elif status == "exited":
                st.error(f"### {node['icon']} {node['name']}")
                st.markdown("**Status :** :red[🔴 HORS-LIGNE]")
                
                if st.button(f"Démarrer {node['container']}", key=f"start_{i}"):
                    with st.spinner("Démarrage en cours..."):
                        client.containers.get(node["container"]).start()
                        time.sleep(2) # Laisse un peu de temps à Docker
                        st.rerun()

            # --- CAS 3 : LE CONTENEUR N'EXISTE PAS (Erreur de nom ou pas créé) ---
            elif status == "not_created":
                st.warning(f"### {node['icon']} {node['name']}")
                st.write("⚠️ Conteneur non trouvé.")
                st.caption(f"Vérifiez le nom : {node['container']}")
            
            else:
                st.info(f"### {node['icon']} {node['name']}")
                st.write("Statut : Chargement...")

    st.divider()
    
    # Rappel des rôles (Validation du projet)
    st.subheader("📝 Rôles des clusters")
    c1, c2, c3 = st.columns(3)
    c1.info("**Cluster A** : Ingestion des fichiers plats (CSV/SFTP).")
    c2.info("**Cluster B** : Synchronisation des données SQL (Postgres).")
    c3.info("**Cluster C** : Analyse des flux temps-réel (API JSON).")