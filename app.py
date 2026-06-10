<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EduGuardian</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #0f172a; color: #f8fafc; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(14px); border: 1px solid rgba(255,255,255,0.05); }
        .animate-in { animation: fadeIn 0.8s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="min-h-screen p-8">
    <div class="max-w-6xl mx-auto">
        <nav class="flex justify-between items-center mb-12">
            <div class="flex items-center space-x-3">
                <div class="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center font-bold text-2xl shadow-lg shadow-indigo-500/20">E</div>
                <h1 class="text-3xl font-extrabold tracking-tighter">EduGuardian <span class="text-indigo-400 font-light italic">Pro</span></h1>
            </div>
            <a href="/admin" class="px-6 py-2 bg-white/10 hover:bg-white/20 rounded-full text-xs font-bold uppercase tracking-widest border border-white/10 transition-all">📊 Admin Dashboard</a>
        </nav>

        <main class="grid grid-cols-1 lg:grid-cols-12 gap-10">
            <div class="lg:col-span-5">
                <div class="glass p-10 rounded-[3rem] shadow-2xl">
                    <h2 class="text-2xl font-black mb-8 text-indigo-100">Student Pulse</h2>
                    <form id="pulseForm" class="space-y-6">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-[10px] font-bold text-slate-500 uppercase">Attendance %</label>
                                <input type="number" id="att" required class="w-full p-4 rounded-2xl bg-slate-800 border-none outline-none focus:ring-2 focus:ring-indigo-500" placeholder="85">
                            </div>
                            <div>
                                <label class="text-[10px] font-bold text-slate-500 uppercase">Avg Marks</label>
                                <input type="number" id="marks" required class="w-full p-4 rounded-2xl bg-slate-800 border-none outline-none focus:ring-2 focus:ring-indigo-500" placeholder="70">
                            </div>
                        </div>
                        <div>
                            <label class="text-[10px] font-bold text-slate-500 uppercase">Wellness (1-5)</label>
                            <input type="range" id="well" min="1" max="5" step="0.5" class="w-full accent-indigo-500">
                        </div>
                        <div>
                            <label class="text-[10px] font-bold text-slate-500 uppercase">Travel Distance (KM)</label>
                            <input type="number" id="travel" required class="w-full p-4 rounded-2xl bg-slate-800 border-none outline-none focus:ring-2 focus:ring-indigo-500" placeholder="5">
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <select id="inc" class="p-4 rounded-2xl bg-slate-800 border-none text-sm font-bold">
                                <option value="1">Low Income</option>
                                <option value="2" selected>Mid Income</option>
                                <option value="3">High Income</option>
                            </select>
                            <select id="dig" class="p-4 rounded-2xl bg-slate-800 border-none text-sm font-bold">
                                <option value="1">Internet: Yes</option>
                                <option value="0">Internet: No</option>
                            </select>
                        </div>
                        <button type="submit" class="w-full py-5 bg-indigo-600 text-white font-black rounded-2xl hover:bg-indigo-700 shadow-xl shadow-indigo-500/20 uppercase tracking-widest text-sm italic">
                            Analyze Resilience
                        </button>
                    </form>

                    <div class="mt-6 p-4 bg-white/5 rounded-2xl border border-white/10">
                        <h4 class="text-[10px] font-black uppercase text-indigo-400 mb-2">Why this data?</h4>
                        <ul class="text-[10px] space-y-1 text-slate-400 italic">
                            <li>• <strong>Travel:</strong> Long commutes increase physical fatigue and safety risks.</li>
                            <li>• <strong>Income:</strong> Financial strain creates high opportunity costs for families.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-7">
                <div id="emptyView" class="h-full border-2 border-dashed border-white/5 rounded-[3.5rem] flex flex-col items-center justify-center text-slate-500 opacity-50">
                    <p class="text-lg font-bold">Awaiting Student Pulse Data...</p>
                </div>
                
                <div id="resultView" class="hidden space-y-6 animate-in">
                    <div id="riskCard" class="p-10 rounded-[3.5rem] shadow-2xl transition-all duration-700 border-l-[16px]">
                        <div class="flex justify-between items-start mb-8">
                            <div>
                                <p class="text-[10px] font-black uppercase text-white/40 tracking-widest mb-2">Risk Probability</p>
                                <h3 id="probText" class="text-8xl font-black italic tracking-tighter">0%</h3>
                            </div>
                            <span id="levelLabel" class="px-5 py-2 rounded-full font-black text-[10px] uppercase border">STABLE</span>
                        </div>

                        <div class="bg-indigo-950/40 p-8 rounded-[2.5rem] border border-indigo-500/20 mb-8">
                            <div class="flex items-center space-x-3 mb-3">
                                <span class="text-2xl">🤖</span>
                                <h4 class="text-[10px] font-black uppercase text-indigo-400">AI Support Mentor</h4>
                            </div>
                            <p id="counselorText" class="text-sm italic text-indigo-100"></p>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div class="bg-black/20 p-6 rounded-[2.5rem]">
                                <h4 class="text-[10px] font-black uppercase text-center opacity-30 mb-4">6-Month Risk Projection</h4>
                                <div class="h-40"><canvas id="timelineChart"></canvas></div>
                            </div>
                            <div class="flex flex-col justify-center space-y-4">
                                <div class="bg-white/5 p-4 rounded-2xl border border-white/5">
                                    <p class="text-[10px] font-black opacity-40 uppercase mb-1">Primary Driver</p>
                                    <p id="driverText" class="font-black italic text-xl uppercase text-indigo-400"></p>
                                </div>
                                <div class="bg-emerald-500/10 p-4 rounded-2xl border border-emerald-500/20">
                                    <p class="text-[10px] font-black opacity-40 uppercase mb-1">Actionable Impact</p>
                                    <p id="impactText" class="font-black italic text-sm text-emerald-400">Processing interventions...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        let timelineChart;
    
        document.getElementById('pulseForm').onsubmit = async (e) => {
            e.preventDefault();
    
            // Collect pipeline payloads securely
            const payload = {
                attendance: parseFloat(document.getElementById('att').value),
                marks: parseFloat(document.getElementById('marks').value),
                wellness: parseFloat(document.getElementById('well').value),
                digital: parseInt(document.getElementById('dig').value),
                travel: parseFloat(document.getElementById('travel').value),
                income: parseInt(document.getElementById('inc').value),
                scholarship: 0
            };
    
            try {
                const response = await fetch('/analyze_pro', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
    
                if (!response.ok) throw new Error('Backend Engine Communication Error');
                const data = await response.json();
    
                // Unhide the charts/analytics board 
                document.getElementById('emptyView').classList.add('hidden');
                document.getElementById('resultView').classList.remove('hidden');
    
                // Map metrics to elements dynamically
                const probValue = data.analysis.probability;
                document.getElementById('probText').innerText = (probValue * 100).toFixed(1) + '%';
                document.getElementById('levelLabel').innerText = data.analysis.level;
                
                document.getElementById('counselorText').innerText = data.counselor_voice;
                document.getElementById('driverText').innerText = data.analysis.top_driver;
                document.getElementById('impactText').innerText = data.actionable_impact; // Dynamic assignment fix
    
                // Handle theme variations according to security severity states
                const card = document.getElementById('riskCard');
                const level = data.analysis.level;
                let color = '#10b981'; // Green fallback
                
                if (level === 'CRITICAL') {
                    color = '#f43f5e';
                    card.className = "p-10 rounded-[3.5rem] shadow-2xl transition-all border-l-[16px] bg-rose-950/40 border-rose-500 text-rose-100";
                } else if (level === 'ELEVATED') {
                    color = '#f59e0b';
                    card.className = "p-10 rounded-[3.5rem] shadow-2xl transition-all border-l-[16px] bg-amber-950/40 border-amber-500 text-amber-100";
                } else {
                    card.className = "p-10 rounded-[3.5rem] shadow-2xl transition-all border-l-[16px] bg-emerald-950/40 border-emerald-500 text-emerald-100";
                }
    
                // Destroy old instance to avoid hover flicker bugs
                if (timelineChart) timelineChart.destroy();
                timelineChart = new Chart(document.getElementById('timelineChart'), {
                    type: 'line',
                    data: {
                        labels: ['Now', 'M1', 'M2', 'M3', 'M4', 'M5'],
                        datasets: [{
                            data: data.analysis.timeline,
                            borderColor: color,
                            borderWidth: 4,
                            tension: 0.4,
                            fill: false,
                            pointRadius: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { display: false, min: 0, max: 1 },
                            x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.2)', font: { size: 9, weight: 'bold' } } }
                        }
                    }
                });
    
            } catch (error) {
                console.error("Pipeline Error:", error);
                alert("Error connecting to AI Engine. Check if your backend app.py server is up and running.");
            }
        };
    </script>
</body>
</html>
