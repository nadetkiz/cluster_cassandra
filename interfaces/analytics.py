import streamlit as st
import pandas as pd
import plotly.express as px
from cassandra.cluster import Cluster

def get_all_data(port, keyspace, table):
    """
    Récupère les données d'un cluster Cassandra et sécurise le format pour Streamlit.
    
    Logique :
    - Connexion au cluster spécifique (9043 ou 9044).
    - Conversion des types 'Date' de Cassandra en 'String' pour éviter le crash PyArrow.
    - Gestion des erreurs de connexion pour éviter de bloquer toute l'interface.
    """
    try:
        # Configuration de la connexion
        cluster = Cluster(['127.0.0.1'], port=port)
        session = cluster.connect(keyspace)
        
        # Extraction totale
        query = f"SELECT * FROM {table}"
        rows = session.execute(query)
        df = pd.DataFrame(list(rows))
        cluster.shutdown()

        if not df.empty:
            # FIX TECHNIQUE : Streamlit ne supporte pas nativement le type Date de Cassandra
            for col in df.columns:
                if 'date' in col.lower():
                    df[col] = df[col].astype(str)
        return df
    except Exception as e:
        st.error(f"Erreur de lecture sur le port {port} : {e}")
        return pd.DataFrame()

def show():
    """
    Interface principale de la page Analytics.
    Organisée en deux sections : Scolarité (PostgreSQL) et Finance (API JSON).
    """
    st.title("📊 Analyse Globale des Clusters")
    st.markdown("---")

    # =========================================================================
    # SECTION 1 : CLUSTER B (Scolarité - Sync PostgreSQL)
    # =========================================================================
    st.header("🐘 Scolarité - Source : PostgreSQL")
    
    # Récupération des données (Port 9043)
    df_scolarite = get_all_data(9043, 'univ_sync', 'etudiants_inscrits')

    if not df_scolarite.empty:
        # A. Aperçu Tabulaire
        st.subheader(f"📋 Registre des inscriptions ({len(df_scolarite)} lignes)")
        st.dataframe(df_scolarite.head(20), width="stretch")
        
        st.write("") # Espacement

        # B. Analyse Graphique (Histogramme global)
        st.subheader("📈 Répartition par Formation")
        
        # Note : On utilise 'code_formation' car 'filiere' est absent de tes logs Cassandra
        target_col = 'code_formation' 
        
        if target_col in df_scolarite.columns:
            fig_insc = px.histogram(
                df_scolarite, 
                x=target_col, 
                title=f"Effectifs par {target_col.replace('_', ' ').capitalize()}",
                color_discrete_sequence=['#3366CC'],
                template="plotly_white"
            )
            fig_insc.update_layout(bargap=0.2)
            st.plotly_chart(fig_insc, width="stretch")
            st.caption(f"💡 Analyse basée sur 100% des données du Cluster B.")
        else:
            st.warning(f"La colonne '{target_col}' n'existe pas. Colonnes trouvées : {list(df_scolarite.columns)}")
            
    else:
        st.warning("⚠️ Cluster B : Aucune donnée trouvée. Vérifiez la synchronisation PostgreSQL.")

    st.divider()

    # =========================================================================
    # SECTION 2 : CLUSTER C (Finances - Sync API JSON)
    # =========================================================================
    st.header("🌐 Finance - Source : API JSON")
    
    # Récupération des données (Port 9044)
    df_finance = get_all_data(9044, 'univ_analytics', 'paiements_etudiants')

    if not df_finance.empty:
        # A. Aperçu Tabulaire
        st.subheader(f"💰 Journal des flux financiers ({len(df_finance)} transactions)")
        st.dataframe(df_finance.head(20), width="stretch")
        
        st.write("")

        # B. Analyse Graphique (Donut Chart pour les statuts)
        st.subheader("📈 État Global des Encaissements")
        
        # Vérification du nom de colonne pour le statut (ex: 'statut' ou 'status')
        target_finance = 'statut'
        
        if target_finance in df_finance.columns:
            df_stat_fin = df_finance[target_finance].value_counts().reset_index()
            df_stat_fin.columns = [target_finance, 'Nombre']
            
            fig_pie = px.pie(
                df_stat_fin, 
                values='Nombre', 
                names=target_finance,
                hole=0.4,
                title="Proportion des statuts de paiement",
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pie, width="stretch")
        else:
            st.info(f"Colonne '{target_finance}' non trouvée dans le Cluster C. Colonnes : {list(df_finance.columns)}")
            
    else:
        st.warning("⚠️ Cluster C : Aucune donnée de paiement trouvée. Vérifiez le serveur API JSON.")