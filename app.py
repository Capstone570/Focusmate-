import streamlit as st

# Page Configuration
st.set_page_config(page_title="FocusMate", page_icon="🧠", layout="centered")

st.title("🧠 FocusMate")
st.caption("Your Grounded Deep Work Companion")

# Pre-mapped Mood Database
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

# User Inputs
st.subheader("1. How are you feeling right now?")

# Create a 2x2 grid for mood selection
col1, col2 = st.columns(2)
with col1:
    btn_stressed = st.button("😰 Stressed / Anxious", use_container_width=True)
    btn_distracted = st.button("📱 Distracted / Restless", use_container_width=True)
with col2:
    btn_tired = st.button("🥱 Tired / Low Energy", use_container_width=True)
    btn_overwhelmed = st.button("🌀 Overwhelmed by Options", use_container_width=True)

# Maintain mood selection state
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

if btn_stressed:
    st.session_state.selected_mood = "stressed"
elif btn_tired:
    st.session_state.selected_mood = "tired"
elif btn_distracted:
    st.session_state.selected_mood = "distracted"
elif btn_overwhelmed:
    st.session_state.selected_mood = "overwhelmed"

# Display chosen status indicator
if st.session_state.selected_mood:
    mood_info = MOOD_DATABASE[st.session_state.selected_mood]
    st.info(f"Selected: **{mood_info['title']}**")
else:
    st.warning("Please tap a button above to select your current state.")

st.divider()

# Biometric & Session Sliders
st.subheader("2. Session Parameters")
target_hours = st.number_input("📚 Target Study Hours", min_value=1, max_value=12, value=3)

s_col1, s_col2 = st.columns(2)
with s_col1:
    sleep_score = st.slider("😴 Sleep Quality", min_value=1, max_value=10, value=7)
with s_col2:
    energy_score = st.slider("⚡ Energy Level", min_value=1, max_value=10, value=7)

generate = st.button("✨ Generate Focus Strategy ✨", type="primary", use_container_width=True)

# Strategy Output
if generate:
    if not st.session_state.selected_mood:
        st.error("Please pick a mood status first before generating your strategy.")
    else:
        # Calculate dynamic capacity and session pacing
        capacity = round(((sleep_score * 0.4) + (energy_score * 0.6)) * 10)
        sprint_time = 35 if capacity > 70 else (20 if capacity > 40 else 10)
        rest_time = 5

        st.divider()
        st.subheader("🎯 Your Custom Action Plan")

        # Metrics display
        m1, m2, m3 = st.columns(3)
        m1.metric("Focus Capacity", f"{capacity}%")
        m2.metric("Sprint Length", f"{sprint_time} min")
        m3.metric("Rest Break", f"{rest_time} min")

        selected = MOOD_DATABASE[st.session_state.selected_mood]

        st.markdown(f"### {selected['title']}")
        st.markdown(f"**Reality Check:**\n{selected['verdict']}")
        st.markdown(f"**First Micro-Step:**\n{selected['action']}")
        st.markdown(f"**Recommended Pace:**\nWork in **{sprint_time}-minute focus blocks** followed by **{rest_time}-minute total breaks** across your {target_hours}-hour session.")
