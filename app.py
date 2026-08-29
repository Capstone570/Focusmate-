import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="FocusMate AI", page_icon="🔮", layout="centered")

# 2. Reassuring Response Database
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
        "title": "🌀 Overwhelmed by Everything",
        "verdict": "When you have ten things to do, your mind gets paralyzed trying to figure out where to start. You don't need the perfect plan; you just need to pick one direction and let the rest wait.",
        "action": "Write down 3 things on your mind, pick the easiest one to complete, and ignore the other two completely until your first short focus sprint is finished."
    }
}

# Preserve State for Mood Button Selection & Text Input
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None
if "mind_dump_text" not in st.session_state:
    st.session_state.mind_dump_text = ""

# Mascot & Header
st.title("🔮 FocusMate AI")
st.caption("Your AI-Powered Deep Work Companion")

st.info("🔒 **Privacy Guarantee:** Your input is processed in memory and never logged, saved, or shared.", icon="🛡️")

# 3. Form Input Area
with st.form("focus_form"):
    st.markdown("### 💬 1. AI Mind Dump")
    st.caption("Tap a mood below or type your raw thoughts in the text box:")

    # Quick Mood Option Buttons
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.form_submit_button("😰 Stressed / Anxious", use_container_width=True):
            st.session_state.selected_mood = "stressed"
            st.session_state.mind_dump_text = MOOD_DATABASE["stressed"]["title"]
        if st.form_submit_button("📱 Distracted / Restless", use_container_width=True):
            st.session_state.selected_mood = "distracted"
            st.session_state.mind_dump_text = MOOD_DATABASE["distracted"]["title"]
            
    with btn_col2:
        if st.form_submit_button("🥱 Tired / Low Energy", use_container_width=True):
            st.session_state.selected_mood = "tired"
            st.session_state.mind_dump_text = MOOD_DATABASE["tired"]["title"]
        if st.form_submit_button("🌀 Overwhelmed by Options", use_container_width=True):
            st.session_state.selected_mood = "overwhelmed"
            st.session_state.mind_dump_text = MOOD_DATABASE["overwhelmed"]["title"]

    # Text Area (User can type freely or use selected mood)
    mind_dump = st.text_area(
        "Or describe what's on your mind:",
        value=st.session_state.mind_dump_text,
        placeholder="Vent your raw thoughts, doubts, fears, or anxieties here...",
        help="Type anything on your mind—the system will read the context and guide you empathetically."
    )
    
    # Original Input Controls & Sliders
    target_hours = st.number_input("📚 2. Target Study Hours", min_value=1, max_value=12, value=3)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sleep_score = st.slider("😴 3. Sleep Score", min_value=1, max_value=10, value=7)
    with col2:
        difficulty_score = st.slider("🎯 4. Task Difficulty", min_value=1, max_value=10, value=6)
    with col3:
        energy_score = st.slider("⚡ 5. Energy Level", min_value=1, max_value=10, value=8)

    submit_button = st.form_submit_button("✨ Generate Focus Strategy ✨", use_container_width=True)

# 4. Actionable Response Output
if submit_button:
    # Determine response logic (Rule-based match or generic reassurance fallback)
    selected_key = st.session_state.selected_mood
    
    if not selected_key:
        # Match text input if keywords exist, default to overwhelmed
        text_lower = mind_dump.lower()
        if "stress" in text_lower or "anxi" in text_lower:
            selected_key = "stressed"
        elif "tir" in text_lower or "sleep" in text_lower or "exhaust" in text_lower:
            selected_key = "tired"
        elif "distract" in text_lower or "focus" in text_lower or "phone" in text_lower:
            selected_key = "distracted"
        else:
            selected_key = "overwhelmed"

    mood_data = MOOD_DATABASE[selected_key]

    # Calculate metrics matching your slider formulas
    capacity = round(((sleep_score * 0.4) + (energy_score * 0.6)) * 10)
    sprint_time = 45 if capacity > 70 else (25 if capacity > 40 else 15)
    rest_time = 10 if sprint_time == 45 else 5

    st.divider()
    st.subheader("🎯 Your Custom Focus Strategy")

    # Metrics Layout
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Focus Capacity", f"{capacity}%")
    m_col2.metric("Sprint Duration", f"{sprint_time} min")
    m_col3.metric("Rest Interval", f"{rest_time} min")

    # Display Grounded Reassuring Response
    st.markdown(f"### {mood_data['title']}")
    st.markdown(f"**🌱 Emotional Analysis:**\n{mood_data['verdict']}")
    st.markdown(f"**⚡ Recommended Micro-Action:**\n{mood_data['action']}")
    st.markdown(f"**⏱️ Sprint Pace:**\nWork in gentle **{sprint_time}-minute focus blocks** with **{rest_time}-minute rest breaks** over your target {target_hours} hours.")
