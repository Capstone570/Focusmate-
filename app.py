import streamlit as st
import streamlit.components.v1 as components

# 1. Page Setup
st.set_page_config(page_title="FocusMate", page_icon="🔮", layout="wide")

# Hide standard Streamlit header/padding to give full screen to the app
st.markdown("""
    <style>
        .block-container { padding: 0 !important; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. Complete Animated Application (HTML/JS/GSAP inside Streamlit string)
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
    <div id="welcome-screen" class="relative z-10 flex flex-col items-center justify-center min-h-screen text-center w-full max-w-2xl mx-auto">
        <h1 class="text-6xl font-extrabold tracking-tight glow-title mb-2">FocusMate</h1>
        <p class="text-slate-400 text-lg mb-8">Your AI-Powered Deep Work Companion</p>

        <div id="speech-bubble" class="opacity-0 translate-y-4 bg-gradient-to-r from-purple-200 to-pink-200 text-slate-900 font-bold text-xl px-8 py-4 rounded-2xl shadow-lg relative speech-tail mb-64">
            "Hi! Welcome to FocusMate!" ✨
        </div>

        <button id="dive-btn" onclick="startFlightSequence()" class="opacity-0 translate-y-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold text-xl px-10 py-5 rounded-2xl shadow-xl transition-all duration-300 transform hover:scale-105 active:scale-95 cursor-pointer">
            Let's Dive In! 🚀
        </button>
    </div>

    <!-- SCREEN 2: 5 FEATURES GUIDED BY ROBOT -->
    <div id="workspace-screen" class="hidden relative z-10 w-full max-w-4xl mx-auto py-12">
        <div class="glass-card rounded-3xl p-6 mb-8 text-center relative">
            <h2 class="text-3xl font-bold glow-title mb-2">Interactive Mission Center</h2>
            <p id="guide-text" class="text-pink-200 font-semibold text-lg">"Let's configure your 5 session parameters below!"</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="glass-card rounded-2xl p-6 border-l-4 border-purple-400 md:col-span-2">
                <label class="block text-purple-300 font-bold mb-2 text-lg">💬 1. AI Mind Dump</label>
                <textarea class="w-full bg-slate-900/80 border border-slate-700 rounded-xl p-4 text-slate-100 focus:outline-none focus:border-purple-400" rows="3" placeholder="Vent your raw thoughts, doubts, or anxieties here..."></textarea>
            </div>

            <div class="glass-card rounded-2xl p-6 border-l-4 border-pink-400">
                <label class="block text-pink-300 font-bold mb-2 text-lg">📚 2. Target Study Hours</label>
                <input type="number" min="1" max="12" value="3" class="w-full bg-slate-900/80 border border-slate-700 rounded-xl p-3 text-slate-100 focus:outline-none focus:border-pink-400">
            </div>

            <div class="glass-card rounded-2xl p-6 border-l-4 border-sky-400">
                <label class="block text-sky-300 font-bold mb-2 text-lg">😴 3. Sleep Quality Score (1-10)</label>
                <input type="range" min="1" max="10" value="7" class="w-full accent-sky-400 cursor-pointer">
            </div>

            <div class="glass-card rounded-2xl p-6 border-l-4 border-indigo-400">
                <label class="block text-indigo-300 font-bold mb-2 text-lg">🎯 4. Task Difficulty (1-10)</label>
                <input type="range" min="1" max="10" value="6" class="w-full accent-indigo-400 cursor-pointer">
            </div>

            <div class="glass-card rounded-2xl p-6 border-l-4 border-emerald-400">
                <label class="block text-emerald-300 font-bold mb-2 text-lg">⚡ 5. Current Energy Level (1-10)</label>
                <input type="range" min="1" max="10" value="8" class="w-full accent-emerald-400 cursor-pointer">
            </div>
        </div>

        <button onclick="alert('Focus Strategy Generated! 🚀')" class="w-full mt-8 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold text-xl py-5 rounded-2xl shadow-xl hover:opacity-90 transition-all cursor-pointer">
            ✨ Generate Focus Strategy ✨
        </button>
    </div>

    <script>
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

            const grad = ctx.createRadialGradient(0, 0, 10, 0, 0, 80);
            grad.addColorStop(0, 'rgba(192, 132, 252, 0.4)');
            grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(0, 0, 80, 0, Math.PI * 2);
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
            ctx.roundRect(-28, 28, 56, 44, 14);
            ctx.fill();

            ctx.fillStyle = '#f472b6';
            ctx.beginPath();
            ctx.arc(0, 48, 7, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#c084fc';
            ctx.beginPath();
            ctx.arc(-42, 42, 10, 0, Math.PI * 2);
            ctx.arc(42, 42, 10, 0, Math.PI * 2);
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
                    createSmokeParticle(robot.x, hoverY + 60);
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
                y: window.innerHeight / 2 - 20,
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
    </script>
</body>
</html>
"""

# Render inside Streamlit safely
components.html(app_code, height=900, scrolling=True)
