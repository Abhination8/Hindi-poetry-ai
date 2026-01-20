import streamlit as st
from poem_generator import generate_poem
from poem_store import (
    init_db,
    save_poem,
    update_rating,
    get_liked_poems
)

# -----------------------------------
# Page config
# -----------------------------------
st.set_page_config(page_title="Hindi Poetry AI", layout="centered")
st.title("🪔 Hindi Poetry AI")

# -----------------------------------
# Init DB
# -----------------------------------
init_db()

# -----------------------------------
# Session State Initialization
# -----------------------------------
if "poem" not in st.session_state:
    st.session_state["poem"] = None

if "explanation" not in st.session_state:
    st.session_state["explanation"] = None

if "poem_id" not in st.session_state:
    st.session_state["poem_id"] = None

if "rated" not in st.session_state:
    st.session_state["rated"] = False

if "show_share" not in st.session_state:
    st.session_state["show_share"] = False

# -----------------------------------
# Inputs
# -----------------------------------
theme = st.text_input("Theme", "प्रेम")
mood = st.text_input("Mood", "करुण")
style = st.text_input("Style", "Bhakti")
meter = st.selectbox("Poetic Form", ["Free Verse", "Doha", "Chaupai"])

# -----------------------------------
# Generate poem
# -----------------------------------
if st.button("Generate Poem"):
    liked_poems = get_liked_poems(limit=5)

    with st.spinner("कविता लिखी जा रही है..."):
        poem_text, explanation = generate_poem(
            theme,
            mood,
            style,
            meter,
            liked_poems
        )

    poem_id = save_poem(
        poem_text,
        theme,
        mood,
        style,
        meter,
        [p["name"] for p in explanation["poets"]]
    )

    # Reset & store state
    st.session_state["poem"] = poem_text
    st.session_state["explanation"] = explanation
    st.session_state["poem_id"] = poem_id
    st.session_state["rated"] = False
    st.session_state["show_share"] = False

# -----------------------------------
# Poem UI (ONLY if poem exists)
# -----------------------------------
if st.session_state["poem"]:

    st.subheader("📜 Your Poem")
    st.write(st.session_state["poem"])

    # Copy-friendly block
    st.code(st.session_state["poem"], language="text")

    # --------------------------------
    # Share UX (modal-like behavior)
    # --------------------------------
    if not st.session_state["show_share"]:
        if st.button("🔗 Share"):
            st.session_state["show_share"] = True
    else:
        st.markdown("---")
        st.subheader("🔗 Share this poem")

        share_link = f"https://your-app-domain/poem/{st.session_state['poem_id']}"

        st.text_input(
            "Shareable link",
            value=share_link,
            disabled=True
        )

        st.info("Copy this link and share it anywhere.")

        if st.button("Close"):
            st.session_state["show_share"] = False

    # --------------------------------
    # Ratings (single-use)
    # --------------------------------
    if not st.session_state["rated"]:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Like"):
                update_rating(st.session_state["poem_id"], 1)
                st.session_state["rated"] = True
                st.success("Thanks! This will improve future poems.")

        with col2:
            if st.button("👎 Dislike"):
                update_rating(st.session_state["poem_id"], -1)
                st.session_state["rated"] = True
                st.warning("Feedback recorded.")

    # --------------------------------
    # Explanation
    # --------------------------------
    if st.button("How this poem was created"):
        exp = st.session_state["explanation"]

        st.subheader("📖 Explanation")
        st.write(f"**Poetic Form:** {exp['meter']}")

        st.write("**Stylistic Inspirations:**")
        for p in exp["poets"]:
            st.write(f"- {p['name']} ({p['influence']})")

        st.write("**Themes Used:**")
        st.write(", ".join(exp["themes"]))

        if exp.get("quality_examples_used"):
            st.info("This poem was improved using highly-rated past poems.")

    # --------------------------------
    # Reset
    # --------------------------------
    if st.button("New Poem"):
        st.session_state["poem"] = None
        st.session_state["explanation"] = None
        st.session_state["poem_id"] = None
        st.session_state["rated"] = False
        st.session_state["show_share"] = False