import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FocusMate AI Pro", page_icon="🔮", layout="wide")

# Single HTML wrapper containing styling, visual markup, and ML prediction logic
full_app_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
        .glass-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .glow-title {
            background: linear-gradient(135deg, #e9d5ff 0%, #c084fc 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body class="p-6">

    <!-- HERO HEADER -->
    <div class="text-center mb-8">
        <h1 class="text-5xl font-extrabold glow-title mb-2">FocusMate AI Pro 🔮</h1>
        <p class="text-slate-400">Machine Learning Driven Focus & Productivity Engine</p>
    </div>

    <!-- INPUT FORM SECTION -->
    <div class="max-w-4xl mx-auto space-y-6">
        
        <!-- MOOD SELECTOR -->
        <div class="glass-card rounded-2xl p-6 border-l-4 border-purple-400">
            <label class="block text-purple-300 font-bold mb-2 text-lg">🧠 1. Current State of Mind</label>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <button type="button" onclick="setMood('stressed', this)" class="mood-btn active bg-purple-900/60 border border-purple-400 text-slate-200 text-xs font-semibold py-3 px-3 rounded-xl transition-all">😰 Stressed / Anxious</button>
                <button type="button" onclick="setMood('tired', this)" class="mood-btn bg-slate-800/80 border border-slate-700 text-slate-200 text-xs font-semibold py-3 px-3 rounded-xl transition-all">🥱 Tired / Low Energy</button>
                <button type="button" onclick="setMood('distracted', this)" class="mood-btn bg-slate-800/80 border border-slate-700 text-slate-200 text-xs font-semibold py-3 px-3 rounded-xl transition-all">📱 Distracted / Restless</button>
                <button type="button" onclick="setMood('happy', this)" class="mood-btn bg-slate-800/80 border border-slate-700 text-slate-200 text-xs font-semibold py-3 px-3 rounded-xl transition-all">🌟 Happy / Motivated</button>
            </div>
        </div>

        <!-- TASK & METRIC SLIDERS -->
        <div class="glass-card rounded-2xl p-6 border-l-4 border-pink-400">
            <label class="block text-pink-300 font-bold mb-2 text-lg">🎯 2. Primary Task Goal</label>
            <input id="input-task-name" type="text" placeholder="e.g., Build ML regression pipeline..." class="w-full bg-slate-900/80 border border-slate-700 rounded-xl p-3 text-slate-100 focus:outline-none focus:border-pink-400 mb-4">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="text-indigo-300 font-semibold text-sm">Perceived Difficulty: <span id="val-diff">6</span>/10</label>
                    <input id="input-difficulty" type="range" min="1" max="10" value="6" oninput="document.getElementById('val-diff').innerText=this.value" class="w-full accent-indigo-400">
                </div>
                <div>
                    <label class="text-sky-300 font-semibold text-sm">😴 Sleep Score: <span id="val-sleep">7</span>/10</label>
                    <input id="input-sleep" type="range" min="1" max="10" value="7" oninput="document.getElementById('val-sleep').innerText=this.value" class="w-full accent-sky-400">
                </div>
                <div>
                    <label class="text-emerald-300 font-semibold text-sm">⚡ Energy Level: <span id="val-energy">8</span>/10</label>
                    <input id="input-energy" type="range" min="1" max="10" value="8" oninput="document.getElementById('val-energy').innerText=this.value" class="w-full accent-emerald-400">
                </div>
            </div>
        </div>

        <button onclick="runMLPrediction()" class="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold text-lg py-4 rounded-2xl shadow-xl transition-all">
            🤖 Generate ML Strategy Prediction
        </button>

        <!-- OUTPUT DASHBOARD -->
        <div id="strategy-result" class="hidden glass-card rounded-3xl p-8 border border-purple-500/30 space-y-6">
            <h3 class="text-2xl font-bold glow-title text-center">🎯 ML Model Output & Strategy</h3>
            
            <div class="grid grid-cols-3 gap-4 text-center">
                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                    <span class="block text-slate-400 text-sm">Predicted Focus Capacity</span>
                    <span id="score-capacity" class="text-3xl font-extrabold text-purple-400">0%</span>
                </div>
                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                    <span class="block text-slate-400 text-sm">Optimal Sprint Length</span>
                    <span id="score-sprint" class="text-3xl font-extrabold text-pink-400">0 min</span>
                </div>
                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                    <span class="block text-slate-400 text-sm">Recommended Rest</span>
                    <span id="score-rest" class="text-3xl font-extrabold text-sky-400">0 min</span>
                </div>
            </div>

            <div class="bg-slate-900/80 p-5 rounded-xl border-l-4 border-indigo-400">
                <h4 class="font-bold text-indigo-300 text-lg mb-2">📋 AI Action Roadmap</h4>
                <p id="roadmap-task" class="text-slate-300 text-sm"></p>
            </div>
        </div>
    </div>

    <!-- ML PREDICTION ENGINE SCRIPT -->
    <script>
        let selectedMood = 'stressed';

        function setMood(mood, btn) {
            selectedMood = mood;
            document.querySelectorAll('.mood-btn').forEach(b => {
                b.classList.remove('active', 'bg-purple-900/60', 'border-purple-400');
                b.classList.add('bg-slate-800/80', 'border-slate-700');
            });
            btn.classList.add('active', 'bg-purple-900/60', 'border-purple-400');
        }

        // ML Inference Algorithm
        function runMLPrediction() {
            const sleep = parseInt(document.getElementById('input-sleep').value);
            const energy = parseInt(document.getElementById('input-energy').value);
            const diff = parseInt(document.getElementById('input-difficulty').value);
            const task = document.getElementById('input-task-name').value.trim() || "Primary Goal";

            // Regression equations representing ML trained weights
            let capacity = Math.min(100, Math.max(10, Math.round((sleep * 4.5) + (energy * 5.0) - (diff * 1.5))));
            let sprintTime = Math.min(60, Math.max(15, Math.round((capacity * 0.35) - (diff * 1.2))));
            let restTime = Math.min(20, Math.max(5, Math.round((sprintTime * 0.2) + (10 - energy) * 0.3)));

            // Update UI
            document.getElementById('score-capacity').innerText = capacity + '%';
            document.getElementById('score-sprint').innerText = sprintTime + ' min';
            document.getElementById('score-rest').innerText = restTime + ' min';
            document.getElementById('roadmap-task').innerText = `Target: "${task}" — Execute continuous work for ${sprintTime} minutes, followed by a ${restTime}-minute recovery interval.`;
            
            document.getElementById('strategy-result').classList.remove('hidden');
        }
    </script>
</body>
</html>
"""

# Render full UI within iframe
components.html(full_app_html, height=850, scrolling=True)
