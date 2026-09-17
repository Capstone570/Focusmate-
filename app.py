import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Config & Streamlit margin reset
st.set_page_config(page_title="FocusMate", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { visibility: hidden; }
        iframe { width: 100vw !important; height: 100vh !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# Machine Learning Setup
@st.cache_resource
def train_ml_models():
    np.random.seed(42)
    X = np.column_stack((
        np.random.randint(1, 12, 500),
        np.random.randint(1, 11, 500),
        np.random.randint(1, 11, 500),
        np.random.randint(1, 11, 500)
    ))
    capacity = np.clip((X[:, 1] * 5.0) + (X[:, 3] * 4.0) - (X[:, 2] * 2.0) - (X[:, 0] * 1.5), 10, 100)
    sprint = np.clip((capacity * 0.4) - (X[:, 2] * 1.0), 10, 60)
    rest = np.clip((sprint * 0.25) + (10 - X[:, 3]) * 0.4, 5, 25)
    return RandomForestRegressor(n_estimators=50, random_state=42).fit(X, np.column_stack((capacity, sprint, rest)))

ml_model = train_ml_models()

params = st.query_params
start_page = params.get("page", "1")
capacity_val, sprint_val, rest_val = 34, 15, 5
mind_dump_text = params.get("dump", "I'm stressed, bored, feeling suffocated")

if "predict" in params:
    try:
        preds = ml_model.predict(np.array([[
            float(params.get("hours", 1)),
            int(params.get("sleep", 5)),
            int(params.get("diff", 5)),
            int(params.get("energy", 5))
        ]]))[0]
        capacity_val, sprint_val, rest_val = int(round(preds[0])), int(round(preds[1])), int(round(preds[2]))
        start_page = "2"
    except Exception:
        pass

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            background-color: #0d0f1d;
            color: #ffffff;
            font-family: system-ui, -apple-system, sans-serif;
            overflow-x: hidden;
        }}
        .title-gradient {{
            background: linear-gradient(135deg, #f472b6 0%, #c084fc 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .card-pink {{ border: 2px solid #f472b6; background: rgba(18, 20, 39, 0.85); border-radius: 1.25rem; }}
        .card-blue {{ border: 2px solid #38bdf8; background: rgba(18, 20, 39, 0.85); border-radius: 1.25rem; }}
        .card-purple {{ border: 2px solid #818cf8; background: rgba(18, 20, 39, 0.85); border-radius: 1.25rem; }}
        .card-green {{ border: 2px solid #34d399; background: rgba(18, 20, 39, 0.85); border-radius: 1.25rem; }}
        .card-main {{ border: 1px solid rgba(244, 114, 182, 0.3); background: rgba(18, 20, 39, 0.95); border-radius: 1.5rem; }}
        .btn-gradient {{ background: linear-gradient(90deg, #c084fc 0%, #f472b6 100%); }}

        /* BOBBING / FLOATING ROBOT ANIMATION */
        @keyframes floatAnim {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        .robot-float {{
            animation: floatAnim 3s ease-in-out infinite;
        }}

        /* PURPLE & PINK GAS/SMOKE PARTICLES */
        .gas-cloud {{
            position: fixed;
            border-radius: 50%;
            pointer-events: none;
            animation: smokeBurst 1.2s ease-out forwards;
            z-index: 99;
        }}
        @keyframes smokeBurst {{
            0% {{ opacity: 0.9; transform: translate(0, 0) scale(0.3); filter: blur(4px); }}
            50% {{ opacity: 0.7; filter: blur(10px); }}
            100% {{ opacity: 0; transform: translate(var(--dx), var(--dy)) scale(4); filter: blur(20px); }}
        }}
    </style>
</head>
<body class="flex justify-center items-center">

    <div class="w-full max-w-3xl px-6 py-6">

        <!-- PAGE 1: WELCOME SCREEN -->
        <div id="page-1" class="{'flex' if start_page == '1' else 'hidden'} flex-col items-center justify-center space-y-8 min-h-[90vh]">
            
            <div class="text-center space-y-2">
                <h1 class="text-6xl font-black title-gradient">FocusMate</h1>
                <p class="text-slate-400 text-sm font-semibold tracking-wide">Your AI-Powered Deep Work Companion</p>
            </div>
            
            <!-- SPEECH BUBBLE & ROBOT (STRICT VERTICAL STACKING) -->
            <div class="flex flex-col items-center space-y-4 my-2">
                <div class="bg-pink-100 text-slate-900 font-extrabold px-6 py-2 rounded-2xl shadow-md border border-pink-300 text-base">
                    "Hi! Welcome to FocusMate!" ✨
                </div>
                
                <div class="w-24 h-24 robot-float" id="robot-avatar">
                    <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full drop-shadow-[0_8px_16px_rgba(192,132,252,0.4)]">
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

            <button onclick="triggerGasAndDive()" class="btn-gradient text-white font-extrabold py-3.5 px-10 rounded-2xl shadow-xl hover:scale-105 transition-transform text-base">
                Let's Dive In! 🚀
            </button>
        </div>

        <!-- PAGE 2: INPUTS & OUTPUTS -->
        <div id="page-2" class="{'block' if start_page == '2' else 'hidden'} space-y-5">
            <div class="flex justify-between items-center">
                <button onclick="goToPage(1)" class="text-xs text-purple-400 font-semibold hover:underline">
                    ← Back to Home
                </button>
                <span class="text-xs text-slate-500 font-bold">PAGE 2 OF 2</span>
            </div>

            <div class="card-purple p-4">
                <label class="block text-purple-300 font-bold mb-2 text-xs">🧠 1. Mind Dump / Current Feelings</label>
                <input id="input-dump" type="text" value="{mind_dump_text}" class="w-full bg-slate-900/90 border border-slate-700 rounded-xl p-2.5 text-slate-100 text-xs focus:outline-none focus:border-purple-400">
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="card-pink p-4">
                    <label class="block text-pink-300 font-bold mb-2 text-xs">📚 2. Target Study Hours</label>
                    <input id="input-hours" type="number" value="1" min="0.5" max="12" step="0.5" class="w-full bg-slate-900/90 border border-slate-700 rounded-xl p-2.5 text-slate-100 text-xs focus:outline-none focus:border-pink-400">
                </div>

                <div class="card-blue p-4">
                    <div class="flex justify-between text-sky-300 font-bold mb-1 text-xs">
                        <span>😴 3. Sleep Quality Score (1–10)</span>
                        <span id="lbl-sleep">5</span>
                    </div>
                    <input id="input-sleep" type="range" min="1" max="10" value="5" oninput="document.getElementById('lbl-sleep').innerText=this.value" class="w-full accent-sky-400">
                </div>

                <div class="card-purple p-4">
                    <div class="flex justify-between text-indigo-300 font-bold mb-1 text-xs">
                        <span>🎯 4. Task Difficulty (1–10)</span>
                        <span id="lbl-diff">5</span>
                    </div>
                    <input id="input-diff" type="range" min="1" max="10" value="5" oninput="document.getElementById('lbl-diff').innerText=this.value" class="w-full accent-indigo-400">
                </div>

                <div class="card-green p-4">
                    <div class="flex justify-between text-emerald-300 font-bold mb-1 text-xs">
                        <span>⚡ 5. Current Energy Level (1–10)</span>
                        <span id="lbl-energy">5</span>
                    </div>
                    <input id="input-energy" type="range" min="1" max="10" value="5" oninput="document.getElementById('lbl-energy').innerText=this.value" class="w-full accent-emerald-400">
                </div>
            </div>

            <button onclick="submitToML()" class="w-full btn-gradient text-white font-extrabold text-base py-3.5 rounded-2xl shadow-lg transition-transform hover:opacity-95">
                ✨ Generate Focus Strategy ✨
            </button>

            <div id="strategy-card" class="card-main p-6 space-y-4 {'block' if 'predict' in params else 'hidden'}">
                <h3 class="text-xl font-extrabold text-pink-300 text-center">🫐 Your Custom Focus Strategy</h3>

                <div class="grid grid-cols-3 gap-3 text-center">
                    <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                        <span class="block text-slate-400 text-[10px] font-semibold">Focus Capacity</span>
                        <span class="text-2xl font-black text-purple-300">{capacity_val}%</span>
                    </div>
                    <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                        <span class="block text-slate-400 text-[10px] font-semibold">Sprint Duration</span>
                        <span class="text-2xl font-black text-pink-400">{sprint_val} min</span>
                    </div>
                    <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                        <span class="block text-slate-400 text-[10px] font-semibold">Rest Interval</span>
                        <span class="text-2xl font-black text-sky-400">{rest_val} min</span>
                    </div>
                </div>

                <div class="bg-slate-900/60 p-3 rounded-lg border-l-4 border-purple-400">
                    <h4 class="font-bold text-purple-300 text-xs mb-0.5">🧠 Mind Dump Analysis</h4>
                    <p class="text-slate-300 text-[11px]">"{mind_dump_text}" → Prioritized and mapped.</p>
                </div>

                <div class="bg-slate-900/60 p-3 rounded-lg border-l-4 border-emerald-400">
                    <h4 class="font-bold text-emerald-300 text-xs mb-0.5">🚀 Recommended Roadmap</h4>
                    <p class="text-slate-300 text-[11px]">Start with low-friction tasks for 10 mins to build momentum.</p>
                </div>
            </div>
        </div>

    </div>

    <script>
        function triggerGasAndDive() {{
            const robot = document.getElementById('robot-avatar');
            const rect = robot.getBoundingClientRect();
            const colors = ['#f472b6', '#c084fc', '#e879f9', '#38bdf8'];

            // Burst 40 smoke/gas clouds from the bottom of the robot
            for (let i = 0; i < 40; i++) {{
                const gas = document.createElement('div');
                gas.className = 'gas-cloud';
                const size = Math.random() * 30 + 15;
                gas.style.width = size + 'px';
                gas.style.height = size + 'px';
                gas.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                
                gas.style.left = (rect.left + rect.width / 2 - size / 2) + 'px';
                gas.style.top = (rect.bottom - 10) + 'px';

                const dx = (Math.random() - 0.5) * 350;
                const dy = Math.random() * 200 + 50;
                gas.style.setProperty('--dx', dx + 'px');
                gas.style.setProperty('--dy', dy + 'px');

                document.body.appendChild(gas);
                setTimeout(() => gas.remove(), 1200);
            }}

            setTimeout(() => {{
                goToPage(2);
            }}, 500);
        }}

        function goToPage(p) {{
            const p1 = document.getElementById('page-1');
            const p2 = document.getElementById('page-2');
            if (p === 2) {{
                p1.classList.replace('flex', 'hidden');
                p2.classList.replace('hidden', 'block');
            }} else {{
                p2.classList.replace('block', 'hidden');
                p1.classList.replace('hidden', 'flex');
            }}
        }}

        function submitToML() {{
            const h = document.getElementById('input-hours').value;
            const s = document.getElementById('input-sleep').value;
            const d = document.getElementById('input-diff').value;
            const e = document.getElementById('input-energy').value;
            const txt = encodeURIComponent(document.getElementById('input-dump').value || "I'm stressed, bored");

            window.parent.location.href = `?predict=true&page=2&hours=${{h}}&sleep=${{s}}&diff=${{d}}&energy=${{e}}&dump=${{txt}}`;
        }}
    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
