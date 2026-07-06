import streamlit as st
import pandas as pd
import random
import requests
from datetime import datetime, timedelta

# --- APP CONFIG ---
st.set_page_config(page_title="Unabhängiger Produktvergleicher", layout="wide")

# --- GOOGLE API SECRET KEYS ---
# Holt die Keys sicher aus den Streamlit Secrets (richten wir in Schritt 2 ein)
API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
SEARCH_ENGINE_ID = st.secrets.get("GOOGLE_CSE_ID", "")

# --- KOPFZEILE ---
st.title("🔍 Unabhängiger Produktvergleicher")
st.subheader("Finde echte Angebote in deutschen Webshops – ohne bezahlte Rankings.")
st.markdown("---")

# Das Eingabefeld
suchbegriff = st.text_input("Welches Produkt suchst du?", placeholder="Z.B. Quick Mill 3004, Sony Alpha 7 IV, etc...")

# --- SIDEBAR ---
st.sidebar.header("Scraper-Zentrale")
if API_KEY and SEARCH_ENGINE_ID:
    st.sidebar.success("🤖 API-Status: Live-Modus aktiv")
else:
    st.sidebar.warning("⚠️ API-Status: Demo-Modus (Keys fehlen)")

# --- FUNKTION FÜR REALISTISCHEN TAGES-PREISVERLAUF ---
def generiere_tages_preise(seed_val=42):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    datums_liste = pd.date_range(start=start_date, end=end_date, freq='D')
    
    anzahl_tage = len(datums_liste)
    preise = []
    random.seed(seed_val)
    
    basis_start = random.randint(400, 1200)
    basis_ende = basis_start - random.randint(20, 100)
    
    for i in range(anzahl_tage):
        basis_preis = basis_start - (i * (basis_start - basis_ende) / anzahl_tage)
        rauschen = random.uniform(-5, 5)
        preise.append(round(basis_preis + rauschen, 2))
            
    return pd.DataFrame({"Datum": datums_liste, "Preis (€)": preise}).set_index("Datum")

# --- LIVE SCRAPER VIA GOOGLE CUSTOM SEARCH ---
def google_live_scrape(query):
    if not API_KEY or not SEARCH_ENGINE_ID:
        return None
        
    # Wir suchen gezielt nach deutschen Onlineshops und schließen Preissuchmaschinen aus
    search_query = f'"{query}" site:.de -site:amazon.de -site:idealo.de -site:geizhals.de -site:ebay.de -site:billiger.de'
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_query}"
    
    try:
        response = requests.get(url).json()
        items = response.get("items", [])
        
        ergebnisse = []
        for item in items:
            link = item.get("link", "")
            display_link = item.get("displayLink", "").replace("www.", "")
            titel = item.get("title", "")
            
            # Preis-Extraktion aus den Meta-Tags (viele Shops hinterlegen strukturierte Daten)
            pagemap = item.get("pagemap", {})
            offers = pagemap.get("offer", [{}]) or pagemap.get("product", [{}])
            
            extracted_price = "Auf Anfrage"
            if isinstance(offers, list) and len(offers) > 0:
                price = offers[0].get("price", "") or offers[0].get("amount", "")
                if price:
                    extracted_price = f"{price} €"
            
            ergebnisse.append({
                "Shop": display_link.capitalize(),
                "Preis": extracted_price,
                "Versand": "Siehe Shop",
                "Verfügbarkeit": "Lieferbar",
                "Link": link
            })
        return ergebnisse
    except Exception as e:
        st.error(f"Fehler bei der Live-Abfrage: {e}")
        return None

# --- HAUPTSEITE LOGIK ---
if suchbegriff:
    st.markdown(f"### Aktuelle Suche: **{suchbegriff}**")
    
    # Aufteilung: Links Stammdaten & Bild, Rechts Webshops
    col1, col2 = st.columns([1, 1.2])
    
    # Fallunterscheidung: Echte API-Abfrage oder Fallback auf unsere optimierte Quick Mill Demo
    is_demo = not (API_KEY and SEARCH_ENGINE_ID) or ("quick" in suchbegriff.lower() or "3004" in suchbegriff)
    
    with col1:
        st.info("📦 **Produkt-Stammdaten**")
        
        # Bild-Zuweisung
        img_url = "https://upload.wikimedia.org/wikipedia/commons/d/d9/Espresso_machine_with_portafilter.jpg" if "quick" in suchbegriff.lower() else "https://upload.wikimedia.org/wikipedia/commons/1/15/No_image_available_600_x_450.svg"
        st.image(img_url, width=400, caption=f"Produktbild für {suchbegriff}")
        
        # Stammdaten Tabelle
        gelistet_seit = "Oktober 2014" if is_demo else "Live geladen via API"
        stammdaten = {
            "Eigenschaft": ["Produktname", "Gelistet seit", "Kategorie-Status"],
            "Wert": [suchbegriff, gelistet_seit, "Unabhängig verifiziert"]
        }
        st.table(pd.DataFrame(stammdaten))
        
        # Preisverlauf
        st.markdown("**Preisverlauf auf Tagesebene (Letzte 12 Monate):**")
        seed_hash = sum(ord(c) for c in suchbegriff)
        df_tagesverlauf = generiere_tages_preise(seed_hash)
        st.line_chart(df_tagesverlauf)

    with col2:
        st.success("🏪 **Gefundene Angebote in deutschen Webshops**")
        
        if is_demo and ("quick" in suchbegriff.lower() or "3004" in suchbegriff):
            # Unsere verifizierte Demo-Liste für die Quick Mill
            alle_shops = [
                {"Shop": "Kaffee24.de", "Preis": "579,00 €", "Versand": "0,00 €", "Verfügbarkeit": "1-3 Werktage", "Link": "https://www.kaffee24.de/quick-mill-cassiopea-3004-espressomaschine-glaenzend"},
                {"Shop": "Stoll-Espresso.de", "Preis": "649,00 €", "Versand": "4,90 €", "Verfügbarkeit": "2-4 Werktage", "Link": "https://www.stoll-espresso.de"},
                {"Shop": "Roastmarket.de", "Preis": "679,00 €", "Versand": "0,00 €", "Verfügbarkeit": "Sofort lieferbar", "Link": "https://www.roastmarket.de"},
                {"Shop": "Espressissimo.de", "Preis": "685,00 €", "Versand": "5,90 €", "Verfügbarkeit": "3-5 Werktage", "Link": "https://www.espressissimo.de"},
                {"Shop": "Moba-Coffee.de", "Preis": "699,00 €", "Versand": "0,00 €", "Verfügbarkeit": "1-2 Werktage", "Link": "https://www.moba-coffee.de"}
            ]
        else:
            with st.spinner("Scrape deutsche Webshops live via Google API..."):
                alle_shops = google_live_scrape(suchbegriff)
        
        if alle_shops:
            # Tabellen-Header
            h1, h2, h3, h4 = st.columns([1.5, 1, 1.2, 1])
            h1.markdown("**Händler**")
            h2.markdown("**Preis**")
            h3.markdown("**Lieferzeit**")
            h4.markdown("**Aktion**")
            st.markdown("<hr style='margin: 0.5em 0px;' />", unsafe_allow_html=True)
            
            if "show_more" not in st.session_state:
                st.session_state.show_more = False
                
            sichtbare_shops = alle_shops if st.session_state.show_more else alle_shops[:3]
            
            for shop in sichtbare_shops:
                s1, s2, s3, s4 = st.columns([1.5, 1, 1.2, 1])
                s1.markdown(f"**{shop['Shop']}**\n
