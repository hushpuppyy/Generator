import random
import time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pile ou Face - Achat/Vente", page_icon="🪙", layout="centered")

# STYLE 
st.markdown(
    """
    <style>
      .stApp {
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;

        background: radial-gradient(1200px circle at 20% 10%, rgba(255, 200, 120, .20), transparent 45%),
                    radial-gradient(900px circle at 90% 20%, rgba(120, 180, 255, .18), transparent 40%),
                    linear-gradient(180deg, #0b1020 0%, #070a12 100%);
        color: white;
      }

      .wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 22px;
        text-align: center;
      }

      .title {
        font-size: 48px;
        font-weight: 900;
        text-align: center;
        line-height: 1.05;
      }

      .subtitle {
        opacity: .75;
        text-align: center;
        margin-top: -8px;
        font-size: 16px;
      }

      .coin {
        width: 280px;
        height: 280px;
        border-radius: 999px;
        display: grid;
        place-items: center;

        background: radial-gradient(circle at 30% 30%, #fff3, transparent 40%),
                    linear-gradient(135deg, #f7d07a, #ff8a3d);

        box-shadow:
          0 25px 60px rgba(0,0,0,.55),
          inset 0 0 0 8px rgba(255,255,255,.15);
      }

      .coin-text {
        font-size: 42px;
        font-weight: 900;
        color: white;
        text-shadow: 0 6px 18px rgba(0,0,0,.55);
        letter-spacing: .02em;
      }

      .buy {
        background: radial-gradient(circle at 30% 30%, #fff3, transparent 40%),
                    linear-gradient(135deg, #4ade80, #16a34a);
      }

      .sell {
        background: radial-gradient(circle at 30% 30%, #fff3, transparent 40%),
                    linear-gradient(135deg, #fb7185, #dc2626);
      }

      @keyframes flipdrop {
        0%   { transform: translateY(-30px) rotateX(0) rotateZ(0) scale(1); }
        35%  { transform: translateY(-140px) rotateX(720deg) rotateZ(120deg) scale(1.08); }
        70%  { transform: translateY(10px) rotateX(1440deg) rotateZ(240deg) scale(.98); }
        100% { transform: translateY(0) rotateX(1800deg) rotateZ(300deg) scale(1); }
      }

      .anim { animation: flipdrop 1.4s cubic-bezier(.2,.8,.2,1) 1; }

      .hint {
        padding: 12px 18px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,.15);
        background: rgba(255,255,255,.08);
        font-weight: 800;
        opacity: .9;
      }

      div.stButton > button {
        border-radius: 16px !important;
        padding: 16px 28px !important;
        font-size: 18px !important;
        font-weight: 900 !important;
        background: rgba(255,255,255,.10) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,.20) !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

def rain_effect(kind: str):
    # BUY = 💸 vert | SELL = 💲 rouge
    emoji = "💸" if kind == "BUY" else "💲"

    html = f"""
    <style>
      html, body {{
        margin: 0;
        padding: 0;
        background: transparent;
        overflow: hidden;
      }}
      #rain {{
        position: fixed;
        inset: 0;
        pointer-events: none;
        overflow: hidden;
        z-index: 999999;
      }}
      .drop {{
        position: absolute;
        top: -60px;
        font-size: 38px;
        filter: drop-shadow(0 10px 12px rgba(0,0,0,.45));
        will-change: transform;
      }}

      /* ✅ VERT pour BUY */
      .buyColor {{
        color: #22c55e;
        text-shadow: 0 0 14px rgba(34,197,94,.45);
      }}

      /* ✅ ROUGE pour SELL */
      .sellColor {{
        color: #ff3b3b;
        text-shadow: 0 0 14px rgba(255,59,59,.55);
      }}

      @keyframes fall {{
        0%   {{ transform: translateY(-80px) rotate(0deg); opacity: 0; }}
        10%  {{ opacity: 1; }}
        100% {{ transform: translateY(110vh) rotate(360deg); opacity: 0; }}
      }}
    </style>

    <div id="rain"></div>

    <script>
      const root = document.getElementById("rain");
      const EMOJI = "{emoji}";
      const IS_BUY = {str(kind == "BUY").lower()};

      const COUNT = 55;
      const DURATION_MIN = 1000;
      const DURATION_MAX = 2000;

      for (let i = 0; i < COUNT; i++) {{
        const el = document.createElement("div");

        // ✅ IMPORTANT : on applique toujours une classe couleur
        el.className = "drop " + (IS_BUY ? "buyColor" : "sellColor");
        el.textContent = EMOJI;

        const left = Math.random() * 100;
        const delay = Math.random() * 250;
        const duration = DURATION_MIN + Math.random() * (DURATION_MAX - DURATION_MIN);

        el.style.left = left + "vw";
        el.style.animation = "fall " + duration + "ms linear " + delay + "ms 1";

        root.appendChild(el);
        setTimeout(() => el.remove(), duration + delay + 100);
      }}
    </script>
    """
    components.html(html, height=1, width=1)


# ---------- STATE ----------
if "result" not in st.session_state:
    st.session_state.result = None  # "ACHETER" / "VENDRE"
if "spinning" not in st.session_state:
    st.session_state.spinning = False
if "rain_kind" not in st.session_state:
    st.session_state.rain_kind = None  # "BUY"/"SELL" ou None

# ---------- UI ----------
st.markdown('<div class="wrap">', unsafe_allow_html=True)
st.markdown('<div class="title">TU ACHÈTES OU TU VENDS NULOSSE ?<br><br></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">On a dit argent propre non ?</div>', unsafe_allow_html=True)

start = st.button("🎲 START", use_container_width=False, disabled=st.session_state.spinning)

if start and not st.session_state.spinning:
    st.session_state.spinning = True
    st.session_state.result = None
    st.session_state.rain_kind = None
    st.rerun()

# Contenu sur la pièce
if st.session_state.spinning:
    coin_content = "🪙"
    coin_extra_class = "anim"
elif st.session_state.result == "ACHETER":
    coin_content = "ACHETER"
    coin_extra_class = "buy"
elif st.session_state.result == "VENDRE":
    coin_content = "VENDRE"
    coin_extra_class = "sell"
else:
    coin_content = "🪙"
    coin_extra_class = ""

st.markdown(
    f"""
    <div class="coin {coin_extra_class}">
        <div class="coin-text">{coin_content}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ UN SEUL BLOC: fin d’animation => résultat + pluie
if st.session_state.spinning:
    time.sleep(1.2)
    st.session_state.result = random.choice(["ACHETER", "VENDRE"])
    st.session_state.spinning = False
    is_sell = (st.session_state.result.strip().upper() == "VENDRE")
    st.session_state.rain_kind = "SELL" if is_sell else "BUY"
    st.rerun()

# Déclenche la pluie après le rerun, une seule fois
if st.session_state.rain_kind is not None:
    # Force l'iframe des components en plein écran AU-DESSUS de tout
    st.markdown("""
    <style>
    [data-testid="stIFrame"] {
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 999999 !important;
    border: 0 !important;
    background: transparent !important;
    pointer-events: none !important; 
  }
</style>
    """, unsafe_allow_html=True)

    rain_effect(st.session_state.rain_kind)

    # Stoppe le replay
    st.session_state.rain_kind = None


# Petit texte d'aide
if st.session_state.result is None and not st.session_state.spinning:
    st.markdown('<div class="hint">Dis bismillah et appuie sur START 👆</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
