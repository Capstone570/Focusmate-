import streamlit as st
import streamlit.components.v1 as components
import time

# ------------------------------------------------------------------------------
# 1. PAGE CONFIG & COSMIC THEME
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Focusmate AI", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    /* Gradient Space Canvas */
    .stApp {
        background: linear-gradient(135deg, #0b0d19 0%, #171a2f 50%, #0a0c16 100%);
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #f8fafc;
    }

    /* Glassmorphic Mascot Frame */
    .robot-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 28px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }

    /* Floating Speech Bubble */
    .speech-bubble {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(241,245,249,0.95) 100%);
        border-radius: 20px;
        padding: 16px 30px;
        color: #0f172a;
        font-size: 20px;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
        box-shadow: 0 10px 30px rgba(129, 140, 248, 0.4);
    }

    /* Floating Metric Feature Cards */
    .float-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        backdrop-filter: blur(12px);
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }

    /* Custom Textarea Styling */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #f8fafc !important;
        border-radius: 16px !important;
        font-size: 16px !important;
    }

    /* Action Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 20px !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 18px 36px !important;
        width: 100%;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 45px rgba(168, 85, 247, 0.8) !important;
    }

    /* Solution Panel */
    .solution-panel {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        margin-top: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Multi-Page Flow
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# ------------------------------------------------------------------------------
# 2. 3D MASCOT COMPONENT (THREE.JS - SAFE ESCAPED STRING)
# ------------------------------------------------------------------------------
def render_mascot(height=280):
    threejs_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body { margin: 0; overflow: hidden; background: transparent; }
            canvas { width: 100%; height: 100%; display: block; }
        </style>
    </head>
    <body>
    <script>
        const heightVal = "HEIGHT_PLACEHOLDER";
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / heightVal, 0.1, 1000);
        camera.position.z = 6.5;

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, heightVal);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xc084fc, 1.5);
        dirLight.position.set(5, 5, 5);
        scene.add(dirLight);

        const pointLight = new THREE.PointLight(0x818cf8, 1, 10);
        pointLight.position.set(-3, -2, 2);
        scene.add(pointLight);

        const robotGroup = new THREE.Group();

        // Ditto-Style Soft Blob Body
        const bodyGeo = new THREE.SphereGeometry(1.3, 32, 32);
        const bodyMat = new THREE.MeshStandardMaterial({ 
            color: 0xc084fc, 
            roughness: 0.2, 
            metalness: 0.1
        });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        robotGroup.add(body);

        // Eyes
        const eyeGeo = new THREE.SphereGeometry(0.12, 16, 16);
        const eyeMat = new THREE.MeshBasicMaterial({ color: 0x0f172a });
        
        const eyeLeft = new THREE.Mesh(eyeGeo, eyeMat);
        eyeLeft.position.set(-0.35, 0.2, 1.2);
        robotGroup.add(eyeLeft);

        const eyeRight = new THREE.Mesh(eyeGeo, eyeMat);
        eyeRight.position.set(0.35, 0.2, 1.2);
        robotGroup.add(eyeRight);

        // Smile
        const mouthGeo = new THREE.TorusGeometry(0.15, 0.03, 16, 100, Math.PI);
        const mouthMat = new THREE.MeshBasicMaterial({ color: 0x0f172a });
        const mouth = new THREE.Mesh(mouthGeo, mouthMat);
        mouth.position.set(0, -0.1, 1.22);
        mouth.rotation.x = Math.PI;
        robotGroup.add(mouth);

        scene.add(robotGroup);

        let clock = new THREE.Clock();
        
        function animate() {
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();

            robotGroup.position.y = Math.sin(t * 2) * 0.18;
            robotGroup.rotation.y = Math.sin(t * 1.2) * 0.12;
            robotGroup.scale.x = 1 + Math.sin(t * 2.5) * 0.03;
            robotGroup.scale.y = 1 - Math.sin(t * 2.5) * 0.03;

            if (Math.sin(t * 3.5) > 0.96) {
                eyeLeft.scale.y = 0.1;
                eyeRight.scale.y = 0.1;
            } else {
                eyeLeft.scale.y = 1;
                eyeRight.scale.y = 1;
            }

            renderer.render(scene, camera);
        }
        animate();
    </script>
    </body>
    </html>
    """.replace("HEIGHT_PLACEHOLDER", str(height))
    
    components.html(threejs_code, height=height)

# ------------------------------------------------------------------------------
# PAGE 1: WELCOME SCREEN
# ------------------------------------------------------------------------------
if st.session_state.page == 'welcome':
    st.write("")
    st.write("")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown('<div class="robot-container">', unsafe_allow_html=True)
        render_mascot(300)
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
# PAGE 2: WORKSPACE (5 FLOATING FEATURES + GUIDING MASCOT)
# ------------------------------------------------------------------------------
elif st.session_state.page == 'workspace':
    st.markdown('<div class="robot-container">', unsafe_allow_html=True)
    render_mascot(220)
    st.markdown("""
        <div class="speech-bubble">
            "Configure your 5 floating session parameters below, and I'll generate a custom study solution for you." 🧠
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #c084fc; font-weight: 700; margin-bottom: 20px;'>🛸 Floating Mission Inputs</h3>", unsafe_allow_html=True)

    # Feature 1: Mind Dump
    st.markdown('<div class="float-card">', unsafe_allow_html=True)
    user_thoughts = st.text_area(
        "💬 1. Mind Dump (Venting, doubts, or thoughts occupying your brain):",
        placeholder="e.g., I have an exam tomorrow, my mind is spiraling with doubts, and I can't seem to start...",
        height=90
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Features 2 & 3
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="float-card">', unsafe_allow_html=True)
        study_hours = st.number_input("📚 2. Target Study Time (Whole Hours)", min_value=1, max_value=12, value=3, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="float-card">', unsafe_allow_html=True)
        sleep_quality = st.slider("😴 3. Sleep Quality Score (1-10)", min_value=1, max_value=10, value=7, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    # Features 4 & 5
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="float-card">', unsafe_allow_html=True)
        task_difficulty = st.slider("🎯 4. Task Difficulty Level (1-10)", min_value=1, max_value=10, value=6, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="float-card">', unsafe_allow_html=True)
        energy_level = st.slider("⚡ 5. Energy Level (1-10)", min_value=1, max_value=10, value=8, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    # Execution Action
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
                    <span style="background: linear-gradient(135deg, #818cf8, #c084fc); padding: 8px 20px; border-radius: 20px; font-weight: 700; font-size: 14px; color: #ffffff;">ANALYSIS COMPLETE</span>
                    <h1 style="color: #ffffff; font-size: 42px; margin-top: 10px;">Predicted Focus Capacity: {focus_capacity}%</h1>
                </div>
                <hr style="border-color: rgba(255,255,255,0.1); margin: 20px 0;">
                <h3 style="color: #c084fc; margin-bottom: 15px;">🤖 FocusBot's AI Action Plan:</h3>
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
