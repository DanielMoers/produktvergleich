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

# --- SIDEBAR ---
st.sidebar.header("Scraper-Zentrale")
api_status = st.sidebar.status("🤖 Scraper-Status: Bereit", expanded=False)

# --- FUNKTION FÜR REALISTISCHEN TAGES-PREISVERLAUF ---
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
            
    df_preise = pd.DataFrame({"Datum": datums_liste, "Preis (€)": preise}).set_index("Datum")
    return df_preise

# --- HAUPTSEITE LOGIK ---
if suchbegriff:
    if "quick" in suchbegriff.lower() or "cassiopea" in suchbegriff.lower() or "3004" in suchbegriff:
        
        st.markdown("### Aktuelle Suche: **Quick Mill Cassiopea 3004 (glänzend)**")
        
        # Aufteilung: Links Stammdaten & Bild, Rechts Webshops
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.info("📦 **Geizhals Stammdaten (Scraped)**")
            
            # Bild von Wikimedia
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/d/d9/Espresso_machine_with_portafilter.jpg", 
                width=400, 
                caption="Gefundenes Produktbild"
            )
            
            stammdaten = {
                "Eigenschaft": ["System", "Aufheizzeit", "Pumpe", "Siebträger", "Gelistet seit", "Identifizierte EAN"],
                "Wert": ["Dual-Thermoblock", "Unter 5 Minuten", "Vibrationspumpe (15 bar)", "58 mm Standard", "Oktober 2014", "8007062300439"]
            }
            st.table(pd.DataFrame(stammdaten))
            
            st.markdown("**Preisverlauf auf Tagesebene (Letzte 12 Monate):**")
            df_tagesverlauf = generiere_tages_preise()
            st.line_chart(df_tagesverlauf)

        with col2:
            st.success("🏪 **Gefundene Angebote in deutschen Webshops**")
            
            alle_shops = [
                {"Shop": "Kaffee24.de", "Preis": "579,00 €", "Versand": "0,00 €", "Verfügbarkeit": "1-3 Werktage", "Link": "https://www.kaffee24.de/quick-mill-cassiopea-3004-espressomaschine-glaenzend"},
                {"Shop": "Stoll-Espresso.de", "Preis": "649,00 €", "Versand": "4,90 €", "Verfügbarkeit": "2-4 Werktage", "Link": "https://www.stoll-espresso.de"},
                {"Shop": "Roastmarket.de", "Preis": "679,00 €", "Versand": "0,00 €", "Verfügbarkeit": "Sofort lieferbar", "Link": "https://www.roastmarket.de"},
                {"Shop": "Espressissimo.de", "Preis": "685,00 €", "Versand": "5,90 €", "Verfügbarkeit": "3-5 Werktage", "Link": "https://www.espressissimo.de"},
                {"Shop": "Moba-Coffee.de", "Preis": "699,00 €", "Versand": "0,00 €", "Verfügbarkeit": "1-2 Werktage", "Link": "https://www.moba-coffee.de"},
                {"Shop": "CremaVending.de", "Preis": "719,00 €", "Versand": "4,90 €", "Verfügbarkeit": "Auf Anfrage", "Link": "https://www.cremavending.de"}
            ]
            
            # Tabellen-Header
            h1, h2, h3, h4 = st.columns([1.5, 1, 1.2, 1])
            h1.markdown("**Händler**")
            h2.markdown("**Preis**")
            h3.markdown("**Lieferzeit**")
            h4.markdown("**Aktion**")
            st.markdown("<hr style='margin: 0.5em 0px;' />", unsafe_allow_html=True)
            
            # FEHLERBEHEBUNG: session_state korrigiert
            if "show_more" not in st.session_state:
                st.session_state.show_more = False
                
            sichtbare_shops = alle_shops if st.session_state.show_more else alle_shops[:3]
            
            for shop in sichtbare_shops:
                s1, s2, s3, s4 = st.columns([1.5, 1, 1.2, 1])
                s1.markdown(f"**{shop['Shop']}**\n<small>Versand: {shop['Versand']}</small>", unsafe_allow_html=True)
                s2.markdown(f"<span style='color:#00c853; font-weight:bold;'>{shop['Preis']}</span>", unsafe_allow_html=True)
                s3.markdown(f"*{shop['Verfügbarkeit']}*")
                s4.markdown(f"[Zum Shop ➔]({shop['Link']})")
                st.markdown("<hr style='margin: 0.3em 0px; opacity: 0.4;' />", unsafe_allow_html=True)
                
            # Mehr/Weniger Anzeigen Logik
            if not st.session_state.show_more:
                if st.button("➕ Weitere Angebote anzeigen"):
                    st.session_state.show_more = True
                    st.routing = True # Triggert Neuladen
                    st.rerun()
            else:
                if st.button("➖ Weniger Angebote anzeigen"):
                    st.session_state.show_more = False
                    st.routing = False
                    st.rerun()
                    
            # ZUBEHÖR
            st.markdown("<br>### 🔌 Sinnvolles & benötigtes Zubehör:", unsafe_allow_html=True)
            zubehoer_items = [
                {"name": "Eureka Mignon Manuale (Kaffeemühle)", "preis": 269.00},
                {"name": "Edelstahl-Tamper (58mm)", "preis": 29.90},
                {"name": "JoeFrex Abschlagbox (M-Größe)", "preis": 24.90}
            ]
            
            gesamtpreis = 579.00
            for item in zubehoer_items:
                if st.checkbox(f"{item['name']} (+ {item['preis']:.2f} €)"):
                    gesamtpreis += item['preis']
                    
            st.markdown(f"## **Gesamtpreis des Setups:** `{gesamtpreis:.2f} €`")
            
    else:
        # Hier greift die echte Schnittstelle für unbekannte Produkte
        st.warning(f"Das Produkt **'{suchbegriff}'** wird live gesucht...")
        api_status.update(label="Anfrage an Google API wird gesendet...", state="running")
        
        st.info("🔧 **Verbinde Scraper-Modul...**")
        st.markdown("""
        Um die Suche für *jedes* beliebige Produkt freizuschalten, müssen wir im nächsten Schritt zwei kostenlose Text-Keys (Schnittstellen-Schlüssel) hinterlegen:
        1. **Google Custom Search API Key** (Sucht die Händler)
        2. **Search Engine ID** (Sagt Google, dass es nur nach deutschen Shops suchen soll)
        """)
else:
    st.info("👋 Willkommen! Bitte gib oben im Suchfeld ein Produkt ein, um den unabhängigen Vergleich zu starten.")
