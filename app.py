import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="FocusMate", page_icon="🔮", layout="wide")

# Hide standard Streamlit chrome to retain custom UI presentation
st.markdown("""
    <style>
        .block-container { padding: 0 !important; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        iframe { width: 100% !important; height: 100vh !important; border: none; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. TEACHER'S ML MODEL SETUP (Backend Engine)
# ---------------------------------------------------------
@st.cache_resource
def train_focus_model():
    # Synthetic training data representing user state inputs
    # Features: [mood_code, sleep_score, energy_level, task_difficulty]
    # Mood codes: 0: Stressed, 1: Tired, 2: Distracted, 3: Happy
    X_train = np.array([
        [0, 3, 3, 8], [0, 4, 2, 9], [1, 2, 4, 7], [1, 5, 3, 6],
        [2, 6, 5, 8], [2, 7, 6, 5], [3, 8, 9, 4], [3, 9, 8, 3],
        [0, 6, 7, 5], [1, 8, 4, 6], [2, 4, 8, 7], [3, 7, 7, 8]
    ])
    # Targets: [Capacity %, Sprint Minutes, Rest Minutes]
    y_train = np.array([
        [35, 15, 5],  [30, 15, 5],  [40, 20, 5],  [50, 25, 5],
        [60, 25, 5],  [70, 30, 5],  [95, 45, 10], [90, 45, 10],
        [65, 30, 5],  [55, 25, 5],  [60, 25, 5],  [85, 40, 10]
    ])
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

ml_model = train_focus_model()

# ---------------------------------------------------------
# 2. STREAMLIT SIDEBAR CONTROLS (ML Inputs)
# ---------------------------------------------------------
st.sidebar.title("🤖 ML Model Parameters")
st.sidebar.markdown("Configure the inputs required for the teacher's Machine Learning model:")

mood = st.sidebar.selectbox("Current Mood", ["Stressed / Anxious", "Tired / Low Energy", "Distracted / Restless", "Happy / Motivated"])
sleep = st.sidebar.slider("Sleep Quality (1-10)", 1, 10, 7)
energy = st.sidebar.slider("Energy Level (1-10)", 1, 10, 8)
difficulty = st.sidebar.slider("Task Difficulty (1-10)", 1, 10, 6)
task_name = st.sidebar.text_input("Task Goal", "Build UI Layout")

# Map inputs to ML format
mood_map = {"Stressed / Anxious": 0, "Tired / Low Energy": 1, "Distracted / Restless": 2, "Happy / Motivated": 3}
input_features = np.array([[mood_map[mood], sleep, energy, difficulty]])

# Generate ML Prediction
prediction = ml_model.predict(input_features)[0]
predicted_capacity = int(prediction[0])
predicted_sprint = int(prediction[1])
predicted_rest = int(prediction[2])

# ---------------------------------------------------------
# 3. FRONTEND APP WITH INTEGRATED ML PREDICTIONS
# ---------------------------------------------------------
app_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #0f111a; color: #f8fafc; overflow-x: hidden; min-height: 100vh; margin: 0; }}
        .glass-card {{ background: rgba(22, 24, 38, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(192, 132, 252, 0.2); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4); }}
        .glow-title {{ background: linear-gradient(135deg, #e9d5ff 0%, #c084fc 50%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        canvas {{ pointer-events: none; }}
    </style>
</head>
<body class="relative flex flex-col justify-between items-center min-h-screen p-6">

    <canvas id="stage" class="fixed inset-0 w-full h-full z-20"></canvas>

    <!-- WELCOME SCREEN -->
    <div id="welcome-screen" class="relative z-10 flex flex-col items-center justify-center min-h-screen text-center w-full max-w-2xl mx-auto py-8">
        <h1 class="text-6xl font-extrabold tracking-tight glow-title mb-2">FocusMate</h1>
        <p class="text-slate-400 text-lg mb-10">Your AI-Powered Deep Work Companion</p>
        <div id="speech-bubble" class="opacity-0 translate-y-4 bg-gradient-to-r from-purple-200 to-pink-200 text-slate-900 font-bold text-xl px-10 py-4 rounded-2xl shadow-lg relative mb-12">
            "Hi! Welcome to FocusMate!" ✨
        </div>
        <button id="dive-btn" onclick="startFlightSequence()" class="opacity-0 translate-y-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold text-xl px-10 py-4 rounded-2xl shadow-xl transition-all duration-300 transform hover:scale-105 active:scale-95 cursor-pointer mt-24">
            Let's Dive In! 🚀
        </button>
    </div>

    <!-- WORKSPACE SCREEN -->
    <div id="workspace-screen" class="hidden relative z-10 w-full max-w-4xl mx-auto py-12">
        <div class="glass-card rounded-3xl p-6 mb-8 text-center relative">
            <h2 class="text-3xl font-bold glow-title mb-2">Interactive Mission Center</h2>
            <p class="text-pink-200 font-semibold text-lg">"RandomForest ML Model outputs loaded."</p>
        </div>

        <div class="glass-card rounded-3xl p-8 border border-purple-500/30">
            <h3 class="text-2xl font-bold glow-title mb-4 text-center">🎯 ML Strategy & Action Plan</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 text-center">
                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                    <span class="block text-slate-400 text-sm">Predicted Focus Capacity</span>
                    <span class="text-3xl font-extrabold text-purple-400">{predicted_capacity}%</span>
                </div>
                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                    <span class="block text-slate-400 text-sm">ML Recommended Sprint</span>
                    <span class="text-3xl font-extrabold text-pink-400">{predicted_sprint} min</span>
                </div>
                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                    <span class="block text-slate-400 text-sm">Optimal Rest Interval</span>
                    <span class="text-3xl font-extrabold text-sky-400">{predicted_rest} min</span>
                </div>
            </div>

            <div class="bg-slate-900/80 p-5 rounded-xl border-l-4 border-indigo-400 mb-4">
                <h4 class="font-bold text-indigo-300 text-lg mb-2">📋 Task Roadmap</h4>
                <ol class="list-decimal list-inside space-y-2 text-slate-300 text-sm font-medium">
                    <li>Set up environment for: <strong>{task_name}</strong>.</li>
                    <li>Execute target effort for {predicted_sprint} minutes.</li>
                    <li>Take a mandatory {predicted_rest}-minute rest break.</li>
                </ol>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('stage');
        const ctx = canvas.getContext('2d');
        function resizeCanvas() {{ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }}
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const robot = {{ x: window.innerWidth / 2, y: -150 }};
        function drawRobot(x, y) {{
            ctx.save(); ctx.translate(x, y);
            ctx.fillStyle = '#c084fc'; ctx.beginPath(); ctx.roundRect(-45, -42, 90, 64, 20); ctx.fill();
            ctx.fillStyle = '#1e1b2e'; ctx.beginPath(); ctx.roundRect(-35, -32, 70, 44, 12); ctx.fill();
            ctx.fillStyle = '#38bdf8'; ctx.beginPath(); ctx.arc(-16, -10, 7, 0, Math.PI * 2); ctx.arc(16, -10, 7, 0, Math.PI * 2); ctx.fill();
            ctx.restore();
        }}

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawRobot(robot.x, robot.y);
            requestAnimationFrame(animate);
        }}
        animate();

        window.addEventListener('DOMContentLoaded', () => {{
            gsap.to(robot, {{ y: window.innerHeight / 2 - 20, duration: 1.8, ease: "back.out(1.4)", onComplete: () => {{
                gsap.to('#speech-bubble', {{ opacity: 1, y: 0, duration: 0.6 }});
                gsap.to('#dive-btn', {{ opacity: 1, y: 0, duration: 0.6, delay: 0.2 }});
            }} }});
        }});

        function startFlightSequence() {{
            gsap.to('#welcome-screen', {{ opacity: 0, duration: 0.4 }});
            gsap.to(robot, {{ y: -300, duration: 1.2, ease: "power2.in", onComplete: () => {{
                document.getElementById('welcome-screen').classList.add('hidden');
                document.getElementById('workspace-screen').classList.remove('hidden');
                const rect = document.querySelector('#workspace-screen .glass-card').getBoundingClientRect();
                robot.x = rect.right - 40;
                gsap.to(robot, {{ y: rect.top + 30, duration: 1, ease: "bounce.out" }});
            }} }});
        }}
    </script>
</body>
</html>
"""

components.html(app_code, height=1000, scrolling=True)
