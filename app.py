import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="FocusMate", page_icon="🤖", layout="wide")

# ---------------------------------------------------------
# 1. SCIKIT-LEARN BACKEND
# ---------------------------------------------------------
@st.cache_resource
def train_ml_models():
    np.random.seed(42)
    n_samples = 500

    hours = np.random.randint(1, 12, n_samples)
    sleep = np.random.randint(1, 11, n_samples)
    diff = np.random.randint(1, 11, n_samples)
    energy = np.random.randint(1, 11, n_samples)
    X = np.column_stack((hours, sleep, diff, energy))

    capacity = np.clip((sleep * 5.0) + (energy * 4.0) - (diff * 2.0) - (hours * 1.5) + np.random.normal(0, 3, n_samples), 10, 100)
    sprint = np.clip((capacity * 0.4) - (diff * 1.0) + np.random.normal(0, 2, n_samples), 10, 60)
    rest = np.clip((sprint * 0.25) + (10 - energy) * 0.4, 5, 25)
    
    y = np.column_stack((capacity, sprint, rest))
    model = RandomForestRegressor(n_estimators=50, random_state=42).fit(X, y)
    return model

ml_model = train_ml_models()

# Process query parameters for predictions
params = st.query_params
start_page = params.get("page", "1")
capacity_val, sprint_val, rest_val = 34, 15, 5
mind_dump_text = params.get("dump", "I'm stressed, bored, feeling suffocated")

if "predict" in params:
    try:
        hours = float(params.get("hours", 1))
        sleep = int(params.get("sleep", 5))
        diff = int(params.get("diff", 5))
        energy = int(params.get("energy", 5))

        preds = ml_model.predict(np.array([[hours, sleep, diff, energy]]))[0]
        capacity_val = int(round(preds[0]))
        sprint_val = int(round(preds[1]))
        rest_val = int(round(preds[2]))
        start_page = "2"
    except Exception:
        pass

# ---------------------------------------------------------
# 2. FRONTEND WITH MULTI-PAGE SWITCHING
# ---------------------------------------------------------
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            background-color: #0d0f1d;
            color: #ffffff;
            font-family: system-ui, -apple-system, sans-serif;
            min-height: 100vh;
        }}
        .title-gradient {{
            background: linear-gradient(135deg, #f472b6 0%, #c084fc 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .card-pink {{
            border: 2px solid #f472b6;
            background: rgba(18, 20, 39, 0.8);
            border-radius: 1.25rem;
        }}
        .card-blue {{
            border: 2px solid #38bdf8;
            background: rgba(18, 20, 39, 0.8);
            border-radius: 1.25rem;
        }}
        .card-purple {{
            border: 2px solid #818cf8;
            background: rgba(18, 20, 39, 0.8);
            border-radius: 1.25rem;
        }}
        .card-green {{
            border: 2px solid #34d399;
            background: rgba(18, 20, 39, 0.8);
            border-radius: 1.25rem;
        }}
        .card-main {{
            border: 1px solid rgba(244, 114, 182, 0.3);
            background: rgba(18, 20, 39, 0.9);
            border-radius: 1.5rem;
        }}
        .btn-gradient {{
            background: linear-gradient(90deg, #c084fc 0%, #f472b6 100%);
        }}
        .btn-gradient:hover {{
            opacity: 0.9;
        }}
    </style>
</head>
<body class="p-6 flex flex-col justify-center items-center">

    <div class="max-w-4xl w-full">

        <!-- ================= PAGE 1: WELCOME SCREEN ================= -->
        <div id="page-1" class="{'block' if start_page == '1' else 'hidden'} text-center flex flex-col items-center justify-center py-16 space-y-6">
            <h1 class="text-7xl font-extrabold title-gradient">FocusMate</h1>
            <p class="text-slate-400 text-lg font-medium">Your AI-Powered Deep Work Companion</p>
            
            <div class="relative flex flex-col items-center justify-center my-6">
                <div class="bg-pink-100/90 text-slate-900 font-extrabold px-6 py-2.5 rounded-2xl shadow-lg border border-pink-300 text-lg mb-4">
                    <span>"Hi! Welcome to FocusMate!"</span> ✨
                </div>
                
                <div class="w-28 h-28 relative">
                    <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full drop-shadow-xl">
                        <rect x="42" y="10" width="16" height="6" rx="3" fill="#f472b6" />
                        <circle cx="50" cy="8" r="5" fill="#f472b6" />
                        <rect x="25" y="16" width="50" height="40" rx="12" fill="#a855f7" />
                        <rect x="30" y="21" width="40" height="28" rx="8" fill="#1e1b4b" />
                        <circle cx="40" cy="32" r="4" fill="#38bdf8" />
                        <circle cx="60" cy="32" r="4" fill="#38bdf8" />
                        <rect x="42" y="40" width="16" height="3" rx="1.5" fill="#f472b6" />
                        <circle cx="33" cy="38" r="2.5" fill="#f472b6" opacity="0.6" />
                        <circle cx="67" cy="38" r="2.5" fill="#f472b6" opacity="0.6" />
                        <rect x="35" y="58" width="30" height="26" rx="8" fill="#a855f7" />
                        <circle cx="50" cy="68" r="4" fill="#f472b6" />
                        <rect x="38" y="84" width="8" height="12" rx="4" fill="#6b21a8" />
                        <rect x="54" y="84" width="8" height="12" rx="4" fill="#6b21a8" />
                    </svg>
                </div>
            </div>

            <button onclick="goToPage(2)" class="btn-gradient text-white font-extrabold py-4 px-10 rounded-2xl shadow-xl text-lg hover:scale-105 transition-all">
                Let's Dive In! 🚀
            </button>
        </div>


        <!-- ================= PAGE 2: INPUTS & STRATEGY OUTPUT ================= -->
        <div id="page-2" class="{'block' if start_page == '2' else 'hidden'} space-y-6">
            
            <div class="flex justify-between items-center mb-2">
                <button onclick="goToPage(1)" class="text-xs text-purple-400 hover:text-purple-300 font-semibold flex items-center gap-1">
                    ← Back to Welcome Page
                </button>
                <span class="text-xs text-slate-500 font-bold">PAGE 2 OF 2</span>
            </div>

            <!-- MIND DUMP INPUT -->
            <div class="card-purple p-5">
                <label class="block text-purple-300 font-bold mb-2 text-sm">🧠 1. Mind Dump / Current Feelings</label>
                <input id="input-dump" type="text" value="{mind_dump_text}" placeholder="Describe how you feel or what you need to get done..." class="w-full bg-slate-900/90 border border-slate-700 rounded-xl p-3 text-slate-100 focus:outline-none focus:border-purple-400 text-sm">
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- TARGET STUDY HOURS -->
                <div class="card-pink p-5">
                    <label class="block text-pink-300 font-bold mb-2 text-sm">📚 2. Target Study Hours</label>
                    <input id="input-hours" type="number" value="1" min="0.5" max="12" step="0.5" class="w-full bg-slate-900/90 border border-slate-700 rounded-xl p-3 text-slate-100 focus:outline-none focus:border-pink-400 text-sm">
                </div>

                <!-- SLEEP QUALITY SCORE -->
                <div class="card-blue p-5">
                    <div class="flex justify-between text-sky-300 font-bold mb-2 text-sm">
                        <span>😴 3. Sleep Quality Score (1–10)</span>
                        <span id="lbl-sleep">5</span>
                    </div>
                    <input id="input-sleep" type="range" min="1" max="10" value="5" oninput="document.getElementById('lbl-sleep').innerText=this.value" class="w-full accent-sky-400 mt-2">
                </div>

                <!-- TASK DIFFICULTY -->
                <div class="card-purple p-5">
                    <div class="flex justify-between text-indigo-300 font-bold mb-2 text-sm">
                        <span>🎯 4. Task Difficulty (1–10)</span>
                        <span id="lbl-diff">5</span>
                    </div>
                    <input id="input-diff" type="range" min="1" max="10" value="5" oninput="document.getElementById('lbl-diff').innerText=this.value" class="w-full accent-indigo-400 mt-2">
                </div>

                <!-- CURRENT ENERGY LEVEL -->
                <div class="card-green p-5">
                    <div class="flex justify-between text-emerald-300 font-bold mb-2 text-sm">
                        <span>⚡ 5. Current Energy Level (1–10)</span>
                        <span id="lbl-energy">5</span>
                    </div>
                    <input id="input-energy" type="range" min="1" max="10" value="5" oninput="document.getElementById('lbl-energy').innerText=this.value" class="w-full accent-emerald-400 mt-2">
                </div>
            </div>

            <!-- GENERATE BUTTON -->
            <button onclick="submitToML()" class="w-full btn-gradient text-white font-extrabold text-lg py-4 rounded-2xl shadow-xl transition-all my-2">
                ✨ Generate Focus Strategy ✨
            </button>

            <!-- OUTPUT STRATEGY CARD -->
            <div id="strategy-card" class="card-main p-8 space-y-6 {'block' if 'predict' in params else 'hidden'}">
                <h3 class="text-2xl font-extrabold text-pink-300 flex items-center justify-center gap-2">
                    <span>🫐</span> Your Custom Focus Strategy
                </h3>

                <div class="grid grid-cols-3 gap-4 text-center">
                    <div class="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
                        <span class="block text-slate-400 text-xs font-semibold mb-1">Focus Capacity</span>
                        <span class="text-4xl font-extrabold text-purple-300">{capacity_val}%</span>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
                        <span class="block text-slate-400 text-xs font-semibold mb-1">Sprint Duration</span>
                        <span class="text-4xl font-extrabold text-pink-400">{sprint_val} min</span>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
                        <span class="block text-slate-400 text-xs font-semibold mb-1">Rest Interval</span>
                        <span class="text-4xl font-extrabold text-sky-400">{rest_val} min</span>
                    </div>
                </div>

                <div class="bg-slate-900/60 p-4 rounded-xl border-l-4 border-purple-400">
                    <h4 class="font-bold text-purple-300 text-sm mb-1 flex items-center gap-2">
                        <span>🧠</span> Mind Dump Analysis
                    </h4>
                    <p class="text-slate-300 text-xs">"{mind_dump_text}" → Clear priority extracted and queued.</p>
                </div>

                <div class="bg-slate-900/60 p-4 rounded-xl border-l-4 border-emerald-400">
                    <h4 class="font-bold text-emerald-300 text-sm mb-1 flex items-center gap-2">
                        <span>🚀</span> Recommended Roadmap
                    </h4>
                    <p class="text-slate-300 text-xs">Start with low-friction tasks for 10 mins to build momentum.</p>
                </div>
            </div>

        </div>

    </div>

    <script>
        function goToPage(pageNum) {{
            if (pageNum === 2) {{
                document.getElementById('page-1').classList.add('hidden');
                document.getElementById('page-1').classList.remove('block');
                document.getElementById('page-2').classList.remove('hidden');
                document.getElementById('page-2').classList.add('block');
            }} else {{
                document.getElementById('page-2').classList.add('hidden');
                document.getElementById('page-2').classList.remove('block');
                document.getElementById('page-1').classList.remove('hidden');
                document.getElementById('page-1').classList.add('block');
            }}
        }}

        function submitToML() {{
            const hours = document.getElementById('input-hours').value;
            const sleep = document.getElementById('input-sleep').value;
            const diff = document.getElementById('input-diff').value;
            const energy = document.getElementById('input-energy').value;
            const dump = encodeURIComponent(document.getElementById('input-dump').value || "I'm stressed, bored, feeling suffocated");

            const query = `?predict=true&page=2&hours=${{hours}}&sleep=${{sleep}}&diff=${{diff}}&energy=${{energy}}&dump=${{dump}}`;
            window.parent.location.href = query;
        }}
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
