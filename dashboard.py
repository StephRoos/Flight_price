import joblib
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Flight Price Finder",
    page_icon="✈️",
    layout="wide",
)

st.markdown(
    """
    <style>
      .hero {text-align:center; padding: 2.2rem 0 1rem 0;}
      .hero h1 {font-size: 2.2rem; margin-bottom: .2rem;}
      .hero p {opacity:.75; margin-top: 0;}
      .pill {
        display:inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.12);
        font-size: 0.85rem;
        opacity: .85;
        margin-right: 6px;
        margin-bottom: 6px;
      }
      .bigprice {
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1;
        margin: .2rem 0 .2rem 0;
      }
      .subtle {opacity:.75}
      .searchwrap {
        max-width: 920px;
        margin: 0 auto;
      }
      .stButton>button {
        border-radius: 12px !important;
        padding: 0.65rem 1rem !important;
        font-weight: 700 !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Chargement modèle ----------
@st.cache_resource
def load_model():
    model_path = Path("artifacts") / "flight_price_model.joblib"
    if not model_path.exists():
        st.error(
            "Modèle introuvable. Exporte d'abord le modèle dans le notebook : "
            "`artifacts/flight_price_model.joblib`."
        )
        st.stop()
    return joblib.load(model_path)

model = load_model()

# ---------- Valeurs par défaut / listes ----------
AIRLINES = ["IndiGo", "Air India", "Vistara", "SpiceJet", "GO FIRST", "AirAsia"]
CITIES = ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"]
TIME_BANDS = ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"]
STOPS_LABEL_TO_NUM = {"zero": 0, "one": 1, "two_or_more": 2}
CLASS_LABEL_TO_NUM = {"Economy": 0, "Business": 1}

def make_row(
    airline, source_city, destination_city, departure_time, arrival_time,
    duration, days_left, stops_label, class_label
):
    return pd.DataFrame([{
        "airline": airline,
        "source_city": source_city,
        "destination_city": destination_city,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "duration": float(duration),
        "days_left": int(days_left),
        "stops_num": int(STOPS_LABEL_TO_NUM[stops_label]),
        "class_num": int(CLASS_LABEL_TO_NUM[class_label]),
    }])

def format_inr(x):
    # affichage simple
    x = float(x)
    return f"₹ {x:,.0f}".replace(",", " ")

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
      <h1>✈️ Flight Price Finder</h1>
      <p>Interface type “recherche de vols” pour estimer le prix d’un billet.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- Bloc central (barre de recherche / formulaire) ----------
st.markdown('<div class="searchwrap">', unsafe_allow_html=True)
with st.container():

    c1, c2, c3 = st.columns([1.1, 1.1, 1], vertical_alignment="bottom")
    with c1:
        source_city = st.selectbox("Départ", CITIES, index=0)
    with c2:
        destination_city = st.selectbox("Arrivée", CITIES, index=1)
    with c3:
        class_label = st.segmented_control("Classe", options=["Economy", "Business"], default="Economy")

    c4, c5, c6, c7 = st.columns([1, 1, 1, 1], vertical_alignment="bottom")
    with c4:
        airline = st.selectbox("Compagnie", AIRLINES, index=0)
    with c5:
        stops_label = st.selectbox("Escales", ["zero", "one", "two_or_more"], index=0)
    with c6:
        days_left = st.slider("Jours avant le vol", min_value=1, max_value=60, value=15)
    with c7:
        duration = st.number_input("Durée (heures)", min_value=0.5, max_value=60.0, value=2.5, step=0.5)

    c8, c9 = st.columns([1, 1], vertical_alignment="bottom")
    with c8:
        departure_time = st.selectbox("Créneau départ", TIME_BANDS, index=1)
    with c9:
        arrival_time = st.selectbox("Créneau arrivée", TIME_BANDS, index=3)

    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    run = st.button("🔎 Rechercher le meilleur prix", width='stretch')

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Résultats ----------
st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

if run:
    if source_city == destination_city:
        st.warning("Départ et arrivée identiques : choisis deux villes différentes 🙂")
    else:
        X_input = make_row(
            airline=airline,
            source_city=source_city,
            destination_city=destination_city,
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration=duration,
            days_left=days_left,
            stops_label=stops_label,
            class_label=class_label,
        )

        pred = model.predict(X_input)[0]
        pred = max(0.0, float(pred))

        left, right = st.columns([1.2, 0.8])
        with left:
            st.markdown("### Estimation du prix")
            st.markdown(f'<div class="bigprice">{format_inr(pred)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="subtle">Prix estimé par le modèle (Roupies indiennes).</div>', unsafe_allow_html=True)
            st.markdown("<hr style='opacity:.15'>", unsafe_allow_html=True)

            # petits tags "résumé"
            pills = [
                f"{source_city} → {destination_city}",
                airline,
                f"classe: {class_label}",
                f"escales: {stops_label}",
                f"durée: {duration} h",
                f"J-{days_left}",
                f"départ: {departure_time}",
                f"arrivée: {arrival_time}",
            ]
            st.markdown("".join([f'<span class="pill">{p}</span>' for p in pills]), unsafe_allow_html=True)

        with right:
            st.markdown("### Détails envoyés au modèle")
            st.dataframe(X_input, width='stretch', hide_index=True)
            st.caption("Ton modèle inclut le preprocessing (OneHot + scaler + imputers) dans la Pipeline.")
