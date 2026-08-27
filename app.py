import streamlit as st
import time

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & AESTHETIC CSS
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Focusmate", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #fff5f8 0%, #f3e8ff 100%);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Robot Card Container */
    .robot-card {
        background: white;
        border-radius: 30px;
        padding: 30px;
        text-align: center;
        box-shadow: 0px 15px 35px rgba(220, 170, 230, 0.25);
        border: 2px solid #f5d8ee;
        margin-bottom: 25px;
    }

    /* Floating Robot Icon Animation */
    .big-robot {
        font-size: 90px;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* Interactive Speech Bubble */
    .speech-box {
        background-color: #fcf0f8;
        border: 2px solid #f0c2e0;
        border-radius: 20px;
        padding: 15px 25px;
        font-size: 20px;
        font-weight: 600;
        color: #5d2a50;
        margin-top: 15px;
        display: inline-block;
    }

    /* Styled Feature Cards */
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0px 8px 20px rgba(220, 170, 230, 0.15);
        border: 1px solid #f0d8eb;
        margin-bottom: 15px;
    }

    /* Custom Gradient Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%) !important;
        color: #4a1525 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 12px 30px !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. FEATURE 1: FULL-SCREEN FOCUSBOT WELCOME HERO
# ------------------------------------------------------------------------------
st.markdown("""
<div class="robot-card">
    <div class="big-robot">🤖✨</div>
    <h2>Hi! Welcome to Focusmate!</h2>
    <div class="speech-box">
        "I'm FocusBot! I'll help you organize your study session, boost your concentration, and celebrate your wins! 🌸"
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. INTERACTIVE TABS FOR APP FEATURES
# ------------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Focus Predictor", 
    "⏱️ Pomodoro Timer", 
    "📝 AI Routine Generator", 
    "🏆 Badges & Rewards"
])

# --- TAB 1: DYNAMIC FOCUS PREDICTOR ---
with tab1:
    st.markdown("### 📊 Interactive Focus Engine")
    
    col1, col2 = st.columns(2)
    with col1:
        mood = st.selectbox("💭 Current Mood / State", ["😊 Energized & Ready", "🥱 A Bit Tired", "🤯 Overwhelmed", "☕ Fully Caffeinated"])
        sleep = st.slider("😴 Sleep Last Night (Hours)", 0.0, 12.0, 7.5, 0.5)
        
    with col2:
        task_type = st.selectbox("📚 Task Complexity", ["Light (Emails/Organizing)", "Medium (Reading/Homework)", "Heavy (Coding/Exams)"])
        distractions = st.select_slider("📱 Notification Distractions", options=["None", "Low", "Moderate", "High"])

    # Calculate Score Dynamically
    base_score = 50
    if "Energized" in mood: base_score += 20
    elif "Tired" in mood: base_score -= 15
    
    base_score += int(sleep * 3)
    if distractions == "High": base_score -= 20

    final_score = min(max(base_score, 10), 100)

    st.write("")
    if st.button("✨ Predict My Focus Score ✨"):
        with st.spinner("FocusBot is calculating..."):
            time.sleep(1)
        st.balloons()
        
        st.markdown(f"""
        <div style="background: white; border-radius: 20px; padding: 20px; text-align: center; border: 2px solid #a5d6a7;">
            <h2 style="color: #2e7d32; margin:0;">🎉 Your Predicted Focus Score: {final_score}%</h2>
            <p style="color: #555; font-size: 16px;">FocusBot says: {'Awesome state! Dive into deep work now.' if final_score > 70 else 'Take a quick 5-min walk and grab water first!'}</p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: INTERACTIVE POMODORO TIMER ---
with tab2:
    st.markdown("### ⏱️ FocusBot Pomodoro Timer")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        minutes = st.number_input("Set Timer (Minutes)", min_value=1, max_value=60, value=25)
    with t_col2:
        ambient = st.selectbox("🎧 Ambient Background Sound", ["Rainfall 🌧️", "Cozy Cafe ☕", "Library Quiet 📚"])

    if st.button("▶️ Start Focus Session"):
        st.info(f"Focus Mode Active ({ambient})! FocusBot is guarding your time... 🛑📱")
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.05) # Simulated timer progression for quick demo
            progress_bar.progress(i + 1)
        st.success("🎉 Time's up! Great job! Take a 5-minute break.")
        st.balloons()

# --- TAB 3: ROUTINE GENERATOR ---
with tab3:
    st.markdown("### 📝 Smart Study Routine")
    subject = st.text_input("What are you studying today?", "Machine Learning")
    if st.button("✨ Generate Custom Plan"):
        st.markdown(f"""
        <div class="feature-card">
            <h4>📋 FocusBot's Tailored Plan for {subject}:</h4>
            <ul>
                <li><b>Block 1 (25 mins):</b> High intensity review of core concepts.</li>
                <li><b>Break (5 mins):</b> Hydrate & do light stretching.</li>
                <li><b>Block 2 (25 mins):</b> Practice problems & active recall.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 4: ACHIEVEMENTS & BADGES ---
with tab4:
    st.markdown("### 🏆 Your Focus Badges")
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown("<div class='feature-card' style='text-align:center;'><h1>🤿</h1><b>Deep Diver</b><br><small>Completed 25m Focus</small></div>", unsafe_allow_html=True)
    with b_col2:
        st.markdown("<div class='feature-card' style='text-align:center;'><h1>🌅</h1><b>Early Bird</b><br><small>Logged in before 9 AM</small></div>", unsafe_allow_html=True)
    with b_col3:
        st.markdown("<div class='feature-card' style='text-align:center;'><h1>🤖</h1><b>FocusBot's Bestie</b><br><small>Used 3 Features</small></div>", unsafe_allow_html=True)
