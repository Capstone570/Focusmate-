import streamlit as st
import streamlit.components.v1 as components

# 1. Page Setup
st.set_page_config(page_title="FocusMate AI", page_icon="🔮", layout="wide")

# Hide standard Streamlit header/padding
st.markdown("""
    <style>
        .block-container { padding: 0 !important; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. Application Code with Dynamic Slider Badges & Scale Labels
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

        .speech-tail::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 10px 10px 0;
            border-style: solid;
            border-color: #fbcfe8 transparent;
            display: block;
            width: 0;
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
        <h1 class="text-6xl font-extrabold tracking-tight glow-title mb-2">FocusMate</h1>
        <p class="text-slate-400 text-lg mb-6">Your AI-Powered Deep Work Companion</p>

        <div id="speech-bubble" class="opacity-0 translate-y-4 bg-gradient-to-r from-purple-200 to-pink-200 text-slate-900 font-bold text-xl px-8 py-4 rounded-2xl shadow-lg relative speech-tail mb-44">
            "Hi! Welcome to FocusMate!" ✨
        </div>

        <button id="dive-btn" onclick="startFlightSequence()" class="opacity-0 translate-y-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold text-xl px-10 py-4 rounded-2xl shadow-xl transition-all duration-300 transform hover:scale-105 active:scale-95 cursor-pointer">
            Let's Dive In! 🚀
        </button>
    </div>

    <!-- SCREEN 2: WORKSPACE -->
    <div id="workspace-screen" class="hidden relative z-10 w-full max-w-4xl mx-auto py-12">
        <div class="glass-card rounded-3xl p-6 mb-8 text-center relative">
            <h2 class="text-3xl font-bold glow-title mb-2">Interactive Mission Center</h2>
            <p id="guide-text" class="text-pink-200 font-semibold text-lg">"Let's configure your 5 session parameters below!"</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- 1. MIND DUMP -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-purple-400 md:col-span-2">
                <label class="block text-purple-300 font-bold mb-2 text-lg">💬 1. AI Mind Dump</label>
                <textarea id="input-mind" class="w-full bg-slate-900/80 border border-slate-700 rounded-xl p-4 text-slate-100 focus:outline-none focus:border-purple-400" rows="3" placeholder="Vent your raw thoughts, doubts, or anxieties here..."></textarea>
            </div>

            <!-- 2. TARGET HOURS -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-pink-400">
                <label class="block text-pink-300 font-bold mb-2 text-lg">📚 2. Target Study Hours</label>
                <input id="input-hours" type="number" min="1" max="12" value="3" class="w-full bg-slate-900/80 border border-slate-700 rounded-xl p-3 text-slate-100 focus:outline-none focus:border-pink-400">
            </div>

            <!-- 3. SLEEP QUALITY SLIDER -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-sky-400">
                <div class="flex justify-between items-center mb-2">
                    <label class="text-sky-300 font-bold text-lg">😴 3. Sleep Quality Score</label>
                    <span id="badge-sleep" class="bg-sky-500/20 text-sky-300 border border-sky-400/40 px-3 py-1 rounded-lg font-extrabold text-base">7 / 10</span>
                </div>
                <input id="input-sleep" type="range" min="1" max="10" value="7" oninput="updateSliderValue('sleep', this.value)" class="w-full accent-sky-400 cursor-pointer">
                <div class="flex justify-between text-xs text-slate-400 mt-1">
                    <span>1 (Poor)</span>
                    <span>10 (Restful)</span>
                </div>
            </div>

            <!-- 4. TASK DIFFICULTY SLIDER -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-indigo-400">
                <div class="flex justify-between items-center mb-2">
                    <label class="text-indigo-300 font-bold text-lg">🎯 4. Task Difficulty</label>
                    <span id="badge-difficulty" class="bg-indigo-500/20 text-indigo-300 border border-indigo-400/40 px-3 py-1 rounded-lg font-extrabold text-base">6 / 10</span>
                </div>
                <input id="input-difficulty" type="range" min="1" max="10" value="6" oninput="updateSliderValue('difficulty', this.value)" class="w-full accent-indigo-400 cursor-pointer">
                <div class="flex justify-between text-xs text-slate-400 mt-1">
                    <span>1 (Easy)</span>
                    <span>10 (Extreme)</span>
                </div>
            </div>

            <!-- 5. ENERGY LEVEL SLIDER -->
            <div class="glass-card rounded-2xl p-6 border-l-4 border-emerald-400">
                <div class="flex justify-between items-center mb-2">
                    <label class="text-emerald-300 font-bold text-lg">⚡ 5. Current Energy Level</label>
                    <span id="badge-energy" class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/40 px-3 py-1 rounded-lg font-extrabold text-base">8 / 10</span>
                </div>
                <input id="input-energy" type="range" min="1" max="10" value="8" oninput="updateSliderValue('energy', this.value)" class="w-full accent-emerald-400 cursor-pointer">
                <div class="flex justify-between text-xs text-slate-400 mt-1">
                    <span>1 (Exhausted)</span>
                    <span>10 (Fully Charged)</span>
                </div>
            </div>
        </div>

        <button onclick="generateStrategy()" class="w-full mt-8 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold text-xl py-5 rounded-2xl shadow-xl hover:opacity-90 transition-all cursor-pointer">
            ✨ Generate Focus Strategy ✨
        </button>

        <!-- RESULTS SECTION -->
        <div id="strategy-result" class="hidden mt-10 space-y-6">
            <div class="glass-card rounded-3xl p-8 border border-purple-500/30">
                <h3 class="text-2xl font-bold glow-title mb-4 text-center">🎯 Your Custom Focus Strategy</h3>
                
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

                <div class="space-y-4">
                    <div class="bg-slate-900/80 p-4 rounded-xl border-l-4 border-purple-400">
                        <h4 class="font-bold text-purple-300">🧠 Mind Dump & Emotional Status</h4>
                        <p id="analysis-mind" class="text-slate-300 text-sm mt-1"></p>
                    </div>
                    <div class="bg-slate-900/80 p-4 rounded-xl border-l-4 border-emerald-400">
                        <h4 class="font-bold text-emerald-300">🚀 Recommended Roadmap</h4>
                        <p id="analysis-roadmap" class="text-slate-300 text-sm mt-1"></p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // LIVE SLIDER BADGE UPDATER
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

        const robot = {
            x: window.innerWidth / 2,
            y: -150,
            size: 1
        };

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
                        onComplete: () => {
                            isFlying = false;
                        }
                    });
                }
            });
        }

        function generateStrategy() {
            const sleep = parseInt(document.getElementById('input-sleep').value);
            const energy = parseInt(document.getElementById('input-energy').value);
            const mind = document.getElementById('input-mind').value.trim().toLowerCase();

            let capacity = Math.round(((sleep * 0.4) + (energy * 0.6)) * 10);
            let sprintTime = capacity > 70 ? 45 : capacity > 40 ? 25 : 15;
            let restTime = sprintTime === 45 ? 10 : 5;

            document.getElementById('score-capacity').innerText = capacity + '%';
            document.getElementById('score-sprint').innerText = sprintTime + ' min';
            document.getElementById('score-rest').innerText = restTime + ' min';

            let emotionalFeedback = "";
            let roadmapFeedback = "";

            if (mind.includes('stress') || mind.includes('suffocat') || mind.includes('anxi') || mind.includes('overwhelmed')) {
                emotionalFeedback = "I hear you. High mental pressure detected—take a deep breath. You don't have to finish everything right now, just focus on one micro-step.";
                roadmapFeedback = "Since you're feeling overwhelmed, start with 5 minutes of super easy admin work (cleaning desktop, organizing notes) to lower cortisol before tackling hard tasks.";
            } else if (mind.includes('bored') || mind.includes('tired') || mind.includes('lazy') || mind.includes('sleepy')) {
                emotionalFeedback = "Low stimulation detected. Your brain is seeking dopamine and resisting deep effort.";
                roadmapFeedback = "Use the '5-Minute Rule': commit to working for just 300 seconds. If you still feel bored, take a brisk walk, drink cold water, and change your work spot.";
            } else if (mind.includes('distract') || mind.includes('phone') || mind.includes('social')) {
                emotionalFeedback = "Attention fragmentation detected. External distractions are pulling your focus away.";
                roadmapFeedback = "Put your phone in another room or turn on Do Not Disturb immediately. Run a short 15-minute high-intensity micro-sprint.";
            } else if (mind.length > 0) {
                emotionalFeedback = `Thoughts logged: "${mind}". Expressing mental chatter reduces cognitive load and frees up working memory!`;
                roadmapFeedback = `Break down "${mind.substring(0, 30)}..." into 3 bite-sized steps and execute step 1 during your first ${sprintTime}-minute sprint.`;
            } else {
                emotionalFeedback = "No mental dump provided. Mind is clear and ready to work!";
                roadmapFeedback = `Start your first ${sprintTime}-minute micro-sprint directly with your highest priority task.`;
            }

            document.getElementById('analysis-mind').innerText = emotionalFeedback;
            document.getElementById('analysis-roadmap').innerText = roadmapFeedback;
            document.getElementById('guide-text').innerText = '"Strategy calculated! Check your custom roadmap below."';

            const resultDiv = document.getElementById('strategy-result');
            resultDiv.classList.remove('hidden');
            resultDiv.scrollIntoView({ behavior: 'smooth' });
        }
    </script>
</body>
</html>
"""

components.html(app_code, height=900, scrolling=True)
