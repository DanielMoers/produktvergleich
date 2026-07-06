import streamlit as st
import pandas as pd
import random
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

# --- FUNKTION FÜR TAGES-PREISVERLAUF (12 MONATE ohne externe Bibliotheken) ---
def generiere_tages_preise():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Datums-Reihe auf Tagesbasis erstellen
    datums_liste = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Realistischen Trend von ~649€ auf ~579€ berechnen
    anzahl_tage = len(datums_liste)
    preise = []
    
    # Fixer Start-Zufallswert, damit der Graph bei jedem Neuladen gleich aussieht
    random.seed(42)
    
    for i in range(anzahl_tage):
        # Linearer Abfall von 649 auf 579
        basis_preis = 649 - (i * (649 - 579) / anzahl_tage)
        # Kleines tägliches Rauschen (+/- 4 Euro)
        rauschen = random.uniform(-4, 4)
        aktueller_preis = basis_preis + rauschen
        
        # Ein paar künstliche Rabatt-Ausreißer einbauen
        if i in [50, 120, 230, 310]:
            aktueller_preis -= 35
            
        preise.append(round(aktueller_preis, 2))
            
    df_preise = pd.DataFrame({
        "Datum": datums_liste,
        "Preis (€)": preise
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
            
            # Ein absolut stabiles Platzhalter-Bild von Unsplash (Kaffee-Thema), das garantiert lädt
            st.image("https://images.unsplash.com/photo-1517256064527-09c53b2d0c6b?w=500", width=400, caption="Quick Mill Cassiopea 3004 – Edelstahl")
            
            # Stammdaten inklusive Erscheinungsdatum
            stammdaten = {
                "Eigenschaft": ["System", "Aufheizzeit", "Pumpe", "Siebträger", "Gelistet seit / Erschienen", "UVP"],
                "Wert": ["Dual-Thermoblock", "Unter 5 Minuten", "Vibrationspumpe (15 bar)", "58 mm Standard", "Oktober 2014 (Modellpflege 2022)", "749,00 €"]
            }
            st.table(pd.DataFrame(stammdaten))
            
            # Preisverlauf tagesgenau über 12 Monate
            st.markdown("**Preisverlauf auf Tagesebene (Letzte 12 Monate):**")
            df_tagesverlauf = generiere_tages_preise()
            st.line_chart(df_tagesverlauf)

        with col2:
            st.success("🏪 **Gefundene Angebote in deutschen Webshops**")
            
            shops = [
                {"Shop": "Kaffee24.de", "Preis": "579,00 €", "Verfügbarkeit": "Sofort lieferbar (1-3 Tage)", "Link": "https://www.kaffee24.de/quick-mill-cassiopea-3004-espressomaschine-glaenzend"},
                {"Shop": "Stoll-Espresso.de", "Preis": "649,00 €", "Verfügbarkeit": "Lieferzeit 2-4 Tage", "Link": "#"},
                {"Shop": "Roastmarket.de", "Preis": "679,00 €", "Verfügbarkeit": "Sofort lieferbar", "Link": "#"}
            ]
            
            for shop in shops:
                with st.container():
                    s1, s2 = st.columns([2, 1])
                    s1.markdown(f"### **{shop['Shop']}**\nPreis: **{shop['Preis']}** | *{shop['Verfügbarkeit']}*")
                    s2.markdown(f"\n\n[Zum Shop ➔]({shop['Link']})")
                    st.markdown("---")
                    
            # ZUBEHÖR
            st.markdown("### 🔌 Sinnvolles & benötigtes Zubehör:")
            zubehoer_items = {
                "Eureka Mignon Manuale (Kaffeemühle)": 269.00,
                "Edelstahl-Tamper (58mm)": 29.90,
                "JoeFrex Abschlagbox (M-Größe)": 24.90
            }
            
            gesamtpreis = 579.00
            for item, preis in zubehoer_items.items():
                if st.checkbox(f"{item} (+ {preis:.2f} €)"):
                    gesamtpreis += preis
                    
            st.markdown(f"## **Gesamtpreis des Setups:** `{gesamtpreis:.2f} €`")
            
    else:
        st.warning(f"Das Produkt **'{suchbegriff}'** wurde im Demomodus nicht gefunden.")
        st.info("💡 Gib 'Quick Mill' ein, um die Live-Demo zu sehen.")
else:
    st.info("👆 Bitte gib oben in das Suchfeld ein Produkt ein (z.B. 'Quick Mill'), um den Vergleicher zu starten.")
