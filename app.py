import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FocusMate AI Pro", page_icon="🔮", layout="wide")

# Custom styling for standard Streamlit widgets to keep the glassmorphism theme
st.markdown("""
    <style>
        .block-container { padding-top: 2rem !important; }
        footer { visibility: hidden; }
        
        /* Glassmorphism containers */
        div[data-testid="stForm"], div[data-testid="stMetric"] {
            background: rgba(30, 27, 46, 0.6) !important;
            backdrop-filter: blur(16px);
            border: 1px solid rgba(192, 132, 252, 0.2) !important;
            border-radius: 1rem !important;
            padding: 1rem !important;
        }
        
        /* Custom metric colors */
        div[data-testid="stMetricValue"] {
            color: #c084fc !important;
            font-weight: 800 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATASET (DATA STORES & SESSION STATE)
# ---------------------------------------------------------
if "sprints_completed" not in st.session_state:
    st.session_state.sprints_completed = 0

if "strategy_generated" not in st.session_state:
    st.session_state.strategy_generated = False

SOUND_URLS = {
    "binaural": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3",
    "rain": "https://cdn.pixabay.com/download/audio/2021/09/06/audio_8a287e07eb.mp3",
    "white": "https://cdn.pixabay.com/download/audio/2022/03/24/audio_c8c8731f82.mp3"
}

# Hero animation canvas header (Visual element)
hero_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { margin: 0; background: transparent; overflow: hidden; }
        .glow-title {
            background: linear-gradient(135deg, #e9d5ff 0%, #c084fc 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body class="flex flex-col items-center justify-center p-4">
    <h1 class="text-5xl font-extrabold glow-title mb-2 text-center">FocusMate AI</h1>
    <p class="text-slate-400 text-lg text-center">Your End-to-End Deep Work Engine</p>
</body>
</html>
"""
components.html(hero_code, height=120)


# ---------------------------------------------------------
# 1. INPUT FROM THE USER (PURE PYTHON STREAMLIT UI)
# ---------------------------------------------------------
st.markdown("## ⚙️ Interactive Mission Center")

with st.form("focus_form"):
    mood_options = {
        "😰 Stressed / Anxious": "stressed",
        "🥱 Tired / Low Energy": "tired",
        "📱 Distracted / Restless": "distracted",
        "🌟 Happy / Motivated": "happy"
    }
    selected_mood_label = st.radio("🧠 1. Current State of Mind", list(mood_options.keys()), horizontal=True)
    selected_mood = mood_options[selected_mood_label]

    task_name = st.text_input("🎯 2. Primary Task Goal", placeholder="e.g., Write Chapter 1 of Biology Notes, Build UI layout...")
    
    col_diff, col_sleep, col_energy = st.columns(3)
    with col_diff:
        difficulty = st.slider("Perceived Difficulty", min_value=1, max_value=10, value=6)
    with col_sleep:
        sleep = st.slider("😴 Sleep Score", min_value=1, max_value=10, value=7)
    with col_energy:
        energy = st.slider("⚡ Energy Level", min_value=1, max_value=10, value=8)

    submit_btn = st.form_submit_button("✨ Generate Focus Strategy ✨", use_container_width=True)


# ---------------------------------------------------------
# 3. ALGORITHM (FOCUS STRATEGY LOGIC IN PYTHON)
# ---------------------------------------------------------
def generate_strategy(sleep_val, energy_val, diff_val, mood_val, task_val):
    # Weighted formula for capacity
    capacity = round(((sleep_val * 0.4) + (energy_val * 0.6)) * 10)
    
    # Decision logic for sprint lengths
    if capacity >= 75 and diff_val <= 7:
        sprint_time = 45
    elif capacity < 45 or diff_val >= 8:
        sprint_time = 15
    else:
        sprint_time = 25

    rest_time = 10 if sprint_time == 45 else 5

    # Audio mapping logic
    if mood_val == 'stressed':
        audio_key = 'rain'
    elif mood_val == 'distracted':
        audio_key = 'white'
    else:
        audio_key = 'binaural'

    return {
        "capacity": capacity,
        "sprint_time": sprint_time,
        "rest_time": rest_time,
        "audio_key": audio_key,
        "task": task_val if task_val.strip() else "Primary Goal"
    }


# ---------------------------------------------------------
# 4. OUTPUT (DASHBOARD UI & EXECUTION SUITE)
# ---------------------------------------------------------
if submit_btn:
    st.session_state.strategy = generate_strategy(sleep, energy, difficulty, selected_mood, task_name)
    st.session_state.strategy_generated = True

if st.session_state.strategy_generated:
    strat = st.session_state.strategy
    
    st.markdown("---")
    st.markdown("### 🎯 Strategy & Action Plan")

    # Metric Cards
    c1, c2, c3 = st.columns(3)
    c1.metric("Focus Capacity", f"{strat['capacity']}%")
    c2.metric("Sprint Duration", f"{strat['sprint_time']} min")
    c3.metric("Rest Interval", f"{strat['rest_time']} min")

    # Action Roadmap
    st.markdown("#### 📋 AI Action Roadmap")
    st.info(f"""
    1. Set up workspace and open resources for: **{strat['task']}**
    2. Execute core effort for **{strat['sprint_time']} minutes** (focus solely on step 1)
    3. Review progress, outline next steps, and enter a **{strat['rest_time']}-minute break**
    """)

    # Recommended Soundscape Player
    st.markdown("#### 🔊 Recommended Soundscape")
    st.audio(SOUND_URLS[strat['audio_key']])

    # Analytics Tracking
    col_a, col_b = st.columns(2)
    col_a.metric("Daily Streak", "🔥 1 Day")
    col_b.metric("Completed Sprints", f"{st.session_state.sprints_completed} Sprints")
