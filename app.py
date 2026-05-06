import streamlit as st
import random
import json
from pathlib import Path

st.set_page_config(
    page_title="Mystic Tarot",
    page_icon="🔮",
    layout="wide"
)

# Load tarot data
DATA_FILE = Path("tarot_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    tarot_cards = json.load(f)

# Custom Styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #090909, #1b1028);
    color: #f2d27a;
}

.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: bold;
    color: #f2d27a;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    color: #c8b27c;
    margin-bottom: 30px;
}

.tarot-card {
    background-color: rgba(20,20,20,0.7);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #d4af37;
    box-shadow: 0 0 20px rgba(212,175,55,0.3);
}

.card-title {
    font-size: 28px;
    color: #f2d27a;
    font-weight: bold;
}

.section-title {
    color: #f2d27a;
    font-size: 24px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔮 Mystic Tarot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Reveal your destiny through the cards</div>', unsafe_allow_html=True)

st.sidebar.title("Tarot Settings")

reading_type = st.sidebar.selectbox(
    "Choose Reading Type",
    [
        "Single Card",
        "Three Card Spread",
        "Love Reading",
        "Career Reading",
        "Daily Tarot"
    ]
)

zodiac = st.sidebar.selectbox(
    "Choose Zodiac Sign",
    [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
)

def draw_cards(count=1):
    return random.sample(tarot_cards, count)

def render_card(card):
    reversed_card = random.choice([True, False])

    st.markdown('<div class="tarot-card">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="card-title">{card["name"]}</div>',
        unsafe_allow_html=True
    )

    if reversed_card:
        st.warning("Reversed Card")
    else:
        st.success("Upright Card")

    st.write(f"**Meaning:** {card['meaning']}")
    st.write(f"**Love:** {card['love']}")
    st.write(f"**Career:** {card['career']}")
    st.write(f"**Guidance:** {card['guidance']}")

    if reversed_card:
        st.error("⚠ Warning: Avoid impulsive decisions and emotional confusion.")
    else:
        st.info("✨ Positive Energy: Growth and transformation are approaching.")

    st.markdown('</div>', unsafe_allow_html=True)

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
    st.subheader("AI Style Interpretation")

    st.write(f"""
    Your reading suggests a powerful energetic shift for **{zodiac}**.

    This is a period of reflection, intuition, and transformation.
    Trust your instincts and avoid rushing important decisions.

    Opportunities may appear unexpectedly, especially in relationships and career growth.
    """)

    reading_text = f"{reading_type} reading for {zodiac}"

    st.download_button(
        "Download Reading",
        data=reading_text,
        file_name="tarot_reading.txt"
    )
