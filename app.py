import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FocusMate AI Pro", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
        .block-container { padding: 0 !important; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

app_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
        
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: radial-gradient(circle at 50% 20%, #1e1b2e 0%, #0b0f17 100%);
            color: #f8fafc;
            overflow-x: hidden;
            min-height: 100vh;
            margin: 0;
        }

        .glass-card {
            background: rgba(30, 27, 46, 0.6);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(192, 132, 252, 0.2);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        .glow-title {
            background: linear-gradient(135deg, #e9d5ff 0%, #c084fc 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .mood-btn.active {
            border-color: #c084fc !important;
            background-color: rgba(147, 51, 234, 0.3) !important;
            box-shadow: 0 0 12px rgba(192, 132, 252, 0.3);
        }

        canvas {
            pointer-events: none;
        }
    </style>
</head>
<body class="relative flex flex-col justify-between items-center min-h-screen p-6">

    <canvas id="stage" class="fixed inset-0 w-full h-full z-20"></canvas>

    <!-- SCREEN 1: WELCOME SCREEN -->
    <div id="welcome-screen" class="relative z-10 flex flex-col items-center justify-center min-h-screen text-center w-full max-w-2xl mx-auto py-8">
        <h1 class="text-6xl font-extrabold tracking-tight glow-title mb-2">FocusMate AI</h1>
        <p class="text-slate-400 text-lg mb-6">Your End-to-End Deep Work Engine</p>

        <div id="speech-bubble" class="opacity-0 translate-y-4 bg-gradient-to-r from-purple-200 to-pink-200 text-slate-900 font-bold text-xl px-8 py-4 rounded-2xl shadow-lg relative speech-tail mb-44">
            "Hi! Ready to boost your productivity today?" ✨
        </div>

        <button id="dive-btn" onclick="startFlightSequence()" class="opacity-0 translate-y-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold text-xl px-10 py-4 rounded-2xl shadow-xl transition-all duration-300 transform hover:scale-105 active:scale-95 cursor-pointer">
            Let's Dive In! 🚀
        </button>
    </div>

    <!-- SCREEN 2: WORKSPACE -->
    <div id="workspace-screen" class="hidden relative z-10 w-full max-w-4xl mx-auto py-12">
        <div class="glass-card rounded-3xl p-6 mb-8 text-center relative">
            <h2 class="text-3xl font-bold glow-title mb-2">Interactive Mission Center</h2>
            <p id="guide-text" class="text-pink-200 font-semibold text-lg">"Configure your parameters to generate a custom focus strategy."</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- 1. MOOD SELECTOR -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-purple-400 md:col-span-2">
                <label class="block text-purple-300 font-bold mb-1 text-lg">🧠 1. Current State of Mind</label>
                <p class="text-slate-400 text-xs mb-3">Select your current mental state:</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                    <button type="button" id="btn-stressed" onclick="selectMood('stressed')" class="mood-btn active bg-slate-800/80 hover:bg-purple-900/40 border border-slate-700 text-slate-200 text-xs font-semibold py-3 px-3 rounded-xl transition-all text-center">
                        😰 Stressed / Anxious
                    </button>
                    <button type="button" id="btn-tired" onclick="selectMood('tired')" class="mood-btn bg-slate-800/80 hover:bg-purple-900/40 border border-slate-700 text-slate-200 text-xs font-semibold py-3 px-3 rounded-xl transition-all text-center">
                        🥱 Tired / Low Energy
                    </button>
                    <button type="button" id="btn-distracted" onclick="selectMood('distracted')" class="mood-btn bg-slate-800/80 hover:bg-purple-900/40 border border-slate-700 text-slate-200 text-xs font-semibold py-3 px-3 rounded-xl transition-all text-center">
                        📱 Distracted / Restless
                    </button>
                    <button type="button" id="btn-happy" onclick="selectMood('happy')" class="mood-btn bg-slate-800/80 hover:bg-purple-900/40 border border-slate-700 text-slate-200 text-xs font-semibold py-3 px-3 rounded-xl transition-all text-center">
                        🌟 Happy / Motivated
                    </button>
                </div>
            </div>

            <!-- 2. TASK INPUT & DIFFICULTY -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-pink-400 md:col-span-2">
                <label class="block text-pink-300 font-bold mb-1 text-lg">🎯 2. Primary Task Goal</label>
                <input id="input-task-name" type="text" placeholder="e.g., Write Chapter 1 of Biology Notes, Build UI layout..." class="w-full bg-slate-900/80 border border-slate-700 rounded-xl p-3 text-slate-100 focus:outline-none focus:border-pink-400 mb-4">
                
                <div class="flex justify-between items-center mb-2">
                    <label class="text-indigo-300 font-semibold text-sm">Perceived Difficulty</label>
                    <span id="badge-difficulty" class="bg-indigo-500/20 text-indigo-300 border border-indigo-400/40 px-3 py-1 rounded-lg font-bold text-xs">6 / 10</span>
                </div>
                <input id="input-difficulty" type="range" min="1" max="10" value="6" oninput="updateSliderValue('difficulty', this.value)" class="w-full accent-indigo-400 cursor-pointer">
            </div>

            <!-- 3. SLEEP QUALITY SLIDER -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-sky-400">
                <div class="flex justify-between items-center mb-2">
                    <label class="text-sky-300 font-bold text-lg">😴 3. Sleep Score</label>
                    <span id="badge-sleep" class="bg-sky-500/20 text-sky-300 border border-sky-400/40 px-3 py-1 rounded-lg font-extrabold text-base">7 / 10</span>
                </div>
                <input id="input-sleep" type="range" min="1" max="10" value="7" oninput="updateSliderValue('sleep', this.value)" class="w-full accent-sky-400 cursor-pointer">
            </div>

            <!-- 4. ENERGY LEVEL SLIDER -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-emerald-400">
                <div class="flex justify-between items-center mb-2">
                    <label class="text-emerald-300 font-bold text-lg">⚡ 4. Energy Level</label>
                    <span id="badge-energy" class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/40 px-3 py-1 rounded-lg font-extrabold text-base">8 / 10</span>
                </div>
                <input id="input-energy" type="range" min="1" max="10" value="8" oninput="updateSliderValue('energy', this.value)" class="w-full accent-emerald-400 cursor-pointer">
            </div>
        </div>

        <button onclick="generateStrategy()" class="w-full mt-8 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold text-xl py-5 rounded-2xl shadow-xl hover:opacity-90 transition-all cursor-pointer">
            ✨ Generate Focus Strategy ✨
        </button>

        <!-- RESULTS SECTION -->
        <div id="strategy-result" class="hidden mt-10 space-y-6">
            <div class="glass-card rounded-3xl p-8 border border-purple-500/30">
                <h3 class="text-2xl font-bold glow-title mb-4 text-center">🎯 Strategy & Action Plan</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 text-center">
                    <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                        <span class="block text-slate-400 text-sm">Focus Capacity</span>
                        <span id="score-capacity" class="text-3xl font-extrabold text-purple-400">85%</span>
                    </div>
                    <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                        <span class="block text-slate-400 text-sm">Sprint Duration</span>
                        <span id="score-sprint" class="text-3xl font-extrabold text-pink-400">25 min</span>
                    </div>
                    <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700">
                        <span class="block text-slate-400 text-sm">Rest Interval</span>
                        <span id="score-rest" class="text-3xl font-extrabold text-sky-400">5 min</span>
                    </div>
                </div>

                <!-- DYNAMIC TASK BREAKDOWN -->
                <div class="bg-slate-900/80 p-5 rounded-xl border-l-4 border-indigo-400 mb-4">
                    <h4 class="font-bold text-indigo-300 text-lg mb-2">📋 AI Action Roadmap (3 Steps)</h4>
                    <ol id="task-steps-list" class="list-decimal list-inside space-y-2 text-slate-300 text-sm font-medium">
                    </ol>
                </div>

                <!-- LIVE TIMER & AUDIO SUITE -->
                <div class="bg-gradient-to-r from-slate-900 to-purple-950 p-6 rounded-2xl border border-purple-500/30 text-center mb-6">
                    <span class="text-xs uppercase tracking-widest text-slate-400 font-semibold">Active Execution Suite</span>
                    <div id="timer-display" class="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-300 my-3">25:00</div>
                    
                    <div class="flex justify-center gap-3 mb-4">
                        <button id="timer-btn" onclick="toggleTimer()" class="bg-purple-600 hover:bg-purple-500 text-white font-bold px-6 py-2 rounded-xl text-sm transition-all">Start Sprint</button>
                        <button onclick="resetTimer()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold px-4 py-2 rounded-xl text-sm transition-all">Reset</button>
                    </div>

                    <!-- AMBIENT AUDIO PLAYER -->
                    <div class="flex items-center justify-center gap-2 text-xs text-slate-400 border-t border-slate-800 pt-3">
                        <span>🔊 Soundscape:</span>
                        <select id="audio-select" onchange="changeAudioSource()" class="bg-slate-900 text-purple-300 font-semibold rounded-lg px-2 py-1 border border-slate-700 focus:outline-none">
                            <option value="binaural">Alpha Binaural Beats (Focus)</option>
                            <option value="rain">Calming Heavy Rain (Stress Relief)</option>
                            <option value="white">White Noise (Distraction Blocking)</option>
                        </select>
                        <button onclick="toggleAudio()" id="audio-btn" class="text-pink-400 font-bold ml-2 underline">Play Sound</button>
                    </div>
                </div>

                <!-- ANALYTICS & STREAK TRACKER -->
                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-700 flex justify-between items-center">
                    <div>
                        <span class="block text-slate-400 text-xs font-bold uppercase">Daily Streak</span>
                        <span id="streak-count" class="text-2xl font-extrabold text-emerald-400">🔥 1 Day</span>
                    </div>
                    <div class="text-right">
                        <span class="block text-slate-400 text-xs font-bold uppercase">Completed Sprints</span>
                        <span id="sprint-count" class="text-2xl font-extrabold text-sky-400">0 Sprints</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- AUDIO ENGINE -->
    <audio id="ambient-audio" loop></audio>

    <script>
        let selectedMoodState = 'stressed';
        let timerInterval = null;
        let timeRemaining = 1500;
        let isTimerRunning = false;
        let audioPlaying = false;
        let sprintsCompleted = 0;
        let currentSprintDuration = 25;

        const soundUrls = {
            binaural: "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3",
            rain: "https://cdn.pixabay.com/download/audio/2021/09/06/audio_8a287e07eb.mp3",
            white: "https://cdn.pixabay.com/download/audio/2022/03/24/audio_c8c8731f82.mp3"
        };

        function selectMood(mood) {
            selectedMoodState = mood;
            document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`btn-${mood}`).classList.add('active');
        }

        function updateSliderValue(id, value) {
            document.getElementById(`badge-${id}`).innerText = `${value} / 10`;
        }

        const canvas = document.getElementById('stage');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const robot = { x: window.innerWidth / 2, y: -150 };
        const particles = [];

        function createSmokeParticle(x, y) {
            particles.push({
                x: x + (Math.random() * 20 - 10),
                y: y,
                vx: Math.random() * 2 - 1,
                vy: Math.random() * 4 + 2,
                radius: Math.random() * 12 + 6,
                alpha: 0.8,
                color: Math.random() > 0.5 ? '#f472b6' : '#c084fc'
            });
        }

        function drawRobot(x, y) {
            ctx.save();
            ctx.translate(x, y);

            const grad = ctx.createRadialGradient(0, 0, 10, 0, 0, 90);
            grad.addColorStop(0, 'rgba(192, 132, 252, 0.35)');
            grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(0, 0, 90, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#f472b6';
            ctx.beginPath();
            ctx.arc(0, -65, 8, 0, Math.PI * 2);
            ctx.fill();

            ctx.strokeStyle = '#cbd5e1';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, -57);
            ctx.lineTo(0, -42);
            ctx.stroke();

            ctx.fillStyle = '#c084fc';
            ctx.beginPath();
            ctx.roundRect(-45, -42, 90, 64, 20);
            ctx.fill();

            ctx.fillStyle = '#1e1b2e';
            ctx.beginPath();
            ctx.roundRect(-35, -32, 70, 44, 12);
            ctx.fill();

            ctx.fillStyle = '#38bdf8';
            ctx.beginPath();
            ctx.arc(-16, -10, 7, 0, Math.PI * 2);
            ctx.arc(16, -10, 7, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = 'rgba(244, 114, 182, 0.6)';
            ctx.beginPath();
            ctx.arc(-22, 4, 5, 0, Math.PI * 2);
            ctx.arc(22, 4, 5, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#a855f7';
            ctx.beginPath();
            ctx.roundRect(-28, 28, 56, 40, 14);
            ctx.fill();

            ctx.fillStyle = '#f472b6';
            ctx.beginPath();
            ctx.arc(0, 48, 7, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#c084fc';
            ctx.beginPath();
            ctx.arc(-40, 42, 9, 0, Math.PI * 2);
            ctx.arc(40, 42, 9, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#8b5cf6';
            ctx.beginPath();
            ctx.roundRect(-20, 68, 14, 22, 6);
            ctx.roundRect(6, 68, 14, 22, 6);
            ctx.fill();

            ctx.fillStyle = '#f472b6';
            ctx.beginPath();
            ctx.roundRect(-22, 88, 18, 10, 4);
            ctx.roundRect(4, 88, 18, 10, 4);
            ctx.fill();

            ctx.restore();
        }

        let frame = 0;
        let isFlying = false;

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            frame += 0.04;
            const hoverY = robot.y + (isFlying ? 0 : Math.sin(frame) * 8);

            if (isFlying) {
                for (let i = 0; i < 3; i++) {
                    createSmokeParticle(robot.x - 12, hoverY + 98);
                    createSmokeParticle(robot.x + 12, hoverY + 98);
                }
            }

            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.alpha -= 0.015;
                p.radius += 0.2;

                if (p.alpha <= 0) {
                    particles.splice(i, 1);
                } else {
                    ctx.save();
                    ctx.globalAlpha = p.alpha;
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.restore();
                }
            }

            drawRobot(robot.x, hoverY);
            requestAnimationFrame(animate);
        }
        animate();

        window.addEventListener('DOMContentLoaded', () => {
            gsap.to(robot, {
                y: window.innerHeight / 2 + 30,
                duration: 1.8,
                ease: "back.out(1.4)",
                onComplete: () => {
                    gsap.to('#speech-bubble', { opacity: 1, y: 0, duration: 0.6 });
                    gsap.to('#dive-btn', { opacity: 1, y: 0, duration: 0.6, delay: 0.2 });
                }
            });
        });

        function startFlightSequence() {
            isFlying = true;
            gsap.to('#welcome-screen', { opacity: 0, duration: 0.4 });
            gsap.to(robot, {
                y: -300,
                duration: 1.2,
                ease: "power2.in",
                onComplete: () => {
                    document.getElementById('welcome-screen').classList.add('hidden');
                    document.getElementById('workspace-screen').classList.remove('hidden');
                    robot.x = window.innerWidth - 120;
                    robot.y = -100;
                    gsap.to(robot, {
                        y: 120,
                        duration: 1,
                        ease: "bounce.out",
                        onComplete: () => { isFlying = false; }
                    });
                }
            });
        }

        // STRATEGY & TASK BREAKDOWN LOGIC
        function generateStrategy() {
            const sleep = parseInt(document.getElementById('input-sleep').value);
            const energy = parseInt(document.getElementById('input-energy').value);
            const difficulty = parseInt(document.getElementById('input-difficulty').value);
            const rawTask = document.getElementById('input-task-name').value.trim();
            const taskName = rawTask || "Primary Goal";

            let capacity = Math.round(((sleep * 0.4) + (energy * 0.6)) * 10);
            
            let sprintTime = 25;
            if (capacity >= 75 && difficulty <= 7) sprintTime = 45;
            else if (capacity < 45 || difficulty >= 8) sprintTime = 15;

            currentSprintDuration = sprintTime;
            timeRemaining = sprintTime * 60;
            updateTimerDisplay();

            let restTime = sprintTime === 45 ? 10 : 5;

            document.getElementById('score-capacity').innerText = capacity + '%';
            document.getElementById('score-sprint').innerText = sprintTime + ' min';
            document.getElementById('score-rest').innerText = restTime + ' min';

            // Generate 3 Actionable Micro-Steps based on task input
            const listContainer = document.getElementById('task-steps-list');
            listContainer.innerHTML = `
                <li>Set up workspace and open resources for: <strong>${taskName}</strong>.</li>
                <li>Execute core effort for ${sprintTime} minutes (focus solely on step 1 of ${taskName}).</li>
                <li>Review progress, outline next steps, and enter a ${restTime}-minute break.</li>
            `;

            // Auto-set ambient audio preset based on mood selection
            const audioSelect = document.getElementById('audio-select');
            if (selectedMoodState === 'stressed') audioSelect.value = 'rain';
            else if (selectedMoodState === 'distracted') audioSelect.value = 'white';
            else audioSelect.value = 'binaural';

            document.getElementById('guide-text').innerText = '"Strategy & roadmap calculated below!"';
            const resultDiv = document.getElementById('strategy-result');
            resultDiv.classList.remove('hidden');
            resultDiv.scrollIntoView({ behavior: 'smooth' });
        }

        // TIMER ENGINE logic
        function updateTimerDisplay() {
            const mins = Math.floor(timeRemaining / 60);
            const secs = timeRemaining % 60;
            document.getElementById('timer-display').innerText = 
                `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }

        function toggleTimer() {
            const btn = document.getElementById('timer-btn');
            if (isTimerRunning) {
                clearInterval(timerInterval);
                isTimerRunning = false;
                btn.innerText = "Resume Sprint";
                btn.className = "bg-purple-600 hover:bg-purple-500 text-white font-bold px-6 py-2 rounded-xl text-sm transition-all";
            } else {
                isTimerRunning = true;
                btn.innerText = "Pause";
                btn.className = "bg-pink-600 hover:bg-pink-500 text-white font-bold px-6 py-2 rounded-xl text-sm transition-all";
                timerInterval = setInterval(() => {
                    if (timeRemaining > 0) {
                        timeRemaining--;
                        updateTimerDisplay();
                    } else {
                        clearInterval(timerInterval);
                        isTimerRunning = false;
                        sprintsCompleted++;
                        document.getElementById('sprint-count').innerText = `${sprintsCompleted} Sprints`;
                        alert("🎉 Sprint Completed! Take your break now.");
                        resetTimer();
                    }
                }, 1000);
            }
        }

        function resetTimer() {
            clearInterval(timerInterval);
            isTimerRunning = false;
            timeRemaining = currentSprintDuration * 60;
            updateTimerDisplay();
            const btn = document.getElementById('timer-btn');
            btn.innerText = "Start Sprint";
            btn.className = "bg-purple-600 hover:bg-purple-500 text-white font-bold px-6 py-2 rounded-xl text-sm transition-all";
        }

        // AMBIENT AUDIO ENGINE logic
        function toggleAudio() {
            const audio = document.getElementById('ambient-audio');
            const btn = document.getElementById('audio-btn');
            const selected = document.getElementById('audio-select').value;

            if (audioPlaying) {
                audio.pause();
                audioPlaying = false;
                btn.innerText = "Play Sound";
            } else {
                audio.src = soundUrls[selected];
                audio.play();
                audioPlaying = true;
                btn.innerText = "Pause Sound";
            }
        }

        function changeAudioSource() {
            if (audioPlaying) {
                const audio = document.getElementById('ambient-audio');
                const selected = document.getElementById('audio-select').value;
                audio.src = soundUrls[selected];
                audio.play();
            }
        }
    </script>
</body>
</html>
"""

components.html(app_code, height=950, scrolling=True)
