import random
import time
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Générateur Achat / Vente", page_icon="⚡", layout="centered")

# --- Petit style (facultatif) ---
st.markdown(
    """
    <style>
      .card { padding: 18px; border-radius: 18px; border: 1px solid rgba(255,255,255,.12); }
      .big { font-size: 18px; font-weight: 600; }
      .muted { opacity: .75; }
      .pill {
        display:inline-block; padding: 6px 10px; border-radius: 999px;
        border: 1px solid rgba(255,255,255,.18); margin-right: 8px;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session state ---
if "running" not in st.session_state:
    st.session_state.running = False
if "history" not in st.session_state:
    st.session_state.history = []  # list of (timestamp, action)

# --- UI ---
st.title("⚡ Générateur Achat / Vente")
st.caption("App Python partageable (Streamlit).")

with st.container(border=True):
    st.markdown('<div class="big">Contrôles</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("▶️ Start", use_container_width=True, disabled=st.session_state.running):
            st.session_state.running = True
            st.rerun()

    with c2:
        if st.button("⏹️ Stop", use_container_width=True, disabled=not st.session_state.running):
            st.session_state.running = False
            st.rerun()

    with c3:
        interval = st.number_input("Intervalle (sec)", min_value=1, max_value=60, value=3, step=1)

st.divider()

colA, colB = st.columns(2)
with colA:
    if st.button("✅ Acheter", use_container_width=True):
        st.session_state.history.insert(0, (datetime.now().strftime("%H:%M:%S"), "ACHETER"))
with colB:
    if st.button("🔻 Vendre", use_container_width=True):
        st.session_state.history.insert(0, (datetime.now().strftime("%H:%M:%S"), "VENDRE"))

st.divider()

# --- Affichage état ---
status = "🟢 En cours" if st.session_state.running else "⚪ À l'arrêt"
st.markdown(f'<span class="pill">{status}</span><span class="pill muted">Auto: {"ON" if st.session_state.running else "OFF"}</span>', unsafe_allow_html=True)

# --- Générateur auto ---
# (Choisit aléatoirement ACHETER/VENDRE toutes les N secondes quand Start est actif)
if st.session_state.running:
    action = random.choice(["ACHETER", "VENDRE"])
    st.session_state.history.insert(0, (datetime.now().strftime("%H:%M:%S"), action))
    time.sleep(interval)
    st.rerun()

# --- Historique ---
st.subheader("Historique")
if st.session_state.history:
    st.dataframe(
        [{"Heure": t, "Action": a} for (t, a) in st.session_state.history[:50]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Aucune action pour l’instant. Clique sur Acheter/Vendre ou Start.")
