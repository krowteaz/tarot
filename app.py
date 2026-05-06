import streamlit as st
import random
import json
from pathlib import Path

st.set_page_config(
    page_title="Mystic Tarot",
    page_icon="🔮",
    layout="wide"
)

# LOAD TAROT DATA
DATA_FILE = Path("full_tarot_deck.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# FLATTEN DECK
tarot_cards = []

tarot_cards.extend(data["major_arcana"])

for suit in data["minor_arcana"].values():
    tarot_cards.extend(suit)

# CUSTOM CSS
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        180deg,
        #07070a,
        #140f1f,
        #1e1333
    );
    color: #f2d27a;
}

.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: #f2d27a;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    color: #c9b27b;
    margin-bottom: 40px;
}

.tarot-card {
    background: rgba(20,20,20,0.75);
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 25px rgba(255,215,0,0.15);
}

.card-title {
    font-size: 28px;
    font-weight: bold;
    color: #f2d27a;
}

.section-title {
    font-size: 32px;
    color: #f2d27a;
    margin-top: 20px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(
    '<div class="main-title">🔮 Mystic Tarot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Reveal your destiny through the cards</div>',
    unsafe_allow_html=True
)

# SIDEBAR
st.sidebar.title("Tarot Reading")

reading_type = st.sidebar.selectbox(
    "Choose Reading",
    [
        "Single Card",
        "Three Card Spread",
        "Love Reading",
        "Career Reading",
        "Daily Tarot"
    ]
)

zodiac = st.sidebar.selectbox(
    "Zodiac Sign",
    [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces"
    ]
)

# DRAW FUNCTION
def draw_cards(count):
    return random.sample(tarot_cards, count)

# CARD RENDERER
def render_card(card):

    reversed_card = random.choice([True, False])

    if reversed_card:
        card_data = card["reversed"]
        orientation = "Reversed"
    else:
        card_data = card["upright"]
        orientation = "Upright"

    st.markdown(
        '<div class="tarot-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="card-title">{card["name"]}</div>',
        unsafe_allow_html=True
    )

    if "arcana" in card:
        st.caption(card["arcana"])

    if "suit" in card:
        st.write(f"🃏 Suit: {card['suit']}")

    if "keywords" in card:
        st.write(
            "✨ Keywords:",
            ", ".join(card["keywords"])
        )

    if reversed_card:
        st.warning(f"{orientation} Card")
    else:
        st.success(f"{orientation} Card")

    st.write(f"**Meaning:** {card_data['meaning']}")
    st.write(f"**Love:** {card_data['love']}")
    st.write(f"**Career:** {card_data['career']}")
    st.write(f"**Guidance:** {card_data['guidance']}")

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# BUTTON
if st.button("Reveal My Reading ✨"):

    if reading_type == "Single Card":
        cards = draw_cards(1)

    elif reading_type == "Three Card Spread":
        cards = draw_cards(3)

    else:
        cards = draw_cards(2)

    st.markdown(
        f'<div class="section-title">{reading_type}</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(len(cards))

    for idx, card in enumerate(cards):
        with cols[idx]:
            render_card(card)

    st.markdown("---")

    st.subheader("🔮 AI Interpretation")

    st.write(f"""
    Your reading for **{zodiac}** suggests an important energetic shift.

    This period focuses on transformation, emotional clarity,
    and spiritual growth.

    Trust your intuition and avoid rushing important decisions.

    The cards indicate opportunities involving:
    - Relationships
    - Personal healing
    - Career movement
    - Inner awakening
    """)

    # DOWNLOAD
    reading_export = json.dumps(cards, indent=2)

    st.download_button(
        "Download Reading",
        data=reading_export,
        file_name="tarot_reading.json",
        mime="application/json"
    )
