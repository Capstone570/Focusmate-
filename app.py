import streamlit as st
import streamlit.components.v1 as components
import time

# ------------------------------------------------------------------------------
# 1. PAGE CONFIG & SOFT PASTEL DARK THEME
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Focusmate AI", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    /* Dark Soft Aesthetic Background */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1f1a24 100%);
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #f0f6fc;
    }

    /* Soft Floating Glass Card Container */
    .robot-container {
        background: rgba(30, 27, 46, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 28px;
        padding: 24px;
        text-align: center;
        border: 1px solid rgba(192, 132, 252, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
    }

    /* Pastel Speech Bubble */
    .speech-bubble {
        background: linear-gradient(135deg, #e9d5ff 0%, #fbcfe8 100%);
        border-radius: 20px;
        padding: 18px 28px;
        color: #1e1b2e !important;
        font-size: 19px;
        font-weight: 700;
        display: inline-block;
        margin-top: 15px;
        box-shadow: 0 8px 20px rgba(233, 213, 255, 0.2);
    }

    /* Soft Pastel Cards */
    .float-card {
        background: rgba(30, 35, 45, 0.6);
        border: 1px solid rgba(168, 85, 247, 0.25);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 18px;
        transition: transform 0.2s ease;
    }

    /* FIXED: High-Contrast Pastel Labels */
    .stApp label, .stApp p, .stApp span {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    /* Soft Rounded Input Area */
    .stTextArea textarea {
        background: #161b22 !important;
        border: 1px solid #3b4252 !important;
        color: #f8fafc !important;
        border-radius: 14px !important;
    }

    /* Action Buttons (Pastel Gradient) */
    div.stButton > button {
        background: linear-gradient(135deg, #c084fc 0%, #f472b6 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        border-radius: 18px !important;
        border: none !important;
        padding: 16px 32px !important;
        box-shadow: 0 10px 25px rgba(192, 132, 252, 0.3) !important;
        width: 100%;
    }

    /* Solution Box */
    .solution-panel {
        background: rgba(45, 27, 61, 0.5);
        border: 2px solid #c084fc;
        border-radius: 24px;
        padding: 25px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# ------------------------------------------------------------------------------
# 2. SAFE CANVAS COMPONENT (NO KEY PARAMETER CRASH)
# ------------------------------------------------------------------------------
def render_robot_mascot(height=260):
    canvas_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; background: transparent; display: flex; justify-content: center; align-items: center; }}
            canvas {{ background: transparent; }}
        </style>
    </head>
    <body>
    <canvas id="robotCanvas" width="220" height="220"></canvas>
    <script>
        const canvas = document.getElementById('robotCanvas');
        const ctx = canvas.getContext('2d');
        let frame = 0;

        function drawRobot() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            frame += 0.04;
            
            const hover = Math.sin(frame) * 8;
            const centerX = 110;
            const centerY = 110 + hover;

            // Soft Glow Aura
            const gradient = ctx.createRadialGradient(centerX, centerY, 10, centerX, centerY, 85);
            gradient.addColorStop(0, 'rgba(192, 132, 252, 0.35)');
            gradient.addColorStop(1, 'rgba(192, 132, 252, 0)');
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(centerX, centerY, 85, 0, Math.PI * 2);
            ctx.fill();

            // Antenna Orb
            ctx.fillStyle = '#f472b6';
            ctx.beginPath();
            ctx.arc(centerX, centerY - 65, 8, 0, Math.PI * 2);
            ctx.fill();

            // Antenna Stem
            ctx.strokeStyle = '#cbd5e1';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY - 57);
            ctx.lineTo(centerX, centerY - 42);
            ctx.stroke();

            // Head (Soft Pastel Lavender Body)
            ctx.fillStyle = '#c084fc';
            ctx.beginPath();
            ctx.roundRect(centerX - 48, centerY - 42, 96, 68, 22);
            ctx.fill();

            // Face Screen (Dark Gloss)
            ctx.fillStyle = '#1e1b2e';
            ctx.beginPath();
            ctx.roundRect(centerX - 38, centerY - 32, 76, 48, 14);
            ctx.fill();

            // Glowing Pastel Eyes
            const blink = Math.sin(frame * 0.8) > 0.95 ? 2 : 10;
            ctx.fillStyle = '#38bdf8';
            ctx.beginPath();
            ctx.ellipse(centerX - 18, centerY - 8, 7, blink, 0, 0, Math.PI * 2);
            ctx.ellipse(centerX + 18, centerY - 8, 7, blink, 0, 0, Math.PI * 2);
            ctx.fill();

            // Cute Cheeks
            ctx.fillStyle = 'rgba(244, 114, 182, 0.5)';
            ctx.beginPath();
            ctx.arc(centerX - 26, centerY + 5, 6, 0, Math.PI * 2);
            ctx.arc(centerX + 26, centerY + 5, 6, 0, Math.PI * 2);
            ctx.fill();

            // Torso
            ctx.fillStyle = '#a855f7';
            ctx.beginPath();
            ctx.roundRect(centerX - 30, centerY + 32, 60, 40, 16);
            ctx.fill();

            // Heart/Core Badge
            ctx.fillStyle = '#f472b6';
            ctx.beginPath();
            ctx.arc(centerX, centerY + 50, 7, 0, Math.PI * 2);
            ctx.fill();

            requestAnimationFrame(drawRobot);
        }}
        drawRobot();
    </script>
    </body>
    </html>
    """
    # Removed the key argument completely to prevent Streamlit TypeError
    components.html(canvas_html, height=height)

# ------------------------------------------------------------------------------
# PAGE 1: WELCOME SCREEN
# ------------------------------------------------------------------------------
if st.session_state.page == 'welcome':
    st.write("")
    st.write("")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown('<div class="robot-container">', unsafe_allow_html=True)
        render_robot_mascot(240)
        st.markdown("""
            <div class="speech-bubble">
                "Welcome to Focusmate! Ready to clear brain fog and get into the zone?" ✨
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("🚀 Let's Dive In!"):
            st.session_state.page = 'workspace'
            st.rerun()

# ------------------------------------------------------------------------------
# PAGE 2: WORKSPACE
# ------------------------------------------------------------------------------
elif st.session_state.page == 'workspace':
    st.markdown('<div class="robot-container">', unsafe_allow_html=True)
    render_robot_mascot(200)
    st.markdown("""
        <div class="speech-bubble">
            "Configure your 5 session parameters below, and I'll generate a custom study solution for you." 🧠
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #c084fc; font-weight: 700; margin-bottom: 20px;'>🛸 Floating Mission Inputs</h3>", unsafe_allow_html=True)

    st.markdown('<div class="float-card">', unsafe_allow_html=True)
    user_thoughts = st.text_area(
        "💬 1. Mind Dump (Venting, doubts, or thoughts occupying your brain):",
        placeholder="e.g., I have an exam tomorrow, my mind is spiraling with doubts, and I can't seem to start...",
        height=95
    )
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="float-card">', unsafe_allow_html=True)
        study_hours = st.number_input("📚 2. Target Study Time (Whole Hours)", min_value=1, max_value=12, value=3, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="float-card">', unsafe_allow_html=True)
        sleep_quality = st.slider("😴 3. Sleep Quality Score (1-10)", min_value=1, max_value=10, value=7, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="float-card">', unsafe_allow_html=True)
        task_difficulty = st.slider("🎯 4. Task Difficulty Level (1-10)", min_value=1, max_value=10, value=6, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="float-card">', unsafe_allow_html=True)
        energy_level = st.slider("⚡ 5. Energy Level (1-10)", min_value=1, max_value=10, value=8, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("✨ Analyze Mind State & Generate Solution ✨"):
        if not user_thoughts.strip():
            st.warning("Please type a few words into the Mind Dump box first!")
        else:
            with st.spinner("FocusBot is analyzing your parameters..."):
                time.sleep(1)

            stress_words = ["stress", "anxious", "fail", "scared", "can't", "overwhelmed", "spiraling", "doubt", "hard"]
            stress_score = sum(2 for word in stress_words if word in user_thoughts.lower())

            raw_focus = (sleep_quality * 5) + (energy_level * 4) + ((11 - task_difficulty) * 3) - (stress_score * 6)
            focus_capacity = int(min(max(raw_focus + 10, 15), 98))

            st.balloons()

            st.markdown(f"""
            <div class="solution-panel">
                <div style="text-align: center;">
                    <span style="background: #c084fc; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 14px; color: #ffffff;">ANALYSIS COMPLETE</span>
                    <h1 style="color: #ffffff; font-size: 34px; margin-top: 10px;">Predicted Focus Capacity: {focus_capacity}%</h1>
                </div>
                <hr style="border-color: rgba(192, 132, 252, 0.3); margin: 20px 0;">
                <h3 style="color: #f472b6; margin-bottom: 15px;">🤖 FocusBot's AI Action Plan:</h3>
            """, unsafe_allow_html=True)

            if focus_capacity < 60:
                st.markdown("""
                * **1. Brain Dump Protocol:** Write down the 2 biggest worries racing in your head on a piece of paper, then close the notebook.
                * **2. The 5-Minute Trick:** Commit to studying for just **5 minutes**. If you want to stop after 5 minutes, you can.
                * **3. Micro-Tasks:** Break your goal into tiny 1-step actions (e.g., *"Open document"* instead of *"Write essay"*).
                """)
            else:
                st.markdown("""
                * **1. Clear Horizon:** You have high focus potential today! Close all extra browser tabs and put your phone face down.
                * **2. 25/5 Deep Sprint:** Set a timer for 25 minutes of continuous execution, followed by a 5-minute break.
                * **3. Active Practice:** Focus on solving problems or quizzing yourself rather than passive reading.
                """)

            st.markdown("</div>", unsafe_allow_html=True)
