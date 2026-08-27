import streamlit as st
import time

# ------------------------------------------------------------------------------
# 1. PAGE CONFIG & HIGH-CONTRAST THEME
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Focusmate AI | Deep Work Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'seconds_left' not in st.session_state:
    st.session_state.seconds_left = 25 * 60
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Sidebar Navigation & Settings
with st.sidebar:
    st.title("🤖 Focusmate AI")
    st.caption("Cognitive Load & Study Optimization Engine")
    st.divider()
    
    current_page = st.radio("Navigation", ["Landing Hero", "Focus Workspace"], 
                            index=0 if st.session_state.page == 'welcome' else 1)
    st.session_state.page = 'welcome' if current_page == "Landing Hero" else 'workspace'
    
    st.divider()
    st.subheader("🎧 Ambient Soundscapes")
    ambient_sound = st.selectbox("Select Background Audio", [
        "None", 
        "🌧️ Deep Rain & Thunder", 
        "🌊 Ocean Waves (Delta Waves)", 
        "🧠 Brown Noise (ADHD Focus)", 
        "☕ Cyberpunk Cafe Lo-Fi"
    ])
    
    if ambient_sound != "None":
        st.info(f"Audio Active: **{ambient_sound}**")

# ------------------------------------------------------------------------------
# PAGE 1: LANDING HERO SCREEN
# ------------------------------------------------------------------------------
if st.session_state.page == 'welcome':
    st.title("🤖 Focusmate AI")
    st.subheader("Turn Brain Fog & Overthinking Into Instant Actionable Execution")
    
    st.markdown("""
    Focusmate AI is built for students, builders, and chronic overthinkers. 
    Instead of staring at an overwhelming to-do list, dump your raw thoughts, diagnose your current mental state, and let AI structure your exact deep-work sprint.
    """)
    
    st.divider()
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown("### 🚀 Core Platform Features")
        st.markdown("""
        * **💬 AI Thought Unpacker:** Convert venting & anxiety into clear 5-minute micro-tasks.
        * **⚡ Dynamic Focus Scoring:** Calculate realistic work limits using energy & sleep metrics.
        * **⏱️ Integrated Sprint Timer:** Built-in Pomodoro/Deep Work timer with live visual progress.
        * **🎧 Ambient Audio Engine:** Integrated soundscapes tailored to reduce distraction.
        * **🎯 Task Execution Board:** Track active session micro-sprints without context switching.
        """)
        
        st.write("")
        if st.button("🚀 Let's Dive In!", use_container_width=True, type="primary"):
            st.session_state.page = 'workspace'
            st.rerun()

# ------------------------------------------------------------------------------
# PAGE 2: WORKSPACE & AI ENGINE
# ------------------------------------------------------------------------------
elif st.session_state.page == 'workspace':
    st.title("🧠 Deep Work Command Center")
    st.caption("Configure your session parameters below to initialize your personalized study sprint.")
    
    st.divider()
    
    # 5 Floating Feature Cards Setup
    st.subheader("🛸 Session Inputs & Cognitive Parameters")
    
    # Feature 1: Mind Dump
    user_thoughts = st.text_area(
        "💬 1. Mind Dump (Vent your raw thoughts, anxieties, doubts, or task confusion):",
        placeholder="e.g., I have an exam tomorrow, I haven't started chapter 4, my mind is spiraling with doubts, and I feel completely paralyzed...",
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        study_hours = st.number_input("📚 2. Target Work Allocation (Whole Hours)", min_value=1, max_value=12, value=3, step=1)
        sleep_quality = st.slider("😴 3. Sleep Quality Score (1-10)", min_value=1, max_value=10, value=7, step=1)
        
    with col2:
        task_difficulty = st.slider("🎯 4. Task Complexity Level (1-10)", min_value=1, max_value=10, value=6, step=1)
        energy_level = st.slider("⚡ 5. Energy Level (1-10)", min_value=1, max_value=10, value=8, step=1)

    st.write("")
    if st.button("✨ Unpack Mind & Generate Focus Plan ✨", use_container_width=True, type="primary"):
        if not user_thoughts.strip():
            st.warning("Please type a few words into the Mind Dump box first to run the analysis.")
        else:
            with st.spinner("Analyzing mental load and generating micro-tasks..."):
                time.sleep(1.2)
                
            # Energy & Focus Calculation Engine
            stress_keywords = ["stress", "anxious", "fail", "scared", "can't", "overwhelmed", "spiraling", "doubt", "hard"]
            detected_stress_points = sum(2 for word in stress_keywords if word in user_thoughts.lower())
            
            raw_score = (sleep_quality * 5) + (energy_level * 4) + ((11 - task_difficulty) * 3) - (detected_stress_points * 6)
            focus_capacity = int(min(max(raw_score + 10, 15), 98))
            
            st.session_state.focus_capacity = focus_capacity
            st.session_state.analysis_complete = True
            
            # Generate Dynamic Micro-Tasks
            if focus_capacity < 60:
                st.session_state.recommended_sprint = 15
                st.session_state.tasks = [
                    "Perform 2-minute brain dump on physical paper and close the notebook.",
                    "Complete a 5-minute micro-sprint: Open main reference material only.",
                    "Draft 3 rough bullet points without worrying about quality or perfection."
                ]
            else:
                st.session_state.recommended_sprint = 25
                st.session_state.tasks = [
                    "Silence phone and close all unrelated browser tabs.",
                    "Execute 25-minute deep sprint focused purely on core active recall.",
                    "Review key formulas/concepts and self-quiz for 5 minutes."
                ]
            st.rerun()

    # --------------------------------------------------------------------------
    # RESULTS & INTERACTIVE TIMER ENGINE
    # --------------------------------------------------------------------------
    if st.session_state.analysis_complete:
        st.divider()
        st.header("📊 AI Cognitive Diagnostics & Execution Plan")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Focus Capacity", f"{st.session_state.focus_capacity}%")
        m2.metric("Recommended Sprint", f"{st.session_state.recommended_sprint} mins")
        m3.metric("Burnout Risk Level", "High" if st.session_state.focus_capacity < 50 else "Optimal")
        
        st.subheader("🎯 Generated Actionable Micro-Tasks")
        for idx, task in enumerate(st.session_state.tasks, 1):
            st.checkbox(f"**Step {idx}:** {task}", key=f"task_{idx}")

        st.divider()
        st.subheader("⏱️ Live Focus Sprint Timer")
        
        timer_col1, timer_col2 = st.columns([2, 1])
        
        with timer_col1:
            sprint_seconds = st.session_state.recommended_sprint * 60
            progress_val = min(max(1.0 - (st.session_state.seconds_left / sprint_seconds), 0.0), 1.0)
            
            mins, secs = divmod(st.session_state.seconds_left, 60)
            time_display = f"{mins:02d}:{secs:02d}"
            
            st.markdown(f"## ⏳ Time Remaining: `{time_display}`")
            st.progress(progress_val)
            
            b1, b2, b3 = st.columns(3)
            if b1.button("▶️ Start Sprint"):
                st.session_state.timer_running = True
            if b2.button("⏸️ Pause"):
                st.session_state.timer_running = False
            if b3.button("🔄 Reset Timer"):
                st.session_state.timer_running = False
                st.session_state.seconds_left = st.session_state.recommended_sprint * 60
                st.rerun()

            if st.session_state.timer_running and st.session_state.seconds_left > 0:
                time.sleep(1)
                st.session_state.seconds_left -= 1
                st.rerun()
            elif st.session_state.seconds_left == 0:
                st.balloons()
                st.success("🎉 Focus Sprint Complete! Take a 5-minute rest break.")

        with timer_col2:
            st.info("""
            **Sprint Protocol:**
            * Stay on a single active task.
            * Do not switch tabs until the timer reaches zero.
            * If an off-topic thought pops up, write it down on scrap paper and return to work.
            """)
