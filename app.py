import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- APP CONFIG ---
st.set_page_config(page_title="Unabhängiger Produktvergleicher", layout="wide")

# --- KOPFZEILE MIT SUCHFELD ---
st.title("🔍 Unabhängiger Produktvergleicher")
st.subheader("Finde echte Angebote in deutschen Webshops – ohne bezahlte Rankings.")

# Das Eingabefeld in der Kopfzeile
suchbegriff = st.text_input("Welches Produkt suchst du? (z.B. Quick Mill Cassiopea 3004)", placeholder="Produktname oder EAN eingeben...")

# --- NAVIGATION IN DER SIDEBAR ---
kategorie = st.sidebar.selectbox("Produktkategorie filtern:", ["Alle Kategorien", "Kaffeemaschinen & Zubehör", "Fotografie & Video"])

# --- FUNKTION FÜR TAGES-PREISVERLAUF (12 MONATE) ---
def generiere_tages_preise():
    # Enddatum ist heute, Startdatum vor genau 365 Tagen
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Datums-Reihe auf Tagesbasis erstellen
    datums_liste = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Realistischen, leicht schwankenden Preisverlauf simulieren (Trend nach unten von ~650€ auf ~579€)
    np.random.seed(42) # Sorgt dafür, dass der Graph stabil bleibt
    basis_trend = np.linspace(649, 579, len(datums_liste))
    rauschen = np.random.normal(0, 4, len(datums_liste)) # Kleine tägliche Schwankungen
    preise = basis_trend + rauschen
    
    # Einzelne Ausreißer (kurzzeitige Rabattaktionen an bestimmten Tagen) einbauen
    for i in [50, 120, 230, 310]:
        if i < len(preise):
            preise[i] -= 35
            
    df_preise = pd.DataFrame({
        "Datum": datums_liste,
        "Preis (€)": np.round(preise, 2)
    }).set_index("Datum")
    
    return df_preise

# --- HAUPTSEITE / LOGIK ---
if suchbegriff:
    # Überprüfung auf den Suchbegriff
    if "quick mill" in suchbegriff.lower() or "cassiopea" in suchbegriff.lower() or "3004" in suchbegriff:
        
        st.markdown(f"### Aktuelle Suche: **Quick Mill Cassiopea 3004 (glänzend)**")
        
        # Layout aufteilen: Links Stammdaten & Bild, Rechts Webshops
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.info("📦 **Geizhals Stammdaten**")
            
            # WUNSCH: Neues, stabiles Produktbild (Falls Großansicht gewünscht, Breite angepasst)
            st.image("https://images.unsplash.com/photo-1517256064527-09c53b2d0c6b?w=500&auto=format&fit=crop&q=60", width=400, caption="Quick Mill Cassiopea 3004 – Dual-Thermoblock Edelstahl")
            
            # Stammdaten inklusive Erscheinungsdatum
            stammdaten = {
                "Eigenschaft": ["System", "Aufheizzeit", "Pumpe", "Siebträger", "Gelistet seit / Erschienen", "UVP"],
                "Wert": ["Dual-Thermoblock", "Unter 5 Minuten", "Vibrationspumpe (15 bar)", "58 mm Standard", "Oktober 2014 (Modellpflege 2022)", "749,00 €"]
            }
            st.table(pd.DataFrame(stammdaten))
            
            # WUNSCH
