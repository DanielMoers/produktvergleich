import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Unabhängiger Produktvergleicher", layout="wide")
st.title("🔍 Unabhängiger Produktvergleicher")
st.subheader("Finde echte Angebote in deutschen Webshops – ohne bezahlte Rankings.")

# --- NAVIGATION ---
kategorie = st.sidebar.selectbox("Produktkategorie wählen:", ["Kaffeemaschinen & Zubehör", "Fotografie & Video (Demomodus)"])

# --- HAUPTSEITE ---
if kategorie == "Kaffeemaschinen & Zubehör":
    st.markdown("### Aktuelle Suche: **Quick Mill Cassiopea 3004 (glänzend)**")
    
    # Layout aufteilen: Links Stammdaten, Rechts Webshops
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.info("📦 **Geizhals Stammdaten (Simuliert)**")
        st.image("https://www.quickmill.it/wp-content/uploads/2016/06/3004_retro.jpg", width=250, caption="Quick Mill Cassiopea 3004")
        
        # Stammdaten Tabelle
        stammdaten = {
            "Eigenschaft": ["System", "Aufheizzeit", "Pumpe", "Siebträger", "UVP"],
            "Wert": ["Dual-Thermoblock", "Unter 5 Minuten", "Vibrationspumpe (15 bar)", "58 mm Standard", "749,00 €"]
        }
        st.table(pd.DataFrame(stammdaten))
        
        # Simulierter Preisverlauf
        st.markdown("**Preisverlauf (Letzte 3 Monate):**")
        preis_historie = pd.DataFrame({
            "Datum": ["01.05.", "15.05.", "01.06.", "15.06.", "01.07."],
            "Preis (€)": [680, 650, 630, 599, 579]
        }).set_index("Datum")
        st.line_chart(preis_historie)

    with col2:
        st.success("🏪 **Gefundene Angebote in deutschen Webshops**")
        st.caption("Gefiltert nach deutschen Händlern (.de), ohne bezahlte Premium-Listings.")
        
        # Shop Angebote im Detail
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
                
        # ZUBEHÖR INJEKTION
        st.markdown("### 🔌 Sinnvolles & benötigtes Zubehör:")
        
        zubehoer_items = {
            "Eureka Mignon Manuale (Kaffeemühle)": 269.00,
            "Edelstahl-Tamper (58mm)": 29.90,
            "JoeFrex Abschlagbox (M-Größe)": 24.90
        }
        
        auswahl_zubehoer = {}
        gesamtpreis = 579.00  # Basispreis der Maschine
        
        for item, preis in zubehoer_items.items():
            if st.checkbox(f"{item} (+ {preis:.2f} €)"):
                gesamtpreis += preis
                
        st.markdown(f"## **Gesamtpreis des Setups:** `{gesamtpreis:.2f} €`")

else:
    st.info("Dieser Bereich dient später als Vorlage für dein Kamera-Equipment.")
