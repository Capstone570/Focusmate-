import streamlit as st
import numpy as np
import pickle
import time
import json
import requests
from streamlit_lottie import st_lottie

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & PASTEL DESIGN THEME
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Focusmate | AI Productivity Engine",
    page_icon="🤖",
    layout="wide"
)

# Custom Styling (Pastel Gradient, Rounded Cards, Animations)
st.markdown("""
<style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #fff5f8 0%, #f3e8ff 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Speech Bubble for FocusBot */
    .speech-bubble {
        position: relative;
        background: #ffffff;
        border-radius: 20px;
        padding: 15px 20px;
        color: #5a2a42;
        font-weight: 600;
        box-shadow: 0px 8px 20px rgba(230, 180, 220, 0.3);
        border: 2px solid #f0d5e8;
        margin-bottom: 20px;
    }

    /* Input Card Container */
    [data-testid="stForm"], .css-card {
        background-color: #ffffff !important;
        border-radius: 25px !important;
        padding: 30px !important;
        box-shadow: 0px 10px 30px rgba(210, 170, 220, 0.2) !important;
        border: 1px solid #f5e1f0 !important;
    }

    /* Gradient Action Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%) !important;
        color: #4a1525 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 14px 35px !important;
        box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4) !important;
        width: 100%;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 154, 158, 0.6) !important;
    }

    /* Section Headings */
    h1, h2, h3 {
        color: #5e3a63 !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load Lottie Animations
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load cute robot animation
lottie_robot = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_at4w58ce.json")

# ------------------------------------------------------------------------------
# 2. APP HEADER & FOCUSBOT WELCOME
# ------------------------------------------------------------------------------
col_bot, col_title = st.columns([1, 3])

with col_bot:
    if lottie_robot:
        st_lottie(lottie_robot, height=140, key="robot_welcome")
    else:
        st.markdown("<h1 style='font-size: 80px; text-align: center;'>🤖</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div class="speech-bubble">
        ✨ <b>Beep Boop! I'm FocusBot!</b><br>
        Welcome to Focusmate. Adjust your cognitive metrics below, and I will calculate your optimal focus score! 🌸
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ------------------------------------------------------------------------------
# 3. MODEL & SCALER LOADER
# ------------------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    try:
        model = pickle.load(open("focusmate_model.pkl", "rb"))
        scaler = pickle.load(open("scaler.pkl", "rb"))
        return model, scaler
    except:
        return None, None

model, scaler = load_artifacts()

# ------------------------------------------------------------------------------
# 4. INPUT SECTION (5 NEW ADVANCED FEATURES)
# ------------------------------------------------------------------------------
st.markdown("### 🧠 Neuro-Productivity Inputs")

col1, col2 = st.columns(2)

with col1:
    cognitive_load = st.slider(
        "🧠 1. Cognitive Load Index (1-10)",
        min_value=1, max_value=10, value=6,
        help="How mentally demanding is your current task?"
    )
    
    deep_work_velocity = st.number_input(
        "⚡ 2. Deep Work Velocity (Uninterrupted Hours)",
        min_value=0.0, max_value=12.0, value=3.5, step=0.5,
        help="Continuous hours spent focusing without context switching."
    )
    
    distractions = st.slider(
        "📱 3. Digital Distraction Frequency (Pings / Hr)",
        min_value=0, max_value=50, value=12,
        help="Notifications, tabs opened, or phone checks per hour."
    )

with col2:
    circadian_align = st.select_slider(
        "☀️ 4. Circadian Energy Alignment",
        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        value=8,
        help="1 = Sluggish/Tired timing, 10 = Peak natural alertness window."
    )
    
    recovery_ratio = st.slider(
        "🌿 5. Recovery & Downtime Ratio (%)",
        min_value=5, max_value=50, value=20,
        help="Percentage of work time spent taking active screen-free breaks."
    )

st.write("")

# ------------------------------------------------------------------------------
# 5. PREDICTION & INTERACTIVE POP-UP RESULTS
# ------------------------------------------------------------------------------
if st.button("✨ Calculate My Focus Score ✨"):
    # Animated Loading State
    with st.spinner("🌸 FocusBot is analyzing your neural metrics..."):
        time.sleep(1.2) # Smooth UI delay for pop-up feel
        
        # Prepare Feature Vector
        features = np.array([[
            cognitive_load, 
            deep_work_velocity, 
            distractions, 
            circadian_align, 
            recovery_ratio
        ]])
        
        # ML Inference Logic
        if model is not None and scaler is not None:
            scaled_features = scaler.transform(features)
            predicted_score = float(model.predict(scaled_features)[0])
        else:
            # Smart Mock Math Fallback (if raw models are not yet retrained)
            base_score = (deep_work_velocity * 12) + (circadian_align * 4) + (recovery_ratio * 0.5)
            penalty = (distractions * 0.8) + (cognitive_load * 2)
            predicted_score = int(np.clip(base_score - penalty + 40, 10, 99))

    # Trigger Celebratory Animation
    st.balloons()

    # Aesthetic Result Container
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 2])
    
    with res_col1:
        st.metric(
            label="✨ Predicted Focus Score",
            value=f"{predicted_score:.0f}%",
            delta=f"{'High Zone' if predicted_score >= 75 else 'Moderate Zone'}"
        )

    with res_col2:
        # Dynamic Feedback from FocusBot
        if predicted_score >= 80:
            st.success("🎉 **Peak Focus State Detected!** FocusBot says: You are in optimal flow state. Protect this window from all interruptions!")
        elif predicted_score >= 60:
            st.info("💡 **Solid Focus Level!** FocusBot says: Good energy! Lower your phone notifications to gain an extra +10% boost.")
        else:
            st.warning("☕ **High Burnout Risk!** FocusBot says: Your brain needs active recovery. Step away for a 15-minute walk!")
