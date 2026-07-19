import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analyseur Loto Pro", page_icon="🎲", layout="wide")
st.title("📊 Analyseur Statistique & Écarts du Loto")

st.sidebar.header("Configuration des données")
st.sidebar.write("Modifiez les tirages ci-dessous :")

tirages_input = st.sidebar.text_area(
    "Entrez un tirage par ligne (5 numéros séparés par des espaces) :",
    value="5 12 24 36 41\n1 12 18 24 45\n5 9 14 36 49\n12 22 31 41 44\n2 5 18 29 36",
    height=150
)

try:
    lignes = tirages_input.strip().split('\n')
    historique_tirages = [[int(n) for n in ligne.split()] for ligne in lignes if ligne.strip()]
    
    if historique_tirages:
        stats = {}
        for num in range(1, 50):
            ecart = 0
            sorti = False
            sorties_totales = 0
            
            for i, tirage in enumerate(historique_tirages):
                if num in tirage:
                    sorties_totales += 1
                    if not sorti:
                        ecart = i
                        sorti = True
            
            if not sorti:
                ecart = len(historique_tirages)
                
            forme = (sorties_totales / len(historique_tirages)) * 100
            
            stats[num] = {
                "Numéro": num,
                "Écart Actuel": ecart,
                "Nombre de Sorties": sorties_totales,
                "Forme (%)": f"{forme:.0f}%"
            }
            
        df_stats = pd.DataFrame(stats).T
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Tableau Général des Numéros (1 à 49)")
            st.dataframe(df_stats, use_container_width=True, hide_index=True)
            
        with col2:
            st.subheader("🔥 Les plus en Forme")
            top_forme = df_stats.sort_values(by="Nombre de Sorties", ascending=False).head(5)
            for _, row in top_forme.iterrows():
                if row['Nombre de Sorties'] > 0:
                    st.success(f"Numéro **{row['Numéro']}** — Sorti {row['Nombre de Sorties']} fois")
            
            st.subheader("⏳ Les plus gros Écarts")
            top_ecart = df_stats.sort_values(by="Écart Actuel", ascending=False).head(5)
            for _, row in top_ecart.iterrows():
                st.warning(f"Numéro **{row['Numéro']}** — Écart de {row['Écart Actuel']} tirage(s)")

except Exception as e:
    st.error(f"Erreur : {e}")


