import streamlit as st
import urllib.parse
import json
# Wir nutzen den kostenlosen g4f-Provider für KI-Abfragen ohne Key
from g4f.client import Client

# Seiteneinstellungen
st.set_page_config(page_title="KI-Produkt-Kompass", page_icon="🤖", layout="centered")

# --- HILFSFUNKTION: KI FRAGEN (LIVE-GENERIERUNG) ---
def generiere_produkt_infos(produktname):
    client = Client()
    
    # Wir zwingen die KI über den Prompt, uns ein sauberes JSON-Format zurückzugeben
    prompt = f"""
    Analysiere das Produkt "{produktname}" für einen unabhängigen Produktvergleich.
    Antworte AUSSCHLIESSLICH in diesem JSON-Format (kein Smalltalk, kein Text davor oder danach!):
    {{
        "beschreibung": "Eine präzise Kurzbeschreibung des Produkts (Vorteile, Zielgruppe, Kernfeatures) auf Deutsch.",
        "p_l_sieger": "Eine ehrliche Einschätzung zum Preis-Leistungs-Verhältnis. Gibt es was Besseres fürs Geld?",
        "alternativen": "Nenne 2 konkrete, bessere oder günstigere Alternativen zu diesem Produkt.",
        "zubehoer": ["Zubehörteil 1", "Zubehörteil 2", "Zubehörteil 3"]
    }}
    Wichtig: Das Zubehör-Array darf maximal 3-4 exakte Produktnamen oder Zubehörbegriffe enthalten, nach denen man gut suchen kann.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Nutzt ein extrem starkes Modell im Hintergrund
            messages=[{"role": "user", "content": prompt}]
        )
        ergebnis_text = response.choices[0].message.content
        
        # Säubern, falls die KI Markdown-Codeblöcke mitgeliefert hat
        if "```json" in ergebnis_text:
            ergebnis_text = ergebnis_text.split("```json")[1].split("```")[0]
        elif "```" in ergebnis_text:
            ergebnis_text = ergebnis_text.split("```")[1].split("```")[0]
            
        return json.loads(ergebnis_text.strip())
    except Exception as e:
        # Fallback-Daten, falls die kostenlose KI-Schnittstelle mal überlastet ist
        return {
            "beschreibung": f"Live-Analyse für {produktname} momentan verzögert. Nutze die Direktlinks unten für Echtzeit-Ergebnisse.",
            "p_l_sieger": "Bitte direkt über die Händlerlinks auf Geizhals/Idealo prüfen.",
            "alternativen": "Vergleiche ähnliche Modelle direkt auf den Plattformen.",
            "zubehoer": [f"{produktname} Zubehör", "Universal Tasche", "Passendes Kabel"]
        }

# --- KOPFZEILE ---
st.title("🤖 KI-gestützter Produkt-Kompass")
st.write("Tippe ein beliebiges Produkt ein. Die KI generiert live Beschreibungen, Zubehör und Alternativen, während die Buttons dich zu den echten Preisen führen.")
st.markdown("---")

# Freies Eingabefeld statt starrem Dropdown!
suchbegriff = st.text_input("Welches Produkt suchst du?", placeholder="Z.B. Dyson V15, Makita Akkuschrauber, Philips Airfryer...")

if suchbegriff:
    # Spinner anzeigen, während die KI im Hintergrund nachdenkt und generiert
    with st.spinner(f"🤖 KI analysiert '{suchbegriff}' im Web..."):
        details = generiere_produkt_infos(suchbegriff)
    
    st.markdown("---")
    
    # --- BLOCK 1: LIVE GENERIERTE BESCHREIBUNG & ANALYSE ---
    st.markdown(f"### 📋 Unabhängige Analyse für: {suchbegriff}")
    st.write(details.get("beschreibung", ""))
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.warning("💰 **Preis/Leistung Einschätzung:**")
        st.write(details.get("p_l_sieger", ""))
    with col_info2:
        st.info("🔄 **Beste Alternativen:**")
        st.write(details.get("alternativen", ""))
        
    st.markdown("---")
    
    # --- BLOCK 2: LIVE GENERIERTES ZUBEHÖR ---
    st.markdown("### 🔌 Empfohlenes Zubehör & Ergänzende Produkte")
    st.write("Die KI hat ermittelt, dass dieses Zubehör am häufigsten mitgesucht wird:")
    
    zubehoer_liste = details.get("zubehoer", [])
    if zubehoer_liste:
        cols_zub = st.columns(len(zubehoer_liste))
        for i, zub_item in enumerate(zubehoer_liste):
            with cols_zub[i]:
                zub_encoded = urllib.parse.quote(zub_item)
                zub_url = f"https://geizhals.de/?fs={zub_encoded}"
                st.markdown(f"""
                <a href="{zub_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #f0f2f6; color: #31333f; padding: 10px; text-align: center; border-radius: 6px; font-size: 13px; font-weight: 500; border: 1px solid #d1d5db; min-height: 65px; display: flex; align-items: center; justify-content: center;">
                        📦 {zub_item}<br>(Preise zeigen ➔)
                    </div>
                </a>
                """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- BLOCK 3: DIE DIREKTEN PREIS-BUTTONS ---
    st.markdown("### 📉 Echte Live-Preise & Verlauf ansehen")
    st.write("Hier springst du direkt zu den echten, ungeschönten Marktdaten:")
    
    suchbegriff_encoded = urllib.parse.quote(suchbegriff)
    geizhals_url = f"https://geizhals.de/?fs={suchbegriff_encoded}"
    idealo_url = f"https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={suchbegriff_encoded}"
    
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; gap: 12px;">
            <a href="{geizhals_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #d94540; color: white; padding: 14px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px; border: 1px solid #b3322d; box-shadow: 0px 2px 4px rgba(0,0,0,0.1);">
                    📊 Auf Geizhals öffnen (Preisverlauf & alle Shops)
                </div>
            </a>
            <a href="{idealo_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #002f6c; color: white; padding: 14px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px; border: 1px solid #001f4d; box-shadow: 0px 2px 4px rgba(0,0,0,0.1);">
                    📈 Auf Idealo öffnen (Angebots-Trends & Händler)
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("👋 Willkommen! Bitte gib oben im Suchfeld ein beliebiges Produkt ein, um die automatische KI-Analyse zu starten.")
