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

# Das Eingabefeld
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
    random.seed(42)
    
    for i in range(anzahl_tage):
        basis_preis = 649 - (i * (649 - 579) / anzahl_tage)
        rauschen = random.uniform(-5, 5)
        aktueller_preis = basis_preis + rauschen
        
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
    if "quick" in suchbegriff.lower() or "cassiopea" in suchbegriff.lower() or "3004" in suchbegriff:
        
        st.markdown("### Aktuelle Suche: **Quick Mill Cassiopea 3004 (glänzend)**")
        
        # Aufteilung: Links Stammdaten & Bild, Rechts Webshops
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.info("📦 **Geizhals Stammdaten**")
            
            # Bild aus Wikimedia
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/d/d9/Espresso_machine_with_portafilter.jpg", 
                width=400, 
                caption="Klassische Siebträgermaschine aus Edelstahl (Edelstahl glänzend)"
            )
            
            # Stammdaten Tabelle
            stammdaten = {
                "Eigenschaft": ["System", "Aufheizzeit", "Pumpe", "Siebträger", "Gelistet seit", "UVP"],
                "Wert": ["Dual-Thermoblock", "Unter 5 Minuten", "Vibrationspumpe (15 bar)", "58 mm Standard", "Oktober 2014", "749,00 €"]
            }
            st.table(pd.DataFrame(stammdaten))
            
            # Preisverlauf
            st.markdown("**Preisverlauf auf Tagesebene (Letzte 12 Monate):**")
            df_tagesverlauf = generiere_tages_preise()
            st.line_chart(df_tagesverlauf)

        with col2:
            st.success("🏪 **Gefundene Angebote in deutschen Webshops**")
            st.caption("Kompakte Listenansicht unabhängiger deutscher Händler.")
            
            # Alle Angebote als saubere Datenliste definieren
            alle_shops = [
                {"Shop": "Kaffee24.de", "Preis": "579,00 €", "Versand": "0,00 €", "Verfügbarkeit": "1-3 Werktage", "Link": "https://www.kaffee24.de/quick-mill-cassiopea-3004-espressomaschine-glaenzend"},
                {"Shop": "Stoll-Espresso.de", "Preis": "649,00 €", "Versand": "4,90 €", "Verfügbarkeit": "2-4 Werktage", "Link": "#"},
                {"Shop": "Roastmarket.de", "Preis": "679,00 €", "Versand": "0,00 €", "Verfügbarkeit": "Sofort lieferbar", "Link": "#"},
                {"Shop": "Espressissimo.de", "Preis": "685,00 €", "Versand": "5,90 €", "Verfügbarkeit": "3-5 Werktage", "Link": "#"},
                {"Shop": "Moba-Coffee.de", "Preis": "699,00 €", "Versand": "0,00 €", "Verfügbarkeit": "1-2 Werktage", "Link": "#"},
                {"Shop": "CremaVending.de", "Preis": "719,00 €", "Versand": "4,90 €", "Verfügbarkeit": "Lieferzeit auf Anfrage", "Link": "#"}
            ]
            
            # Header
