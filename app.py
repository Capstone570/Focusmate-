import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="FocusMate", page_icon="🤖", layout="centered")

# Custom CSS for Dark Mode & Styling
st.markdown("""
    <style>
    /* Global Dark Background */
    .stApp {
        background-color: #12111d;
        color: #ffffff;
    }
    /* Mascot Styling */
    .mascot-container {
        text-align: center;
        padding: 20px 0;
    }
    .mascot-speech {
        background: linear-gradient(135deg, #fbcfe8 0%, #f472b6 100%);
        color: #12111d;
        padding: 12px 24px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(244, 114, 182, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Rule-Based Reassuring Database
MOOD_DATABASE = {
    "stressed": {
        "title": "😰 High Stress & Pressure",
        "verdict": "It makes total sense that you feel this way—when expectations stack up, your brain naturally panics. You don't have to conquer everything right now; you just need to start making quiet progress.",
        "action": "Pick just *one* small piece of your task. Write it down on a physical scrap of paper, close all other open tabs, and set a timer for 5 minutes. That's your only goal for now."
    },
    "tired": {
        "title": "🥱 Low Energy & Fatigue",
        "verdict": "Forcing intense concentration when your body is running on empty rarely works. Pushing too hard right now will only cause frustration, so let's adjust the pace to match your current battery.",
        "action": "Do a 5-minute low-brainpower warm-up: organize your files, clear your workspace, or review past notes. Getting into motion gently will build momentum without burning you out."
    },
    "distracted": {
        "title": "📱 Distracted & Restless",
        "verdict": "Don't beat yourself up for losing focus—your mind is just looking for a quick break and low-friction dopamine. It takes a few deliberate minutes to pull your attention back in.",
        "action": "Put your phone entirely out of sight (in another room or inside a drawer). Open only the document you need, and commit to working uninterrupted for just 10 quick minutes."
    },
    "overwhelmed": {
        "title": "🌀 Overwhelmed by Options",
        "verdict": "When you have ten things to do, your mind gets paralyzed trying to figure out where to start. You don't need the perfect plan; you just need to pick one direction and let the rest wait.",
        "action": "Write down 3 things on your mind, pick the easiest one to complete, and ignore the other two completely until your first short focus sprint is finished."
    }
}

# Session State Initializations
if "started" not in st.session_state:
    st.session_state.started = False
if "mind_dump_text" not in st.session_state:
    st.session_state.mind_dump_text = ""

# ==========================================
# SCREEN 1: LANDING PAGE WITH MASCOT
# ==========================================
if not st.session_state.started:
    st.write("<br><br>", unsafe_allow_html=True)
    
    # Title & Subtitle
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 3.5rem; font-weight: 800;'>FocusMate</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem;'>Your AI-Powered Deep Work Companion</p>", unsafe_allow_html=True)
    
    # Robot Mascot Banner
    st.markdown("""
        <div class="mascot-container">
            <div style="font-size: 5rem;">🤖</div>
            <div class="mascot-speech">
                "Hi! Welcome to FocusMate!" ✨
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    # Dive In Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Let's Dive In! 🚀", use_container_width=True, type="primary"):
            st.session_state.started = True
            st.rerun()

# ==========================================
# SCREEN 2: MAIN DASHBOARD & FORM
# ==========================================
else:
    st.title("FocusMate")
    st.caption("Your AI-Powered Deep Work Companion")

    st.info("🔒 **Privacy Guarantee:** Your input is processed in memory and never logged, saved, or shared.", icon="🛡️")

    # Main Card Area
    with st.container(border=True):
        st.subheader("💬 1. AI Mind Dump")
        st.caption("Tap a mood below or type your raw thoughts in the text box:")

        # 4 Preset Mood Buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("😰 Stressed / Anxious", use_container_width=True):
                st.session_state.mind_dump_text = "I'm feeling stressed and anxious right now."
            if st.button("📱 Distracted / Restless", use_container_width=True):
                st.session_state.mind_dump_text = "I'm distracted and having trouble keeping focus."

        with btn_col2:
            if st.button("🥱 Tired / Low Energy", use_container_width=True):
                st.session_state.mind_dump_text = "I'm feeling tired and my energy is low."
            if st.button("🌀 Overwhelmed by Options", use_container_width=True):
                st.session_state.mind_dump_text = "I'm feeling completely overwhelmed by options."

        # Text Input Area
        mind_dump = st.text_area(
            "Or describe what's on your mind:",
            value=st.session_state.mind_dump_text,
            placeholder="Vent your raw thoughts, doubts, fears, or anxieties here...",
            help="Type anything on your mind—the system will read the context and guide you empathetically."
        )

        # Form Controls & Sliders
        with st.form("focus_form"):
            target_hours = st.number_input("📚 2. Target Study Hours", min_value=1, max_value=12, value=3)

            col1, col2, col3 = st.columns(3)
            with col1:
                sleep_score = st.slider("😴 3. Sleep Score", min_value=1, max_value=10, value=7)
            with col2:
                difficulty_score = st.slider("🎯 4. Task Difficulty", min_value=1, max_value=10, value=6)
            with col3:
                energy_score = st.slider("⚡ 5. Energy Level", min_value=1, max_value=10, value=8)

            submit_button = st.form_submit_button("✨ Generate Focus Strategy ✨", use_container_width=True)

    # Strategy Output Display
    if submit_button:
        text_lower = mind_dump.lower()

        if "stress" in text_lower or "anxi" in text_lower:
            selected_key = "stressed"
        elif "tir" in text_lower or "sleep" in text_lower or "exhaust" in text_lower:
            selected_key = "tired"
        elif "distract" in text_lower or "focus" in text_lower or "restless" in text_lower:
            selected_key = "distracted"
        else:
            selected_key = "overwhelmed"

        mood_data = MOOD_DATABASE[selected_key]

        # Metric Calculations
        capacity = round(((sleep_score * 0.4) + (energy_score * 0.6)) * 10)
        sprint_time = 45 if capacity > 70 else (25 if capacity > 40 else 15)
        rest_time = 10 if sprint_time == 45 else 5

        st.divider()
        st.subheader("🎯 Your Custom Focus Strategy")

        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Focus Capacity", f"{capacity}%")
        m_col2.metric("Sprint Duration", f"{sprint_time} min")
        m_col3.metric("Rest Interval", f"{rest_time} min")

        st.markdown(f"### {mood_data['title']}")
        st.markdown(f"**🌱 Emotional Analysis:**\n{mood_data['verdict']}")
        st.markdown(f"**⚡ Recommended Micro-Action:**\n{mood_data['action']}")
        st.markdown(f"**⏱️ Sprint Pace:**\nWork in gentle **{sprint_time}-minute focus blocks** followed by **{rest_time}-minute rest breaks** over your target {target_hours} hours.")
