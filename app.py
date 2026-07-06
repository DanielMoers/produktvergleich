import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# --- APP CONFIG ---
st.set_page_config(page_title="Unabhängiger Produktvergleicher", layout="wide")

# --- KOPFZEILE ---
st.title("🔍 Unabhängiger Produktvergleicher")
st.subheader("Finde echte Angebote in deutschen Webshops – ohne bezahlte Rankings.")
st.markdown("---")

# Das Eingabefeld (jetzt prominent platziert)
suchbegriff = st.text_input("Welches Produkt suchst du?", placeholder="Z.B. Quick Mill, Cassiopea oder 3004 eingeben...")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter-Optionen")
kategorie = st.sidebar.selectbox("Produktkategorie filtern:", ["Alle Kategorien", "Kaffeemaschinen & Zubehör", "Fotografie & Video"])

# --- FUNKTION FÜR TAGES-PREISVERLAUF ---
def generiere_tages_preise():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    datums_liste = pd.date_range(start=start_date, end=end_date, freq='D')
    
    anzahl_tage = len(datums_liste)
    preise = []
    random.seed(42) # Hält den Graphen stabil
    
    for i in range(anzahl_tage):
        basis_preis = 649 - (i * (649 - 579) / anzahl_tage)
        rauschen = random.uniform(-5, 5)
        aktueller_preis = basis_preis + rauschen
        
        # Künstliche Rabatt-Tage (Ausreißer nach unten)
        if i in [45, 130, 220, 315]:
            aktueller_preis -= 40
            
        preise.append(round(aktueller_preis, 2))
            
    df_preise = pd.DataFrame({
        "Datum": datums_liste,
        "Preis (€)": preise
    }).set_index("Datum")
    
    return df_preise

# --- HAUPTSEITE LOGIK ---
if suchbegriff:
    # Prüfung auf den Suchbegriff (Quick Mill)
    if "quick" in suchbegriff.lower() or "cassiopea" in suchbegriff.lower() or "3004" in suchbegriff:
        
        st.markdown(f"### Aktuelle Suche: **Quick Mill Cassiopea 3004 (glänzend)**")
        
        # Aufteilung: Links Stammdaten & Bild, Rechts Webshops
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.info("📦 **Geizhals Stammdaten**")
            
            # GARANTIERT STABILES BILD: Offizielle URL aus Wikimedia Commons (Espressomaschine)
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/4/4e/Espressomaschine_Technika_III_2.jpg", 
                width=450, 
                caption="Symbolbild: Klassische Siebträgermaschine aus Edelstahl (Edelstahl glänzend)"
            )
            
            # Stammdaten Tabelle
            stammdaten = {
                "Eigenschaft": ["System", "Aufheizzeit", "Pumpe", "Siebträger", "Gelistet seit / Erschienen", "UVP"],
                "Wert": ["Dual-Thermoblock", "Unter 5 Minuten", "Vibrationspumpe (15 bar)", "58 mm Standard", "Oktober 2014 (Modellpflege 2022)", "749,00 €"]
            }
            st.table(pd.DataFrame(stammdaten))
            
            # Preisverlauf tagesgenau
            st.markdown("**Preisverlauf auf Tagesebene (Letzte 12 Monate):**")
            df_tagesverlauf = generiere_tages_preise()
            st.line_chart(df_tagesverlauf)

        with col2:
            st.success("🏪 **Gefundene Angebote in deutschen Webshops**")
            st.caption("Gefiltert nach Händlern mit deutschem Impressum, ohne bezahlte CPC-Rankings.")
            
            shops = [
                {"Shop": "Kaffee24.de", "Preis": "579,00 €", "Verfügbarkeit": "Sofort lieferbar (1-3 Tage)", "Link": "https://www.kaffee24.de/quick-mill-cassiopea-3004-espressomaschine-glaenzend"},
                {"Shop": "Stoll-Espresso.de", "Preis": "649,00 €", "Verfügbarkeit": "Lieferzeit 2-4 Tage", "Link": "#"},
                {"Shop": "Roastmarket.de", "Preis": "679,00 €", "Verfügbarkeit": "Sofort lieferbar", "Link": "#"}
            ]
            
            for shop in shops:
                with st.container():
                    s1, s2 = st.columns([2, 1])
                    s1.markdown(f"### **{shop
