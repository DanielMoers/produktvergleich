import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Unabhängiger Produktvergleicher", layout="wide")

# --- KOPFZEILE MIT SUCHFELD ---
st.title("🔍 Unabhängiger Produktvergleicher")
st.subheader("Finde echte Angebote in deutschen Webshops – ohne bezahlte Rankings.")

# Das neue Eingabefeld in der Kopfzeile
suchbegriff = st.text_input("Welches Produkt suchst du? (z.B. Quick Mill Cassiopea 3004)", placeholder="Produktname oder EAN eingeben...")

# --- NAVIGATION IN DER SIDEBAR ---
kategorie = st.sidebar.selectbox("Produktkategorie filtern:", ["Alle Kategorien", "Kaffeemaschinen & Zubehör", "Fotografie & Video"])

# --- HAUPTSEITE / LOGIK ---
if suchbegriff:
    # Überprüfung, ob nach der Quick Mill gesucht wurde (Groß-/Kleinschreibung ignoriert)
    if "quick mill" in suchbegriff.lower() or "cassiopea" in suchbegriff.lower() or "3004" in suchbegriff:
        
        st.markdown(f"### Aktuelle Suche: **Quick Mill Cassiopea 3004 (glänzend)**")
        
        # Layout aufteilen: Links Stammdaten & Bild, Rechts Webshops
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.info("📦 **Geizhals Stammdaten**")
            
            # WUNSCH: Produktbild anzeigen
            st.image("https://www.quickmill.it/wp-content/uploads/2016/06/3004_retro.jpg", width=300, caption="Quick Mill Cassiopea 3004 (Edelstahl glänzend)")
            
            # WUNSCH: Stammdaten inklusive Erscheinungsdatum
            stammdaten = {
                "Eigenschaft": ["System", "Aufheizzeit", "Pumpe", "Siebträger", "Gelistet seit / Erschienen", "UVP"],
                "Wert": ["Dual-Thermoblock", "Unter 5 Minuten", "Vibrationspumpe (15 bar)", "58 mm Standard", "Oktober 2014 (Modellpflege 2022)", "749,00 €"]
            }
            st.table(pd.DataFrame(stammdaten))
            
            # WUNSCH: Preisverlauf über 12 Monate
            st.markdown("**Preisverlauf (Letzte 12 Monate):**")
            preis_historie_12m = pd.DataFrame({
                "Monat": ["Jul 25", "Aug 25", "Sep 25", "Okt 25", "Nov 25", "Dez 25", "Jan 26", "Feb 26", "Mrz 26", "Apr 26", "Mai 26", "Jun 26"],
                "Preis (€)": [640, 635, 620, 599, 610, 589, 599, 585, 579, 580, 579, 579]
            }).set_index("Monat")
            st.line_chart(preis_historie_12m)

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
        # Hinweistext für alle anderen Suchbegriffe
        st.warning(f"Das Produkt **'{suchbegriff}'** wurde im Demomodus nicht gefunden.")
        st.info("💡 **Nächster Schritt:** Hier binden wir als Nächstes den automatischen Web-Scraper an, der bei Geizhals nach diesem Begriff sucht, die EAN ausliest und deutsche Shops live scannt!")
else:
    st.info("👆 Bitte gib oben in das Suchfeld ein Produkt ein (z.B. 'Quick Mill'), um den Vergleicher zu starten.")
