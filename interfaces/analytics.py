import streamlit as st
import pandas as pd
import plotly.express as px
# from cassandra.cluster import Cluster

def show():
    st.title("📊 Dashboard BI & Analytics")
    st.markdown("Analyse croisée des données issues des 3 clusters distribués.")

    # --- FILTRES DE HAUT DE PAGE ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Filtres Globaux")
    annee = st.sidebar.selectbox("Année Académique", ["2023-2024", "2024-2025"])
    faculte = st.sidebar.multiselect("Faculté", ["Informatique", "Gestion", "Droit"], default=["Informatique"])

    st.divider()

    # --- ZONE 1 : LES INDICATEURS (KPIs) ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Étudiants", "1,250", "+5%")
    c2.metric("Taux de Boursiers", "18%", "-2%")
    c3.metric("Recouvrement", "85%", "+10%")
    c4.metric("Alertes Retard", "42", "⚠️")

    st.divider()

    # --- ZONE 2 : ANALYSE VISUELLE ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🎓 Inscriptions par Niveau (Cluster B)")
        # Simulation de données dénormalisées
        data_inscriptions = pd.DataFrame({
            'Niveau': ['L1', 'L2', 'L3', 'M1', 'M2'],
            'Effectif': [450, 320, 280, 120, 80]
        })
        fig1 = px.bar(data_inscriptions, x='Niveau', y='Effectif', 
                     color='Effectif', color_continuous_scale='Blues',
                     template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        st.subheader("💰 État des Paiements (Cluster C)")
        data_paiements = pd.DataFrame({
            'Statut': ['Soldé', 'Avance', 'Impayé'],
            'Nombre': [800, 300, 150]
        })
        fig2 = px.pie(data_paiements, values='Nombre', names='Statut', 
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # --- ZONE 3 : LE CROISEMENT (Le point fort du SID) ---
    st.subheader("🔄 Analyse Croisée : Impact des Bourses sur les Paiements")
    st.caption("Données fusionnées entre Cluster A (SFTP) et Cluster C (API)")
    
    # Simulation d'un croisement
    data_cross = pd.DataFrame({
        'Type': ['Boursiers', 'Non-Boursiers'],
        'Taux Recouvrement (%)': [98, 72]
    })
    fig3 = px.line(data_cross, x='Type', y='Taux Recouvrement (%)', markers=True)
    st.plotly_chart(fig3, use_container_width=True)