import streamlit as st
import random
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Mystic Tarot",
    page_icon="🔮",
    layout="wide"
)

# =========================
# LOAD TAROT DATA
# =========================

DATA_FILE = Path("full_tarot_deck.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# =========================
# FLATTEN DECK
# =========================

tarot_cards = []

tarot_cards.extend(data["major_arcana"])

for suit in data["minor_arcana"].values():
    tarot_cards.extend(suit)

# =========================
# SESSION STATE
# =========================

if "deck" not in st.session_state:
    st.session_state.deck = tarot_cards.copy()

if "last_reading" not in st.session_state:
    st.session_state.last_reading = []

# =========================
# SHUFFLE FUNCTION
# =========================

def shuffle_deck():
    random.shuffle(st.session_state.deck)

# =========================
# DRAW FUNCTION
# =========================

def draw_cards(count):

    # Auto reshuffle if deck too small
    if len(st.session_state.deck) < count:
        st.session_state.deck = tarot_cards.copy()
        shuffle_deck()

    selected = st.session_state.deck[:count]
    st.session_state.deck = st.session_state.deck[count:]

    return selected

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top, #24143d 0%, #09090f 60%);
    color: #f4d27d;
}

.main-title {
    text-align: center;
    font-size: 68px;
    font-weight: 800;
    color: #f4d27d;
    margin-top: 20px;
    text-shadow: 0 0 20px rgba(255,215,0,0.35);
}

.subtitle {
    text-align: center;
    color: #d8bf87;
    margin-bottom: 35px;
    font-size: 18px;
}

.tarot-card {
    background: rgba(18,18,24,0.85);
    border: 1px solid rgba(255,215,0,0.25);
    border-radius: 24px;
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
    box-shadow:
        0 0 30px rgba(255,215,0,0.08),
        0 0 60px rgba(180,120,255,0.08);
    transition: 0.3s;
}

.tarot-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 0 40px rgba(255,215,0,0.18);
}

.card-title {
    font-size: 30px;
    font-weight: bold;
    color: #f4d27d;
    margin-bottom: 10px;
}

.section-title {
    font-size: 36px;
    color: #f4d27d;
    margin-top: 25px;
    margin-bottom: 25px;
    text-align: center;
}

.profile-box {
    background: rgba(20,20,28,0.75);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,215,0,0.15);
    margin-bottom: 20px;
}

.shuffle-box {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 20px;
    color: #cdb57c;
}

.footer {
    text-align: center;
    color: #8f7b53;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown(
    '<div class="main-title">🔮 Mystic Tarot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Reveal your destiny through the ancient cards</div>',
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("✨ Tarot Reading")

reading_type = st.sidebar.selectbox(
    "Choose Reading",
    [
        "Single Card",
        "Three Card Spread",
        "Love Reading",
        "Career Reading",
        "Daily Tarot",
        "Soulmate Reading",
        "Future Path Reading"
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

# =========================
# USER PROFILE
# =========================

st.sidebar.markdown("---")

st.sidebar.subheader("🧙 Your Energy Profile")

name = st.sidebar.text_input("Name", "Mystic Soul")

age = st.sidebar.slider(
    "Age",
    min_value=13,
    max_value=80,
    value=25
)

sex = st.sidebar.selectbox(
    "Sex",
    [
        "Male",
        "Female",
        "Non Binary",
        "Prefer not to say"
    ]
)

relationship_status = st.sidebar.selectbox(
    "Relationship Status",
    [
        "Single",
        "In a Relationship",
        "Married",
        "Complicated"
    ]
)

# =========================
# SHUFFLE BUTTON
# =========================

if st.sidebar.button("🔀 Shuffle Deck"):
    shuffle_deck()
    st.sidebar.success("The tarot deck has been shuffled.")

st.sidebar.markdown(
    f"""
    <div class="shuffle-box">
    🃏 Remaining Cards: {len(st.session_state.deck)}
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# CARD RENDERER
# =========================

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
        st.caption(f"✨ {card['arcana']}")

    if "suit" in card:
        st.write(f"🃏 Suit: {card['suit']}")

    if "keywords" in card:
        st.write(
            "✨ Keywords:",
            ", ".join(card["keywords"])
        )

    if reversed_card:
        st.warning(f"↩️ {orientation} Card")
    else:
        st.success(f"⬆️ {orientation} Card")

    st.write(f"### Meaning")
    st.write(card_data["meaning"])

    st.write(f"### ❤️ Love")
    st.write(card_data["love"])

    st.write(f"### 💼 Career")
    st.write(card_data["career"])

    st.write(f"### 🔮 Guidance")
    st.write(card_data["guidance"])

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# =========================
# MAIN BUTTON
# =========================

if st.button("✨ Reveal My Reading"):

    shuffle_deck()

    if reading_type == "Single Card":
        cards = draw_cards(1)

    elif reading_type == "Three Card Spread":
        cards = draw_cards(3)

    elif reading_type in ["Love Reading", "Career Reading"]:
        cards = draw_cards(2)

    else:
        cards = draw_cards(4)

    st.session_state.last_reading = cards

    st.markdown(
        f'<div class="section-title">{reading_type}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="profile-box">
        👤 <b>Name:</b> {name}<br>
        🎂 <b>Age:</b> {age}<br>
        ⚧ <b>Sex:</b> {sex}<br>
        💞 <b>Status:</b> {relationship_status}<br>
        ♈ <b>Zodiac:</b> {zodiac}<br>
        📅 <b>Date:</b> {datetime.now().strftime("%B %d, %Y")}
        </div>
        """,
        unsafe_allow_html=True
    )

    cols = st.columns(len(cards))

    for idx, card in enumerate(cards):
        with cols[idx]:
            render_card(card)

    st.markdown("---")

    # =========================
    # AI INTERPRETATION
    # =========================

    st.subheader("🔮 Spiritual Interpretation")

    age_message = ""

    if age < 20:
        age_message = "A youthful chapter of discovery surrounds your energy."
    elif age < 35:
        age_message = "You are entering a strong period of personal transformation."
    elif age < 50:
        age_message = "Wisdom and responsibility now shape your spiritual path."
    else:
        age_message = "Your reading reflects deep maturity and intuitive mastery."

    love_focus = ""

    if relationship_status == "Single":
        love_focus = "New emotional connections may soon emerge."
    elif relationship_status == "In a Relationship":
        love_focus = "Your connection requires honesty and emotional balance."
    elif relationship_status == "Married":
        love_focus = "Stability and deeper commitment surround your path."
    else:
        love_focus = "Unresolved emotions need clarity before forward movement."

    st.write(f"""
    Dear **{name}**, your tarot reading reveals powerful energetic movements.

    {age_message}

    As a **{sex.lower()} {zodiac}**, your current vibration is strongly connected to:

    - Emotional healing
    - Spiritual awakening
    - Destiny alignment
    - Personal transformation
    - Intuition enhancement

    {love_focus}

    The cards encourage patience, self trust,
    and confidence in the path unfolding before you.

    Avoid impulsive decisions during emotionally intense situations.

    Your spiritual energy is strongest during moments of silence,
    reflection, and intuition.
    """)

    # =========================
    # DOWNLOAD
    # =========================

    reading_export = {
        "name": name,
        "age": age,
        "sex": sex,
        "zodiac": zodiac,
        "relationship_status": relationship_status,
        "reading_type": reading_type,
        "cards": cards
    }

    st.download_button(
        "⬇️ Download Reading",
        data=json.dumps(reading_export, indent=2),
        file_name="mystic_tarot_reading.json",
        mime="application/json"
    )

# =========================
# FOOTER
# =========================

st.markdown(
    """
    <div class="footer">
    ✨ The universe whispers through symbols and intuition ✨
    </div>
    """,
    unsafe_allow_html=True
)
