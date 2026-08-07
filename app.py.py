import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
from datetime import datetime

# ---------------------------------------------------------
# Page Config & Custom High-Contrast Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="FocusMate — Youth Well-Being & Focus Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if "intro_seen" not in st.session_state:
    st.session_state.intro_seen = False
if "in_focus_room" not in st.session_state:
    st.session_state.in_focus_room = False
if "focus_task" not in st.session_state:
    st.session_state.focus_task = ""
if "focus_minutes" not in st.session_state:
    st.session_state.focus_minutes = 25
if "early_exit_triggered" not in st.session_state:
    st.session_state.early_exit_triggered = False

# Profile Daily Progress State
if "completed_sessions_today" not in st.session_state:
    st.session_state.completed_sessions_today = 0
if "water_drank_today" not in st.session_state:
    st.session_state.water_drank_today = 0
if "thought_dump_input" not in st.session_state:
    st.session_state.thought_dump_input = ""

# Dynamic Background & Screen Dimming CSS
dimmed_mode_css = ""
if st.session_state.in_focus_room:
    dimmed_mode_css = """
        section[data-testid="stSidebar"], .brand-header, header {
            display: none !important;
        }
        .stApp {
            background-color: #020305 !important;
            filter: brightness(0.4) contrast(0.95) !important;
            transition: all 0.5s ease-in-out !important;
        }
        .focus-dimmed-overlay {
            filter: brightness(2.5) !important;
            margin-top: 2vh;
        }
    """

st.markdown(f"""
    <style>
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }}
    .stApp {{
        background-color: #0B0F19;
        color: #FFFFFF !important;
    }}
    div[data-testid="stWidgetLabel"] label, 
    div[data-testid="stWidgetLabel"] p,
    .stSlider label, .stNumberInput label, .stTextInput label, 
    .stSelectbox label, .stTextArea label, .stCheckbox label span {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }}
    textarea, input {{
        color: #FFFFFF !important;
        background-color: #1A2234 !important;
        border: 1px solid #38BDF8 !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: #111827 !important;
        border-right: 1px solid #1E293B;
    }}
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {{
        color: #F8FAFC !important;
        font-weight: 600;
    }}
    .brand-header {{
        background: linear-gradient(90deg, #1E293B 0%, #0F172A 100%);
        padding: 1.25rem 1.75rem;
        border-radius: 12px;
        border: 1px solid #38BDF8;
        margin-bottom: 1.5rem;
    }}
    .brand-title {{
        font-size: 2.2rem;
        font-weight: 800;
        color: #38BDF8 !important;
        margin: 0;
    }}
    .brand-tagline {{
        color: #CBD5E1;
        font-size: 1rem;
        margin-top: 4px;
        margin-bottom: 0;
    }}
    h1, h2, h3 {{
        color: #38BDF8 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        color: #34D399 !important;
        font-weight: 800 !important;
    }}
    div[data-testid="stMetricLabel"] {{ color: #FFFFFF !important; }}
    .stButton>button {{
        background-color: #0284C7;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: 1px solid #38BDF8;
        padding: 0.5rem 1rem;
        font-weight: 700;
    }}
    .stButton>button:hover {{
        background-color: #0369A1;
        border-color: #38BDF8;
    }}
    .focus-dimmed-overlay {{
        background-color: #030407;
        border: 2px solid #0284C7;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 0 50px rgba(56, 189, 248, 0.35);
        max-width: 800px;
        margin: 0 auto;
    }}
    .focus-timer-display {{
        font-size: 5.5rem;
        font-weight: 900;
        color: #38BDF8;
        letter-spacing: 4px;
        text-shadow: 0 0 25px rgba(56, 189, 248, 0.7);
        margin: 1rem 0;
    }}
    .focus-gentle-msg {{
        color: #94A3B8;
        font-size: 1.3rem;
        font-style: italic;
    }}
    {dimmed_mode_css}
    </style>
""", unsafe_allow_html=True)

# Request System OS Desktop Notification Permission
st.components.v1.html("""
    <script>
        if ("Notification" in window && Notification.permission !== "granted") {
            Notification.requestPermission();
        }
    </script>
""", height=0)

# ---------------------------------------------------------
# Welcome Intro Popup
# ---------------------------------------------------------
@st.dialog("👋 Welcome to FocusMate AI")
def show_welcome_popup():
    st.markdown("""
    ### 🧠 What is FocusMate?
    FocusMate is a digital workspace built specifically for teenagers, students, and young adults. It aims to:
    * **Overcome Overthinking:** Untangle anxiety loops and unburden chaotic thoughts in a safe space.
    * **Build Organic Focus:** Help youth stay productive naturally—without rigid streak pressure, loud alarms, or guilt.

    ---
    
    #### 🔒 Bright Privacy & Data Safety Disclaimer
    """, unsafe_allow_html=True)
    
    st.error("""
    🛡️ **Your Privacy Comes First:**  
    All entries, mood logs, thoughts, and biometric inputs stay **strictly local** within your active session. FocusMate does **not** sell, track, or share your personal mental health data with any third parties.
    """)
    
    st.divider()
    if st.button("🚀 Continue to Workspace", type="primary", use_container_width=True):
        st.session_state.intro_seen = True
        st.rerun()

if not st.session_state.intro_seen:
    show_welcome_popup()

# ---------------------------------------------------------
# Top Banner Header & Sidebar
# ---------------------------------------------------------
st.markdown("""
    <div class="brand-header">
        <h1 class="brand-title">🧠 FocusMate AI</h1>
        <p class="brand-tagline">Youth Mental Well-Being & Organic Digital Focus Engine</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color:#38BDF8; margin-bottom:0;'>🧠 FocusMate AI</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#CBD5E1; font-size:0.9rem;'>Empowering Youth Well-Being & Focus</p>", unsafe_allow_html=True)
st.sidebar.divider()

navigation = st.sidebar.radio(
    "Explore Workspace:",
    [
        "👤 Profile Dashboard",
        "🧘 Daily Mood Tracker",
        "🤖 Biometric Burnout & AI Predictor",
        "🌿 Anti-Gamification & Calm",
        "🎯 Personalized Focus Planner"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 **Design Goal:** Reduce overthinking, prevent burnout, and foster guilt-free productivity.")

SCALER_PATH = "scaler.pkl"
MODEL_PATH = "focusmate_model.pkl"

# =========================================================
# FEATURE 1: PROFILE DASHBOARD (DAILY GOALS WITH 11:59 PM RESET)
# =========================================================
if navigation == "👤 Profile Dashboard":
    st.subheader("👤 User Profile & Daily Goal Engine")
    st.write("Set target baselines for **Today**. All goals automatically reset at **11:59 PM** to give you a fresh daily start.")
    st.divider()
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.write("### 📋 Personal Info")
        name = st.text_input("Full Name", value="")
        age = st.number_input("Age", min_value=10, max_value=100, value=18, step=1)
        occupation = st.text_input("Occupation / Major", value="")
        gender = st.selectbox("Gender", ["Male", "Female","Prefer not to say"])
        
    with col2:
        st.write("### 🎯 Today's Goals (Resets at 11:59 PM)")
        screen_goal = st.slider("Max Screen Time Target (Hours)", 1, 12, 4, step=1)
        focus_goal = st.slider("Focus Sessions Target / Day", 1, 10, 4, step=1)
        sleep_goal = st.slider("Sleep Target (Hours)", 4, 12, 8, step=1)
        water_goal = st.slider("Water Goal (Glasses)", 2, 15, 8, step=1)

    st.divider()
    st.write("### 📊 Today's Progress vs Target")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    g_col1.metric("Screen Limit Target", f"{int(screen_goal)} hrs")
    g_col2.metric("Focus Sessions Done", f"{st.session_state.completed_sessions_today} / {int(focus_goal)}")
    g_col3.metric("Sleep Target", f"{int(sleep_goal)} hrs")
    g_col4.metric("Water Drank Today", f"{st.session_state.water_drank_today} / {int(water_goal)} glasses")

    st.info("⏰ **Daily Tracking:** Your focus sessions completed in Feature 5 automatically update this dashboard.")

# =========================================================
# FEATURE 2: DAILY MOOD TRACKER & THOUGHT DISSOLVE
# =========================================================
elif navigation == "🧘 Daily Mood Tracker":
    st.subheader("🧘 Daily Mood Check-In & Thought Dump")
    st.write("A zero-judgment space to express your feelings and unburden overthinking loops.")
    st.divider()
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.write("### 💭 Log Current State")
        mood = st.select_slider("How are you feeling right now?", options=["Very Low", "Low", "Neutral", "Good", "Excellent"])
        stress_lvl = st.slider("Perceived Stress (1 - 10)", 1, 10, 5, step=1)
        sleep_hrs = st.slider("Sleep Last Night (Hours)", 0, 12, 7, step=1)
        
    with col2:
        st.write("### 🔥 Mind Unburden Canvas")
        st.caption("Externalize racing thoughts. Click 'Release & Dissolve' to unburden your mind into the void without leaving a digital trace.")
        
        journal_entry = st.text_area("Write out any chaotic thoughts or anxieties here...", value=st.session_state.thought_dump_input, height=160, key="dump_area")
        
        if st.button("✨ Release & Dissolve Thought", type="primary"):
            st.session_state.thought_dump_input = ""
            st.success("🌊 Thought unburdened and dissolved into the void! Taking it out of your head brings instant mental calm.")
            st.rerun()

# =========================================================
# FEATURE 3: AI BIOMETRIC BURNOUT PREDICTOR (FIXED LOGIC)
# =========================================================
elif navigation == "🤖 Biometric Burnout & AI Predictor":
    st.subheader("🤖 AI Biometric Burnout Predictor")
    st.write("Evaluates focus capability and burnout risk with machine learning and fail-safe health logic.")
    st.divider()
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.write("### 📥 Input Daily Metrics")
        input_sleep = st.slider("Average Sleep Duration (Hours)", 0, 12, 7, step=1)
        input_stress = st.slider("Current Stress Level (1 - 10)", 1, 10, 5, step=1)
        input_screen = st.slider("Screen Time Today (Hours)", 0, 15, 4, step=1)
        analyze_btn = st.button("Run AI Prediction", type="primary", use_container_width=True)

    with col2:
        st.write("### 🎯 Machine Learning Output")
        if analyze_btn:
            try:
                # 1. Base ML model prediction attempt
                try:
                    with open(r"C:\Users\Shahbaz\Desktop\AI CAPSTONE\scaler.pkl", 'rb') as sf: scaler = pickle.load(sf)
                    with open(r"C:\Users\Shahbaz\Desktop\AI CAPSTONE\focusmate_model.pkl", 'rb') as mf: model = pickle.load(mf)
                    raw_data = np.array([[float(input_sleep), float(input_stress), float(input_screen)]])
                    scaled_data = scaler.transform(raw_data)
                    predicted_score = float(model.predict(scaled_data)[0])
                except:
                    predicted_score = 50.0

                # 2. FAILSAFE HEALTH GUARDRAILS: Sleep, stress, and screen time MUST adjust the score realistically
                health_score = (input_sleep / 8.0) * 40.0 + ((10.0 - input_stress) / 10.0) * 35.0 + max(0.0, (10.0 - input_screen) / 10.0) * 25.0
                
                # Heavy penalty override for extreme low sleep / high stress
                if input_sleep <= 4 or input_stress >= 8 or input_screen >= 10:
                    score_display = int(min(predicted_score, health_score, 35.0))
                else:
                    score_display = int(round(max(5.0, min(100.0, (predicted_score + health_score) / 2.0))))

                st.metric(label="Predicted Focus Capacity / Readiness Score", value=f"{score_display}%")
                st.progress(score_display / 100.0)
                
                st.markdown("### 🌿 AI Recommendation:")
                if score_display >= 75:
                    st.success("🟢 **Low Burnout Risk / High Readiness:** You are in a strong mental state for deep work.")
                elif score_display >= 50:
                    st.warning("🟠 **Moderate Risk:** Work in shorter 20-minute focus windows. Schedule breaks.")
                else:
                    st.error("🔴 **High Fatigue / Burnout Warning:** Extreme strain detected (low sleep or high stress/screen time). Prioritize rest today!")

            except Exception as e:
                st.error(f"Prediction Error: {e}")
        else:
            st.info("Adjust the biometric inputs and click **Run AI Prediction** to compute your readiness.")

# =========================================================
# FEATURE 4: HOLISTIC ANTI-GAMIFICATION & CALM DASHBOARD
# =========================================================
elif navigation == "🌿 Anti-Gamification & Calm":
    st.subheader("🌿 Anti-Gamification & Calm Dashboard")
    st.write("Encouraging holistic digital habits by balancing movement, rest, breaks, and screen time.")
    st.divider()
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.write("### 📊 Daily Habit Balance")
        s_time = st.slider("Screen Time Today (Hours)", 0, 15, 4, step=1)
        soc_media = st.slider("Social Media Usage (Hours)", 0, 10, 1, step=1)
        sleep_last_night = st.slider("Sleep Last Night (Hours)", 0, 12, 7, step=1)
        breaks_taken = st.slider("Healthy Breaks Taken Today", 0, 15, 5, step=1)
        physical_movement = st.slider("Physical Movement (Stretches / Walks)", 0, 15, 3, step=1)

    with col2:
        st.write("### 🧘 The Holistic Calm Meter")
        
        # HOLISTIC CALM CALCULATION: Rewards physical/sleep habits while softly deducting screen fatigue
        calm_score = 50 # Base start
        
        # Positive Wellness Anchors (+)
        if sleep_last_night >= 7: calm_score += 15
        if physical_movement >= 2: calm_score += 15
        if breaks_taken >= 4: calm_score += 15
        
        # Digital Fatigue Deductions (-)
        if s_time > 6: calm_score -= 15
        if soc_media > 3: calm_score -= 15
        
        calm_score = max(5, min(100, calm_score))
        
        st.metric("Calm Index Score", f"{int(calm_score)} / 100")
        st.progress(calm_score / 100.0)
        
        st.write("### 🌱 Your Digital Garden Status")
        if calm_score >= 75:
            st.success("🪴 **Flourishing:** Your habits, sleep, and physical movement are in gentle balance today.")
        elif calm_score >= 45:
            st.warning("🌱 **Growing:** Doing okay, but consider standing up for a quick stretch or stepping away from social media.")
        else:
            st.error("🥀 **Drained:** High digital noise detected. Step away from screen without guilt.")

# =========================================================
# FEATURE 5: PERSONALIZED FOCUS PLANNER & IMMERSIVE FOCUS ROOM
# =========================================================
elif navigation == "🎯 Personalized Focus Planner":

    # Early Exit Notice if user left previous session early
    if st.session_state.early_exit_triggered and not st.session_state.in_focus_room:
        st.error("""
        🤖 **AI Companion Notice:**  
        *"Hey there! I noticed you stepped out of your Focus Room early. Don't worry—there's no penalty or rush. Take a soft breath, regroup, and enter whenever you feel ready again to keep going. :)"*
        """)
        st.components.v1.html("""
            <script>
                var msg = new SpeechSynthesisUtterance("Hey there! I noticed you stepped out early. Take a breath and take your time. You can do this!");
                msg.volume = 0.8;
                window.speechSynthesis.speak(msg);
            </script>
        """, height=0)
        if st.button("Acknowledge & Clear Alert"):
            st.session_state.early_exit_triggered = False
            st.rerun()

    # MODE A: FOCUS ROOM IS ACTIVE
    if st.session_state.in_focus_room:
        
        # 1. Inject Tab Switch / Minimize OS Desktop Notification Listener
        st.components.v1.html("""
            <script>
                document.addEventListener("visibilitychange", function() {
                    if (document.hidden) {
                        if (Notification.permission === "granted") {
                            new Notification("🧠 FocusMate Alert!", {
                                body: "You switched away from your Focus Room! Return to stay on track.",
                                icon: "https://em-content.zobj.net/source/apple/354/brain_1f9e0.png"
                            });
                        }
                        let ctx = new (window.AudioContext || window.webkitAudioContext)();
                        let osc = ctx.createOscillator();
                        osc.type = "sine";
                        osc.frequency.setValueAtTime(440, ctx.currentTime);
                        osc.connect(ctx.destination);
                        osc.start();
                        osc.stop(ctx.currentTime + 0.5);

                        var msg = new SpeechSynthesisUtterance("Please return to your focus room to stay on track!");
                        msg.volume = 1.0;
                        window.speechSynthesis.speak(msg);
                    }
                });
            </script>
        """, height=0)

        # 2. Responsive Leave Early Button BEFORE timer loop so it is immediately clickable!
        col_x, col_y, col_z = st.columns([1, 2, 1])
        with col_y:
            if st.button("🚪 Leave Focus Room Early", type="secondary", use_container_width=True):
                st.session_state.in_focus_room = False
                st.session_state.early_exit_triggered = True
                st.rerun()

        # 3. Live Countdown Timer Loop
        timer_placeholder = st.empty()
        total_seconds = st.session_state.focus_minutes * 60
        
        for remaining in range(total_seconds, -1, -1):
            if not st.session_state.in_focus_room:
                break
                
            mins, secs = divmod(remaining, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            
            timer_placeholder.markdown(f"""
                <div class="focus-dimmed-overlay">
                    <h2 style="color: #38BDF8 !important; font-size: 2.2rem; margin-bottom: 0.5rem;">🧘 Focus Room Active</h2>
                    <p style="color: #E2E8F0; font-size: 1.4rem;"><b>Target Objective:</b> {st.session_state.focus_task}</p>
                    <div class="focus-timer-display">{time_format}</div>
                    <p class="focus-gentle-msg">to keep going... :)</p>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1)

        if remaining == 0 and st.session_state.in_focus_room:
            st.balloons()
            st.session_state.completed_sessions_today += 1
            st.success("🎉 Excellent session! Session credited to today's profile goals.")
            st.session_state.in_focus_room = False

    # MODE B: SETUP FOCUS SESSION FORM
    else:
        st.subheader("🎯 Gentle Focus Room Setup")
        st.write("State your objective to unlock an ambient, full-screen dimmed focus session.")
        st.divider()

        col_a, col_b, col_c = st.columns([1, 3, 1])
        with col_b:
            st.write("### 🚪 Enter Focus Room")
            task_input = st.text_input("What do you want to focus upon right now?", placeholder="e.g. Read Chapter 3 of Computer Science textbook")
            timer_duration = st.number_input("Session Duration (Minutes)", min_value=1, max_value=120, value=25, step=1)
            
            st.write("")
            if st.button("🚀 Enter Immersive Focus Room", type="primary", use_container_width=True):
                if task_input.strip() != "":
                    st.session_state.focus_task = task_input
                    st.session_state.focus_minutes = int(timer_duration)
                    st.session_state.in_focus_room = True
                    st.session_state.early_exit_triggered = False
                    st.rerun()
                else:
                    st.warning("Please enter what you want to focus upon before entering.")