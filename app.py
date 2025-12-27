# ==============================================================================
# NIMBUS AI - HYPER-SCALE CLOUD DASHBOARD PLATFORM (ENTERPRISE EDITION V5)
# ==============================================================================
# Architecture: Monolithic Single-File Flask App
# Frontend: Custom CSS Framework + Canvas JS Engine
# Backend: Python Flask + Psutil System Monitor
# ==============================================================================

import psutil
import os
import time
import threading
import random
import datetime
import json
from flask import Flask, render_template_string, jsonify, request, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)
start_time = time.time()
stress_mode = False

# ------------------------------------------------------------------------------
# 1. DESIGN SYSTEM (CSS ENGINE)
# ------------------------------------------------------------------------------
CSS_CORE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    :root {
        --c-bg: #09090b;
        --c-surface: #18181b;
        --c-surface-highlight: #27272a;
        --c-border: #3f3f46;
        --c-text-main: #f4f4f5;
        --c-text-muted: #a1a1aa;
        --c-primary: #6366f1;
        --c-primary-glow: rgba(99, 102, 241, 0.5);
        --c-accent: #06b6d4;
        --c-success: #10b981;
        --c-danger: #ef4444;
        --radius: 12px;
        --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        background-color: var(--c-bg);
        color: var(--c-text-main);
        font-family: 'Plus Jakarta Sans', sans-serif;
        line-height: 1.6;
        overflow-x: hidden;
        -webkit-font-smoothing: antialiased;
    }

    /* --- LAYOUT UTILITIES --- */
    .container { max-width: 1400px; margin: 0 auto; padding: 0 2rem; position: relative; z-index: 2; }
    .grid { display: grid; gap: 2rem; }
    .grid-2 { grid-template-columns: repeat(2, 1fr); }
    .grid-3 { grid-template-columns: repeat(3, 1fr); }
    .grid-4 { grid-template-columns: repeat(4, 1fr); }
    .flex { display: flex; align-items: center; }
    .flex-col { flex-direction: column; }
    .justify-between { justify-content: space-between; }
    .justify-center { justify-content: center; }
    .gap-4 { gap: 1rem; }
    .gap-8 { gap: 2rem; }
    .py-20 { padding-top: 5rem; padding-bottom: 5rem; }
    .mt-10 { margin-top: 2.5rem; }
    .text-center { text-align: center; }
    .w-full { width: 100%; }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3, h4 { line-height: 1.1; font-weight: 800; letter-spacing: -0.025em; color: #fff; }
    h1 { font-size: 4rem; }
    h2 { font-size: 2.5rem; margin-bottom: 1rem; }
    h3 { font-size: 1.5rem; margin-bottom: 0.5rem; }
    p { color: var(--c-text-muted); font-size: 1.1rem; max-width: 60ch; }
    
    .text-gradient {
        background: linear-gradient(135deg, #fff 0%, var(--c-text-muted) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .text-gradient-primary {
        background: linear-gradient(135deg, var(--c-primary) 0%, var(--c-accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* --- COMPONENTS --- */
    .btn {
        display: inline-flex; align-items: center; justify-content: center;
        padding: 0.8rem 1.6rem; border-radius: 99px; font-weight: 600;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; text-decoration: none; border: 1px solid transparent;
        font-size: 0.95rem; gap: 0.5rem;
    }
    .btn-primary {
        background: var(--c-primary); color: #fff;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 30px rgba(99, 102, 241, 0.5); }
    
    .btn-outline {
        background: transparent; border-color: var(--c-border); color: #fff;
    }
    .btn-outline:hover { border-color: #fff; background: rgba(255,255,255,0.05); }

    .btn-danger {
        background: rgba(239, 68, 68, 0.15); color: var(--c-danger); border-color: rgba(239, 68, 68, 0.3);
    }
    .btn-danger:hover { background: var(--c-danger); color: #fff; }

    .card {
        background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--radius);
        padding: 2rem; position: relative; overflow: hidden; transition: 0.3s;
    }
    .card:hover { border-color: var(--c-primary); transform: translateY(-5px); box-shadow: var(--shadow); }
    
    .badge {
        padding: 0.25rem 0.75rem; border-radius: 99px; font-size: 0.75rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .badge-live { background: rgba(16, 185, 129, 0.2); color: var(--c-success); display: flex; align-items: center; gap: 6px; width: fit-content; }
    .dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; animation: pulse 2s infinite; }

    /* --- NAVBAR --- */
    .navbar {
        position: fixed; top: 0; left: 0; width: 100%; z-index: 100;
        background: rgba(9, 9, 11, 0.8); backdrop-filter: blur(20px); border-bottom: 1px solid var(--c-border);
    }
    .nav-inner { height: 80px; display: flex; justify-content: space-between; align-items: center; }
    .brand { font-size: 1.5rem; font-weight: 800; color: #fff; text-decoration: none; display: flex; align-items: center; gap: 0.5rem; }
    .nav-list { display: flex; gap: 2rem; list-style: none; }
    .nav-link { color: var(--c-text-muted); text-decoration: none; font-weight: 500; transition: 0.2s; }
    .nav-link:hover, .nav-link-active { color: #fff; }

    /* --- CANVAS --- */
    #bg-canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; opacity: 0.6; }

    /* --- DASHBOARD WIDGETS --- */
    .metric-value { font-size: 3.5rem; font-weight: 800; margin: 1rem 0; line-height: 1; color: #fff; font-family: 'JetBrains Mono', monospace; }
    .progress-bar { width: 100%; height: 6px; background: #27272a; border-radius: 99px; overflow: hidden; }
    .progress-fill { height: 100%; background: var(--c-primary); transition: width 0.5s ease; }
    
    .terminal-box {
        background: #000; border: 1px solid #333; border-radius: var(--radius); padding: 1.5rem;
        height: 300px; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--c-success);
    }
    .log-entry { margin-bottom: 0.5rem; display: flex; gap: 1rem; }
    .timestamp { color: #555; }

    /* --- FOOTER --- */
    footer { border-top: 1px solid var(--c-border); padding: 4rem 0; margin-top: auto; background: var(--c-surface); }
    .footer-links a { display: block; margin-bottom: 0.5rem; color: var(--c-text-muted); text-decoration: none; }
    .footer-links a:hover { color: var(--c-primary); }

    /* --- ANIMATIONS --- */
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    @keyframes float { 0% { transform: translateY(0); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0); } }
    
    /* --- RESPONSIVE --- */
    @media (max-width: 1024px) { .grid-3, .grid-4 { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 768px) { .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; } .nav-list { display: none; } h1 { font-size: 2.5rem; } }
</style>
"""

# ------------------------------------------------------------------------------
# 2. JAVASCRIPT ENGINE (CANVAS & LOGIC)
# ------------------------------------------------------------------------------
JS_CORE = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
<script>
    // --- PARTICLE NETWORK ANIMATION ---
    window.addEventListener('DOMContentLoaded', () => {
        const canvas = document.getElementById('bg-canvas');
        if(canvas) {
            const ctx = canvas.getContext('2d');
            let width, height, particles;
            
            function resize() {
                width = canvas.width = window.innerWidth;
                height = canvas.height = window.innerHeight;
                initParticles();
            }
            
            function initParticles() {
                particles = [];
                const cnt = Math.floor(width * height / 15000);
                for(let i=0; i<cnt; i++) {
                    particles.push({
                        x: Math.random() * width,
                        y: Math.random() * height,
                        vx: (Math.random() - 0.5) * 0.5,
                        vy: (Math.random() - 0.5) * 0.5,
                        size: Math.random() * 2
                    });
                }
            }
            
            function animate() {
                ctx.clearRect(0, 0, width, height);
                ctx.fillStyle = '#6366f1';
                
                for(let i=0; i<particles.length; i++) {
                    let p = particles[i];
                    p.x += p.vx;
                    p.y += p.vy;
                    
                    if(p.x < 0 || p.x > width) p.vx *= -1;
                    if(p.y < 0 || p.y > height) p.vy *= -1;
                    
                    ctx.globalAlpha = 0.5;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                    ctx.fill();
                    
                    for(let j=i+1; j<particles.length; j++) {
                        let p2 = particles[j];
                        let dx = p.x - p2.x;
                        let dy = p.y - p2.y;
                        let dist = Math.sqrt(dx*dx + dy*dy);
                        
                        if(dist < 100) {
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(99, 102, 241, ${1 - dist/100})`;
                            ctx.lineWidth = 0.5;
                            ctx.moveTo(p.x, p.y);
                            ctx.lineTo(p2.x, p2.y);
                            ctx.stroke();
                        }
                    }
                }
                requestAnimationFrame(animate);
            }
            
            window.addEventListener('resize', resize);
            resize();
            animate();
        }
    });

    // --- DASHBOARD LOGIC ---
    let stressMode = false;

    function addLog(message, type='INFO') {
        const terminal = document.getElementById('terminal');
        if(!terminal) return;
        
        const time = new Date().toLocaleTimeString();
        const color = type === 'ALERT' ? '#ef4444' : (type === 'WARN' ? '#f59e0b' : '#10b981');
        
        const row = document.createElement('div');
        row.className = 'log-entry';
        row.innerHTML = `<span class="timestamp">[${time}]</span> <span style="color:${color}; font-weight:bold">${type}</span> <span>${message}</span>`;
        
        terminal.appendChild(row);
        terminal.scrollTop = terminal.scrollHeight;
    }

    function updateDashboard() {
        fetch('/api/stats')
            .then(r => r.json())
            .then(data => {
                // CPU
                document.getElementById('cpu-val').innerText = data.cpu + '%';
                const cpuFill = document.getElementById('cpu-fill');
                cpuFill.style.width = data.cpu + '%';
                cpuFill.style.backgroundColor = data.cpu > 80 ? '#ef4444' : '#6366f1';
                
                // RAM
                document.getElementById('ram-val').innerText = data.ram + '%';
                document.getElementById('ram-fill').style.width = data.ram + '%';
                
                // Random Logs
                if(Math.random() > 0.8) {
                    const msgs = [
                        "Packet tracing enabled on eth0",
                        "Garbage collection started",
                        "Health check: Service operational",
                        "Database query executed (12ms)",
                        "Load balancer routing updated"
                    ];
                    addLog(msgs[Math.floor(Math.random() * msgs.length)]);
                }
            })
            .catch(e => console.error("Connection lost"));
    }

    function toggleStress() {
        stressMode = !stressMode;
        const btn = document.getElementById('btn-stress');
        
        if(stressMode) {
            fetch('/api/stress/on');
            btn.innerHTML = '<i class="fas fa-stop"></i> DURDUR';
            btn.style.backgroundColor = 'rgba(239, 68, 68, 0.2)';
            btn.style.color = '#ef4444';
            btn.style.borderColor = '#ef4444';
            addLog("STRESS TEST INITIATED - CPU SPIKING", "WARN");
        } else {
            fetch('/api/stress/off');
            btn.innerHTML = '<i class="fas fa-fire"></i> STRES TESTİ';
            btn.style.backgroundColor = '';
            btn.style.color = '';
            btn.style.borderColor = '';
            addLog("Stress test stopped. Systems normalizing.", "INFO");
        }
    }

    function triggerKill() {
        if(confirm("UYARI: Bu işlem konteyneri çökertecek. Docker'ın yeniden başlatmasını izlemek istiyor musunuz?")) {
            addLog("KILL SIGNAL RECEIVED - SYSTEM SHUTDOWN IMMINENT", "ALERT");
            fetch('/api/kill');
            setTimeout(() => {
                document.body.innerHTML = `
                    <div style="height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; background:#000; color:#ef4444;">
                        <i class="fas fa-triangle-exclamation fa-5x mb-5"></i>
                        <h1>SYSTEM FAILURE (500)</h1>
                        <p style="margin-top:20px">Docker Orchestrator is rebooting the container...</p>
                        <div class="loader" style="margin-top:30px"></div>
                    </div>
                `;
                setTimeout(() => location.reload(), 6000);
            }, 1500);
        }
    }

    // Auto-update dashboard if element exists
    if(document.getElementById('dashboard-root')) {
        setInterval(updateDashboard, 1000);
    }
</script>
"""

# ------------------------------------------------------------------------------
# 3. HTML COMPONENTS (PYTHON FUNCTIONS FOR SAFETY)
# ------------------------------------------------------------------------------

def get_navbar(active_page):
    links = [
        ('home', '/', 'Ana Sayfa'),
        ('solutions', '/solutions', 'Çözümler'),
        ('pricing', '/pricing', 'Fiyatlandırma'),
        ('blog', '/blog', 'Blog'),
    ]
    
    menu_items = ""
    for id, url, name in links:
        active_class = 'nav-link-active' if id == active_page else ''
        menu_items += f'<li><a href="{url}" class="nav-link {active_class}">{name}</a></li>'

    return f"""
    <nav class="navbar">
        <div class="container nav-inner">
            <a href="/" class="brand">
                <i class="fas fa-cloud-bolt"></i> NIMBUS<span style="color:var(--c-primary)">AI</span>
            </a>
            <ul class="nav-list">
                {menu_items}
            </ul>
            <div class="flex gap-4">
                <a href="/login" class="btn btn-outline" style="padding:0.5rem 1rem; font-size:0.85rem">Giriş</a>
                <a href="/status" class="btn btn-primary" style="padding:0.5rem 1rem; font-size:0.85rem">
                    <i class="fas fa-gauge-high"></i> Panel
                </a>
            </div>
        </div>
    </nav>
    """

def get_footer():
    return f"""
    <footer>
        <div class="container">
            <div class="grid grid-4 gap-8">
                <div class="footer-col">
                    <h4 style="margin-bottom:1rem">NIMBUS AI</h4>
                    <p style="font-size:0.9rem">Geleceğin bulut altyapısı. Otonom, güvenli ve ölçeklenebilir.</p>
                </div>
                <div class="footer-col">
                    <h4 style="margin-bottom:1rem">Ürün</h4>
                    <div class="footer-links">
                        <a href="#">Compute Engine</a>
                        <a href="#">Kubernetes</a>
                        <a href="#">Serverless</a>
                    </div>
                </div>
                <div class="footer-col">
                    <h4 style="margin-bottom:1rem">Kaynaklar</h4>
                    <div class="footer-links">
                        <a href="#">Dokümantasyon</a>
                        <a href="#">API Referansı</a>
                        <a href="#">Durum Sayfası</a>
                    </div>
                </div>
                <div class="footer-col">
                    <h4 style="margin-bottom:1rem">Yasal</h4>
                    <div class="footer-links">
                        <a href="#">Gizlilik</a>
                        <a href="#">Şartlar</a>
                    </div>
                </div>
            </div>
            <div style="border-top:1px solid #333; margin-top:3rem; padding-top:2rem; text-align:center; font-size:0.85rem; color:#555">
                &copy; 2025 Nimbus AI Inc. | Container ID: {os.uname()[1]}
            </div>
        </div>
    </footer>
    """

def render_layout(title, content, active_page='home'):
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | Nimbus AI</title>
        {CSS_CORE}
        {JS_CORE}
    </head>
    <body>
        {get_navbar(active_page)}
        {content}
        {get_footer()}
    </body>
    </html>
    """

# ------------------------------------------------------------------------------
# 4. PAGE CONTENTS
# ------------------------------------------------------------------------------

def page_home():
    return """
    <div style="position:relative; height:100vh; min-height:800px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
        <canvas id="bg-canvas"></canvas>
        <div class="container text-center" style="position:relative; z-index:2">
            <div class="badge badge-live" style="margin:0 auto 2rem auto;">
                <div class="dot"></div> v5.0 ENTERPRISE YAYINDA
            </div>
            <h1 style="max-width:900px; margin:0 auto 1.5rem auto;">
                Altyapınızı <span class="text-gradient-primary">Yapay Zeka</span> ile Ölçeklendirin.
            </h1>
            <p style="margin:0 auto 2.5rem auto; font-size:1.25rem;">
                Nimbus AI, mikroservislerinizi otonom olarak yöneten, kendi kendini iyileştiren (self-healing) yeni nesil bulut platformudur.
            </p>
            <div class="flex justify-center gap-4">
                <a href="/status" class="btn btn-primary" style="font-size:1.1rem; padding:1rem 2rem;">
                    <i class="fas fa-rocket"></i> Canlı Demo
                </a>
                <a href="/solutions" class="btn btn-outline" style="font-size:1.1rem; padding:1rem 2rem;">
                    Çözümleri Keşfet
                </a>
            </div>
            
            <div style="margin-top:5rem; opacity:0.5; display:flex; justify-content:center; gap:4rem;">
                <i class="fab fa-aws fa-3x"></i>
                <i class="fab fa-google fa-3x"></i>
                <i class="fab fa-docker fa-3x"></i>
                <i class="fab fa-linux fa-3x"></i>
            </div>
        </div>
    </div>

    <section class="py-20" style="background:var(--c-surface)">
        <div class="container">
            <div class="text-center mb-5">
                <h2>Teknoloji Stack</h2>
                <p style="margin:0 auto;">Modern işletmeler için tasarlanmış kurumsal özellikler.</p>
            </div>
            <div class="grid grid-3">
                <div class="card">
                    <div style="width:50px; height:50px; background:rgba(99,102,241,0.1); border-radius:12px; display:flex; align-items:center; justify-content:center; margin-bottom:1.5rem; color:var(--c-primary)">
                        <i class="fas fa-bolt fa-lg"></i>
                    </div>
                    <h3>Yüksek Performans</h3>
                    <p>Optimize edilmiş Docker çekirdeği ile %300 daha hızlı başlatma süreleri.</p>
                </div>
                <div class="card">
                    <div style="width:50px; height:50px; background:rgba(16,185,129,0.1); border-radius:12px; display:flex; align-items:center; justify-content:center; margin-bottom:1.5rem; color:var(--c-success)">
                        <i class="fas fa-shield-alt fa-lg"></i>
                    </div>
                    <h3>Askeri Güvenlik</h3>
                    <p>İzole edilmiş VLAN ağları ve otomatik tehdit algılama sistemi.</p>
                </div>
                <div class="card">
                    <div style="width:50px; height:50px; background:rgba(239,68,68,0.1); border-radius:12px; display:flex; align-items:center; justify-content:center; margin-bottom:1.5rem; color:var(--c-danger)">
                        <i class="fas fa-heartbeat fa-lg"></i>
                    </div>
                    <h3>Self-Healing</h3>
                    <p>Sistem çökmelerini algılar ve insan müdahalesi olmadan onarır.</p>
                </div>
            </div>
        </div>
    </section>
    """

def page_solutions():
    return """
    <div class="container py-20 mt-10">
        <div class="text-center mb-5">
            <h1>Kurumsal <span class="text-gradient-primary">Çözümler</span></h1>
            <p style="margin:0 auto">İşletmenizi büyütmek için ihtiyacınız olan tüm araçlar.</p>
        </div>
        
        <div class="grid grid-2">
            <div class="card flex" style="align-items:start; gap:2rem;">
                <i class="fas fa-microchip fa-3x" style="color:var(--c-primary)"></i>
                <div>
                    <h3>AI Compute</h3>
                    <p>Model eğitimi için GPU destekli sanal makineler.</p>
                    <ul style="list-style:none; margin-top:1rem; color:var(--c-text-muted)">
                        <li><i class="fas fa-check" style="color:var(--c-success); margin-right:0.5rem"></i> NVIDIA A100 Desteği</li>
                        <li><i class="fas fa-check" style="color:var(--c-success); margin-right:0.5rem"></i> Jupyter Notebook</li>
                    </ul>
                </div>
            </div>
            <div class="card flex" style="align-items:start; gap:2rem;">
                <i class="fas fa-network-wired fa-3x" style="color:var(--c-accent)"></i>
                <div>
                    <h3>Kubernetes</h3>
                    <p>Tam yönetilen K8s kümeleri. Master node yönetimi bizde.</p>
                    <ul style="list-style:none; margin-top:1rem; color:var(--c-text-muted)">
                        <li><i class="fas fa-check" style="color:var(--c-success); margin-right:0.5rem"></i> Otomatik Ölçekleme</li>
                        <li><i class="fas fa-check" style="color:var(--c-success); margin-right:0.5rem"></i> Multi-Zone</li>
                    </ul>
                </div>
            </div>
             <div class="card flex" style="align-items:start; gap:2rem;">
                <i class="fas fa-database fa-3x" style="color:#f59e0b"></i>
                <div>
                    <h3>Managed DB</h3>
                    <p>PostgreSQL ve Redis veritabanları. Yedekleme dahil.</p>
                </div>
            </div>
             <div class="card flex" style="align-items:start; gap:2rem;">
                <i class="fas fa-globe fa-3x" style="color:var(--c-danger)"></i>
                <div>
                    <h3>Global CDN</h3>
                    <p>İçeriğinizi dünyaya milisaniyeler içinde dağıtın.</p>
                </div>
            </div>
        </div>
    </div>
    """

def page_pricing():
    return """
    <div class="container py-20 mt-10">
        <div class="text-center mb-5">
            <h1>Esnek <span class="text-gradient-primary">Fiyatlandırma</span></h1>
            <p style="margin:0 auto">Gizli ücret yok. İstediğiniz zaman iptal edin.</p>
        </div>
        
        <div class="grid grid-3">
            <div class="card text-center">
                <h3>Developer</h3>
                <div style="font-size:3rem; font-weight:800; margin:1rem 0">$29<span style="font-size:1rem; color:#666">/ay</span></div>
                <ul style="text-align:left; list-style:none; margin:2rem 0; gap:1rem; display:grid;">
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> 2 vCPU</li>
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> 4 GB RAM</li>
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> 50 GB SSD</li>
                </ul>
                <a href="#" class="btn btn-outline w-full">Seç</a>
            </div>
            
            <div class="card text-center" style="border-color:var(--c-primary); transform:scale(1.05); box-shadow:var(--shadow)">
                <div class="badge badge-live" style="margin:0 auto 1rem auto; background:var(--c-primary); color:white">EN POPÜLER</div>
                <h3>Business</h3>
                <div style="font-size:3rem; font-weight:800; margin:1rem 0">$99<span style="font-size:1rem; color:#666">/ay</span></div>
                <ul style="text-align:left; list-style:none; margin:2rem 0; gap:1rem; display:grid;">
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> 8 vCPU</li>
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> 32 GB RAM</li>
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> 500 GB NVMe</li>
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> 7/24 Destek</li>
                </ul>
                <a href="#" class="btn btn-primary w-full">Hemen Başla</a>
            </div>
            
            <div class="card text-center">
                <h3>Enterprise</h3>
                <div style="font-size:3rem; font-weight:800; margin:1rem 0">Özel</div>
                <ul style="text-align:left; list-style:none; margin:2rem 0; gap:1rem; display:grid;">
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> Dedicated Host</li>
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> Sınırsız Trafik</li>
                    <li><i class="fas fa-check" style="color:var(--c-success)"></i> Özel SLA</li>
                </ul>
                <a href="#" class="btn btn-outline w-full">İletişime Geç</a>
            </div>
        </div>
    </div>
    """

def page_status():
    return """
    <div id="dashboard-root" class="container py-20 mt-10">
        <div class="flex justify-between" style="margin-bottom:2rem; align-items:end;">
            <div>
                <h1>Sistem <span class="text-gradient-primary">Paneli</span></h1>
                <p>Gerçek zamanlı sunucu metrikleri ve yönetim araçları.</p>
            </div>
            <div class="badge badge-live" style="font-size:1rem; padding:0.5rem 1rem;">
                <div class="dot"></div> OPERATIONAL
            </div>
        </div>

        <div class="grid grid-3">
            <div class="card">
                <div class="flex justify-between">
                    <span class="metric-label">CPU LOAD</span>
                    <i class="fas fa-microchip" style="color:var(--c-primary)"></i>
                </div>
                <div class="metric-value" id="cpu-val">0%</div>
                <div class="progress-bar"><div class="progress-fill" id="cpu-fill" style="width:0%"></div></div>
                
                <button onclick="toggleStress()" id="btn-stress" class="btn btn-outline w-full" style="margin-top:2rem">
                    <i class="fas fa-fire"></i> STRES TESTİ
                </button>
            </div>

            <div class="card">
                <div class="flex justify-between">
                    <span class="metric-label">MEMORY</span>
                    <i class="fas fa-memory" style="color:var(--c-accent)"></i>
                </div>
                <div class="metric-value" id="ram-val">0%</div>
                <div class="progress-bar"><div class="progress-fill" id="ram-fill" style="width:0%; background:var(--c-accent)"></div></div>
                <p style="margin-top:2rem; font-size:0.85rem">Allocated: Docker Dynamic Memory</p>
            </div>

            <div class="card" style="border-color:rgba(239,68,68,0.3)">
                <div class="flex justify-between">
                    <span class="metric-label" style="color:var(--c-danger)">TEHLİKELİ BÖLGE</span>
                    <i class="fas fa-biohazard" style="color:var(--c-danger)"></i>
                </div>
                <p style="margin:1.5rem 0; font-size:0.95rem">
                    Sistemin "Self-Healing" (otomatik iyileşme) özelliğini test etmek için konteyneri zorla kapatın.
                </p>
                <button onclick="triggerKill()" class="btn btn-danger w-full">
                    <i class="fas fa-power-off"></i> SİSTEMİ ÇÖKERT
                </button>
            </div>
        </div>

        <div class="grid mt-10">
            <div class="card" style="padding:0; overflow:hidden; background:#000;">
                <div style="padding:1rem 2rem; border-bottom:1px solid #333; display:flex; justify-content:space-between;">
                    <span style="font-family:'JetBrains Mono'; font-weight:bold; color:#fff">Live System Logs</span>
                    <div class="flex gap-4">
                        <div style="width:10px; height:10px; border-radius:50%; background:#ef4444"></div>
                        <div style="width:10px; height:10px; border-radius:50%; background:#f59e0b"></div>
                        <div style="width:10px; height:10px; border-radius:50%; background:#10b981"></div>
                    </div>
                </div>
                <div id="terminal" class="terminal-box">
                    <div class="log-entry"><span class="timestamp">[BOOT]</span> <span style="color:#10b981">INFO</span> System initialized successfully...</div>
                    <div class="log-entry"><span class="timestamp">[NET]</span> <span style="color:#10b981">INFO</span> Connected to Nimbus Core Network...</div>
                </div>
            </div>
        </div>
    </div>
    """

# ------------------------------------------------------------------------------
# 5. ROUTES & API
# ------------------------------------------------------------------------------

@app.route('/')
def home():
    return render_layout("Ana Sayfa", page_home(), 'home')

@app.route('/solutions')
def solutions():
    return render_layout("Çözümler", page_solutions(), 'solutions')

@app.route('/pricing')
def pricing():
    return render_layout("Fiyatlandırma", page_pricing(), 'pricing')

@app.route('/blog')
def blog():
    # Simple placeholder for blog
    content = """
    <div class="container py-20 mt-10 text-center">
        <h1>Blog</h1>
        <p>Çok yakında...</p>
        <a href="/" class="btn btn-primary mt-10">Ana Sayfaya Dön</a>
    </div>
    """
    return render_layout("Blog", content, 'blog')

@app.route('/login')
def login():
    content = """
    <div class="container" style="height:80vh; display:flex; align-items:center; justify-content:center;">
        <div class="card" style="width:100%; max-width:400px; text-align:center;">
            <h2 class="mb-5">Giriş Yap</h2>
            <input type="email" placeholder="E-Posta" style="width:100%; padding:1rem; margin-bottom:1rem; background:#000; border:1px solid #333; color:#fff; border-radius:8px;">
            <input type="password" placeholder="Şifre" style="width:100%; padding:1rem; margin-bottom:2rem; background:#000; border:1px solid #333; color:#fff; border-radius:8px;">
            <a href="/status" class="btn btn-primary w-full">Giriş</a>
        </div>
    </div>
    """
    return render_layout("Giriş", content)

@app.route('/status')
def status():
    return render_layout("Sistem Paneli", page_status())

# --- API ---
@app.route('/api/stats')
def api_stats():
    return jsonify({
        'cpu': psutil.cpu_percent(interval=None),
        'ram': psutil.virtual_memory().percent
    })

@app.route('/api/stress/<action>')
def api_stress(action):
    global stress_mode
    if action == 'on':
        stress_mode = True
        threading.Thread(target=run_stress_load).start()
    else:
        stress_mode = False
    return "OK"

def run_stress_load():
    while stress_mode:
        # Generate CPU load
        [x**2 for x in range(10000)]

@app.route('/api/kill')
def api_kill():
    def kill_process():
        time.sleep(2)
        os._exit(1)
    threading.Thread(target=kill_process).start()
    return "Killed"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
