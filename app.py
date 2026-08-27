import streamlit as st
import streamlit.components.v1 as components
import time

# ------------------------------------------------------------------------------
# 1. PAGE CONFIG & HIGH-CONTRAST DARK THEME
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Focusmate AI", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    /* Dark Cosmic Background */
    .stApp {
        background: #0f172a;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #f8fafc;
    }

    /* Container Box */
    .robot-container {
        background: #1e293b;
        border-radius: 24px;
        padding: 20px;
        text-align: center;
        border: 1px solid #334155;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }

    /* Speech Bubble */
    .speech-bubble {
        background: #f8fafc;
        border-radius: 16px;
        padding: 16px 24px;
        color: #0f172a !important;
        font-size: 18px;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
    }

    /* Card Panels */
    .float-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* FORCE ALL STREAMLIT LABELS TO WHITE */
    .stApp label, .stApp p, .stApp div {
        color: #f8fafc !important;
    }

    /* Inputs Styling */
    .stTextArea textarea {
        background: #0f172a !important;
        border: 1px solid #475569 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }

    /* Action Button */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 16px 32px !important;
        width: 100%;
    }

    .solution-panel {
        background: #1e293b;
        border: 2px solid #a855f7;
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# ------------------------------------------------------------------------------
# 2. PROPER 3D ROBOT MASCOT (FORCED CACHE PURGE)
# ------------------------------------------------------------------------------
def render_mascot(height=280, key="robot_v2"):
    threejs_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body {{ margin: 0; overflow: hidden; background: transparent; }}
            canvas {{ width: 100%; height: 100%; display: block; }}
        </style>
    </head>
    <body>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / {height}, 0.1, 1000);
        camera.position.z = 6.5;

        const renderer = new THREE.WebGLRenderer({{ alpha: true, antialias: true }});
        renderer.setSize(window.innerWidth, {height});
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xa855f7, 1.8);
        dirLight.position.set(5, 5, 5);
        scene.add(dirLight);

        const pointLight = new THREE.PointLight(0x38bdf8, 1.5, 10);
        pointLight.position.set(-3, -2, 2);
        scene.add(pointLight);

        const robotGroup = new THREE.Group();

        // Materials
        const bodyMat = new THREE.MeshStandardMaterial({{ color: 0x818cf8, roughness: 0.2, metalness: 0.3 }});
        const metalMat = new THREE.MeshStandardMaterial({{ color: 0x94a3b8, roughness: 0.3, metalness: 0.8 }});
        const screenMat = new THREE.MeshBasicMaterial({{ color: 0x0f172a }});
        const eyeMat = new THREE.MeshBasicMaterial({{ color: 0x38bdf8 }});
        const earMat = new THREE.MeshStandardMaterial({{ color: 0xc084fc }});

        // 1. Robot Head Box
        const headGeo = new THREE.BoxGeometry(1.6, 1.1, 1.1);
        const head = new THREE.Mesh(headGeo, bodyMat);
        head.position.y = 0.6;
        robotGroup.add(head);

        // 2. Visor Screen
        const screenGeo = new THREE.PlaneGeometry(1.3, 0.8);
        const screen = new THREE.Mesh(screenGeo, screenMat);
        screen.position.set(0, 0.6, 0.56);
        robotGroup.add(screen);

        // 3. Glowing Eyes
        const eyeGeo = new THREE.CircleGeometry(0.14, 32);
        const eyeLeft = new THREE.Mesh(eyeGeo, eyeMat);
        eyeLeft.position.set(-0.35, 0.62, 0.57);
        robotGroup.add(eyeLeft);

        const eyeRight = new THREE.Mesh(eyeGeo, eyeMat);
        eyeRight.position.set(0.35, 0.62, 0.57);
        robotGroup.add(eyeRight);

        // 4. Antenna
        const antennaStemGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.4, 16);
        const antennaStem = new THREE.Mesh(antennaStemGeo, metalMat);
        antennaStem.position.set(0, 1.35, 0);
        robotGroup.add(antennaStem);

        const antennaOrbGeo = new THREE.SphereGeometry(0.12, 16, 16);
        const antennaOrbMat = new THREE.MeshBasicMaterial({{ color: 0xc084fc }});
        const antennaOrb = new THREE.Mesh(antennaOrbGeo, antennaOrbMat);
        antennaOrb.position.set(0, 1.6, 0);
        robotGroup.add(antennaOrb);

        // 5. Floating Ears
        const earGeo = new THREE.CylinderGeometry(0.2, 0.2, 0.15, 16);
        const earLeft = new THREE.Mesh(earGeo, earMat);
        earLeft.rotation.z = Math.PI / 2;
        earLeft.position.set(-0.88, 0.6, 0);
        robotGroup.add(earLeft);

        const earRight = earLeft.clone();
        earRight.position.set(0.88, 0.6, 0);
        robotGroup.add(earRight);

        // 6. Torso
        const torsoGeo = new THREE.CylinderGeometry(0.5, 0.6, 0.9, 32);
        const torso = new THREE.Mesh(torsoGeo, bodyMat);
        torso.position.y = -0.5;
        robotGroup.add(torso);

        // 7. Chest Core
        const coreGeo = new THREE.CircleGeometry(0.16, 32);
        const coreMat = new THREE.MeshBasicMaterial({{ color: 0xc084fc }});
        const core = new THREE.Mesh(coreGeo, coreMat);
        core.position.set(0, -0.4, 0.51);
        robotGroup.add(core);

        scene.add(robotGroup);

        let clock = new THREE.Clock();
        
        function animate() {{
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();

            robotGroup.position.y = Math.sin(t * 2) * 0.15;
            robotGroup.rotation.y = Math.sin(t * 1.2) * 0.12;

            if (Math.sin(t * 3.5) > 0.96) {{
                eyeLeft.scale.y = 0.1;
                eyeRight.scale.y = 0.1;
            }} else {{
                eyeLeft.scale.y = 1;
                eyeRight.scale.y = 1;
            }}

            renderer.render(scene, camera);
        }}
        animate();
    </script>
    </body>
    </html>
    """
    components.html(threejs_code, height=height, key=key)

# ------------------------------------------------------------------------------
# PAGE 1: WELCOME SCREEN
# ------------------------------------------------------------------------------
if st.session_state.page == 'welcome':
    st.write("")
    st.write("")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown('<div class="robot-container">', unsafe_allow_html=True)
        render_mascot(300, key="welcome_robot")
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
    render_mascot(220, key="workspace_robot")
    st.markdown("""
        <div class="speech-bubble">
            "Configure your 5 session parameters below, and I'll generate a custom study solution for you." 🧠
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #c084fc; font-weight: 700; margin-bottom: 20px;'>🛸 Mission Inputs</h3>", unsafe_allow_html=True)

    st.markdown('<div class="float-card">', unsafe_allow_html=True)
    user_thoughts = st.text_area(
        "💬 1. Mind Dump (Venting, doubts, or thoughts occupying your brain):",
        placeholder="e.g., I have an exam tomorrow, my mind is spiraling with doubts, and I can't seem to start...",
        height=90
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
                    <span style="background: #818cf8; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 14px; color: #ffffff;">ANALYSIS COMPLETE</span>
                    <h1 style="color: #ffffff; font-size: 36px; margin-top: 10px;">Predicted Focus Capacity: {focus_capacity}%</h1>
                </div>
                <hr style="border-color: #334155; margin: 20px 0;">
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
