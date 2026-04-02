import streamlit as st
from interfaces import home, ingestion, analytics, crud_admin

st.set_page_config(page_title="RDHA Platform", layout="wide", page_icon="🛡️")

# Barre latérale pro
st.sidebar.title("🛡️ RDHA Navigation")
selection = st.sidebar.radio("Navigation", 
    ["🏠 Accueil & Infra", "🚀 Console Ingestion", "📊 Dashboard BI", "✍️ Gestion CRUD"])

# Routage dynamique
if selection == "🏠 Accueil & Infra":
    home.show()
elif selection == "🚀 Console Ingestion":
    # C'EST ICI QU'ON CHANGE :
    ingestion.show()  
elif selection == "📊 Dashboard BI":
    analytics.show() # Assure-toi que analytics.py a aussi une fonction show()
elif selection == "✍️ Gestion CRUD":
    crud_admin.show() # Même chose ici