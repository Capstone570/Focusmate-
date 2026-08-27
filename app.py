import streamlit as st
import streamlit.components.v1 as components
import time

# ------------------------------------------------------------------------------
# 1. PAGE CONFIG & COSMIC THEME
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Focusmate AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #ffffff;
    }

    .robot-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 30px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        margin-bottom: 20px;
    }

    .speech-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 14px 28px;
        font-size: 19px;
        font-weight: 700;
        color: #090a0f;
        display: inline-block;
        margin-top: 10px;
        box-shadow: 0 0 25px rgba(162, 210, 255, 0.5);
    }

    .float-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    .solution-card {
        background: rgba(255, 255, 255, 0.95);
        color: #090a0f;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(162, 210, 255, 0.4);
        margin-top: 20px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #a2d2ff 0%, #ffc8dd 100%) !important;
        color: #090a0f !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 14px 30px !important;
        width: 100%;
        box-shadow: 0 4px 20px rgba(162, 210, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. INTERACTIVE 3D MASCOT GUIDING VIEWPORT
# ------------------------------------------------------------------------------
threejs_robot_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body { margin: 0; overflow: hidden; background: transparent; }
        canvas { width: 100%; height: 100%; display: block; }
    </style>
</head>
</body>
<script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 260, 0.1, 1000);
    camera.position.z = 7;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, 260);
    renderer.shadowMap.enabled = true;
    document.body.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xa2d2ff, 1.2);
    dirLight.position.set(5, 5, 5);
    scene.add(dirLight);

    const robotGroup = new THREE.Group();

    // Head
    const headGeo = new THREE.BoxGeometry(1.6, 1.2, 1.1);
    const headMat = new THREE.MeshStandardMaterial({ color: 0xe0f2fe, roughness: 0.2 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 0.8;
    robotGroup.add(head);

    // Screen
    const faceGeo = new THREE.PlaneGeometry(1.3, 0.9);
    const faceMat = new THREE.MeshBasicMaterial({ color: 0x0f172a });
    const face = new THREE.Mesh(faceGeo, faceMat);
    face.position.set(0, 0.8, 0.56);
    robotGroup.add(face);

    // Blinking Eyes
    const eyeGeo = new THREE.CircleGeometry(0.18, 32);
    const eyeMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
    const eyeLeft = new THREE.Mesh(eyeGeo, eyeMat);
    eyeLeft.position.set(-0.35, 0.85, 0.57);
    robotGroup.add(eyeLeft);

    const eyeRight = new THREE.Mesh(eyeGeo, eyeMat);
    eyeRight.position.set(0.35, 0.85, 0.57);
    robotGroup.add(eyeRight);

    // Body
    const bodyGeo = new THREE.CylinderGeometry(0.6, 0.7, 1.2, 32);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xbae6fd, roughness: 0.3 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = -0.4;
    robotGroup.add(body);

    scene.add(robotGroup);

    let clock = new THREE.Clock();
    
    function animate() {
        requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        robotGroup.position.y = Math.sin(elapsedTime * 2) * 0.25;
        robotGroup.rotation.y = Math.sin(elapsedTime * 1) * 0.15;

        if (Math.sin(elapsedTime * 4) > 0.98) {
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
</html>
"""

st.markdown('<div class="robot-container">', unsafe_allow_html=True)
components.html(threejs_robot_code, height=270)
st.markdown("""
    <div class="speech-box">
        "Welcome! Dump your thoughts below. I'll analyze your focus state & give you a solution! 🧠✨"
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. AI INPUT SECTION
# ------------------------------------------------------------------------------
st.markdown("<h3 style='text-align: center; color: #a2d2ff;'>🧠 Mind & Study Context</h3>", unsafe_allow_html=True)

# Overthinker Free-Text Box
st.markdown('<div class="float-card">', unsafe_allow_html=True)
user_thoughts = st.text_area(
    "💬 What's on your mind right now? (Overthinking, stress, task doubts, or thoughts):",
    placeholder="e.g., I have an exam tomorrow, my mind is spiraling with doubts, and I can't start studying...",
    height=100
)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="float-card">', unsafe_allow_html=True)
    study_hours = st.number_input("📚 Target Study Time (Whole Hours)", min_value=1, max_value=12, value=3, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="float-card">', unsafe_allow_html=True)
    sleep_quality = st.slider("😴 Sleep Quality (1-10 Scale)", min_value=1, max_value=10, value=7, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="float-card">', unsafe_allow_html=True)
    task_difficulty = st.slider("🎯 Subject Difficulty (1-10 Scale)", min_value=1, max_value=10, value=6, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. AI PREDICTION & SOLUTION ENGINE
# ------------------------------------------------------------------------------
st.write("")
if st.button("✨ Analyze Mind State & Predict Focus ✨"):
    if not user_thoughts.strip():
        st.warning("Please type a quick sentence about what's on your mind first!")
    else:
        with st.spinner("FocusBot is running cognitive analysis..."):
            time.sleep(1.2)

        # AI Heuristics Engine
        overthink_keywords = ["stress", "anxious", "exam", "fail", "scared", "can't", "overwhelmed", "spiraling", "doubt"]
        stress_count = sum(1 for word in overthink_keywords if word in user_thoughts.lower())

        # Prediction Math
        base_focus = (sleep_quality * 6) + ((11 - task_difficulty) * 4) - (stress_count * 12)
        predicted_focus = int(min(max(base_focus + 25, 15), 98))

        st.balloons()

        # Dynamic Solution Logic
        st.markdown(f"""
        <div class="solution-card">
            <h2 style="color: #1e3a8a; margin: 0; text-align: center;">🎉 Predicted Focus Capacity: {predicted_focus}%</h2>
            <hr style="border-color: #cbd5e1; margin: 15px 0;">
            <h3 style="color: #0f172a; margin-bottom: 10px;">🤖 FocusBot's Personalized AI Action Plan:</h3>
        """, unsafe_allow_html=True)

        if stress_count > 0 or predicted_focus < 60:
            st.markdown("""
            <ul>
                <li><b>Step 1 (Clear Brain Fog):</b> Spend 2 minutes doing a quick 'Brain Dump'—write down the 3 main things terrifying you right now on a scrap paper, then set it aside.</li>
                <li><b>Step 2 (Micro-Session):</b> Don't commit to all hours. Set a timer for just <b>10 minutes</b> on one single sub-topic. Starting is the antidote to overthinking.</li>
                <li><b>Step 3 (Reduce Complexity):</b> Break your study material down into bullet points instead of reading dense textbook pages directly.</li>
            </ul>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <ul>
                <li><b>Step 1 (Zone In):</b> Your mind is clear! Open your primary study material and close all unrelated browser tabs immediately.</li>
                <li><b>Step 2 (Pomodoro Block):</b> Work in focused <b>25-minute sprints</b> followed by 5-minute active stretch breaks.</li>
                <li><b>Step 3 (Active Recall):</b> Test yourself after every topic rather than passively re-reading notes.</li>
            </ul>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
