<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Rank Tracker - Pro Controller</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at top right, #f8fafc, #eff6ff);
            color: #1e293b;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.04);
        }

        /* Fixed Domain Input Layout */
        .input-wrapper {
            display: flex;
            align-items: center;
            background: white;
            border: 1.5px solid #e2e8f0;
            border-radius: 1rem;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .input-wrapper:focus-within {
            border-color: #4f46e5;
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        }

        .prefix {
            background: #f8fafc;
            padding: 0 1rem;
            height: 52px;
            display: flex;
            align-items: center;
            color: #94a3b8;
            font-size: 0.875rem;
            font-weight: 600;
            border-right: 1px solid #e2e8f0;
            white-space: nowrap;
            user-select: none;
        }

        .field-input {
            flex: 1;
            padding: 0.875rem 1rem;
            border: none;
            outline: none;
            font-size: 0.95rem;
            font-weight: 500;
            width: 100%;
        }

        .btn-base {
            padding: 0.875rem 1.5rem;
            border-radius: 1rem;
            font-weight: 700;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            cursor: pointer;
        }

        .btn-primary {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
        }

        .btn-danger { background: #ef4444; color: white; }
        .btn-secondary { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

        .status-badge {
            padding: 0.35rem 1rem;
            border-radius: 2rem;
            font-size: 0.75rem;
            font-weight: 700;
        }

        textarea::-webkit-scrollbar { width: 6px; }
        textarea::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    </style>
</head>
<body class="min-h-screen p-4 md:p-12">

    <div class="max-w-6xl mx-auto space-y-10">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <!-- Sidebar: Configuration -->
            <div class="lg:col-span-4 space-y-6">
                <div class="glass-card p-8 rounded-[2rem]">
                    <h2 class="text-xl font-extrabold mb-8 flex items-center gap-3 text-slate-900 tracking-tight">
                        <span class="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center">
                            <i class="fas fa-cog"></i>
                        </span>
                        Tracker Setup
                    </h2>
                    
                    <div class="space-y-6">
                        <!-- API Key -->
                        <div>
                            <label class="block text-[11px] font-extrabold text-slate-400 mb-2 uppercase tracking-widest">Gemini API Key</label>
                            <input type="password" id="apiKey" placeholder="Enter API Key..." class="w-full px-5 py-3.5 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none text-sm bg-white font-medium">
                        </div>

                        <!-- Target Domain -->
                        <div>
                            <label class="block text-[11px] font-extrabold text-slate-400 mb-2 uppercase tracking-widest">Target Domain</label>
                            <div class="input-wrapper">
                                <div class="prefix">https://</div>
                                <input type="text" id="targetDomain" placeholder="example.com" class="field-input">
                            </div>
                        </div>

                        <!-- Location -->
                        <div>
                            <label class="block text-[11px] font-extrabold text-slate-400 mb-2 uppercase tracking-widest">Search Location</label>
                            <input list="locations-list" type="text" id="location" placeholder="e.g. Sacramento, California" class="w-full px-5 py-3.5 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none text-sm font-medium">
                            <datalist id="locations-list">
                                <option value="Sacramento, California"><option value="Los Angeles, California">
                                <option value="California, US"><option value="Tehran, Iran">
                            </datalist>
                        </div>

                        <!-- Keywords -->
                        <div>
                            <label class="block text-[11px] font-extrabold text-slate-400 mb-2 uppercase tracking-widest">Keywords (One per line)</label>
                            <textarea id="keywords" rows="5" placeholder="seo services&#10;dental clinic..." class="w-full px-5 py-3.5 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none text-sm resize-none font-medium"></textarea>
                        </div>

                        <!-- Controls -->
                        <div class="flex flex-col gap-3">
                            <button id="startCheck" class="btn-base btn-primary w-full shadow-indigo-200">
                                <i class="fas fa-play"></i> Run Analysis
                            </button>
                            <button id="stopCheck" class="btn-base btn-danger w-full hidden">
                                <i class="fas fa-stop"></i> Stop Process
                            </button>
                        </div>
                    </div>
                </div>

                <div id="progressContainer" class="hidden glass-card p-7 rounded-[2rem] border-l-4 border-indigo-600">
                    <div class="flex justify-between items-center mb-4 text-[11px] font-extrabold text-slate-500">
                        <span>SCAN PROGRESS</span>
                        <span id="progressText" class="text-indigo-600">0%</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                        <div id="progressBar" class="bg-indigo-600 h-full transition-all duration-500" style="width: 0%"></div>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-8">
                <div class="glass-card rounded-[2.5rem] overflow-hidden min-h-[650px] flex flex-col">
                    <div class="p-8 border-b border-slate-100 flex justify-between items-center bg-white/40">
                        <h2 class="text-xl font-extrabold text-slate-900 tracking-tight">Live SERP Results</h2>
                        <div class="flex gap-2">
                            <button id="resetTool" class="btn-base btn-secondary px-4 py-2.5 text-xs">Reset</button>
                            <button id="copyResults" class="btn-base btn-secondary px-4 py-2.5 text-xs">Copy</button>
                        </div>
                    </div>

                    <div class="flex-grow overflow-x-auto">
                        <table class="w-full text-left">
                            <thead>
                                <tr class="text-[10px] uppercase tracking-widest text-slate-400 font-black bg-slate-50/50">
                                    <th class="px-8 py-5">Keyword</th>
                                    <th class="px-8 py-5">Position</th>
                                    <th class="px-8 py-5">Target URL</th>
                                    <th class="px-8 py-5 text-center">Status</th>
                                </tr>
                            </thead>
                            <tbody id="resultsBody" class="divide-y divide-slate-50">
                                <tr id="placeholderRow">
                                    <td colspan="4" class="py-40 text-center text-slate-300 italic">Configure settings and click "Run Analysis".</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="msgBox" class="fixed bottom-8 right-8 transform translate-x-32 opacity-0 transition-all duration-500 bg-slate-900 text-white px-7 py-5 rounded-[1.5rem] shadow-2xl z-50 flex items-center gap-4">
        <span id="msgContent" class="text-sm font-bold"></span>
    </div>

    <script>
        const modelName = "gemini-1.5-flash"; // Using stable model name
        let isAborted = false;

        const startBtn = document.getElementById('startCheck');
        const stopBtn = document.getElementById('stopCheck');
        const resetBtn = document.getElementById('resetTool');
        const resultsBody = document.getElementById('resultsBody');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const progressContainer = document.getElementById('progressContainer');
        const placeholderRow = document.getElementById('placeholderRow');
        const domainInput = document.getElementById('targetDomain');
        const apiKeyInput = document.getElementById('apiKey');

        // Load saved domain and API key
        window.addEventListener('DOMContentLoaded', () => {
            const savedDomain = localStorage.getItem('seo_tracker_domain');
            const savedApiKey = localStorage.getItem('seo_tracker_api_key');
            if (savedDomain) domainInput.value = savedDomain;
            if (savedApiKey) apiKeyInput.value = savedApiKey;
        });

        function showMessage(text) {
            const msgBox = document.getElementById('msgBox');
            document.getElementById('msgContent').innerText = text;
            msgBox.classList.remove('translate-x-32', 'opacity-0');
            msgBox.classList.add('translate-x-0', 'opacity-100');
            setTimeout(() => {
                msgBox.classList.remove('translate-x-0', 'opacity-100');
                msgBox.classList.add('translate-x-32', 'opacity-0');
            }, 4000);
        }

        async function callGemini(keyword, domain, location, customKey) {
            // Using a strictly formatted URL to avoid 404
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${customKey}`;
            
            const payload = {
                contents: [{ parts: [{ text: `Find the organic rank (1-100) of the domain "${domain}" for the keyword "${keyword}" in "${location}" using Google Search results.` }] }],
                systemInstruction: { parts: [{ text: "You are an SEO Rank Checker. Search Google and return JSON ONLY: {\"rank\": number|null, \"url\": \"string\", \"found\": boolean}. If not in top 100, rank is null." }] },
                tools: [{ "google_search": {} }],
                generationConfig: { responseMimeType: "application/json" }
            };

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    const errorDetails = await response.json();
                    console.error("Google API Response Error:", errorDetails);
                    // No more hardcoded region assumptions, just passing the real error.
                    throw new Error(errorDetails.error?.message || `API Error ${response.status}`);
                }

                const result = await response.json();
                const contentText = result.candidates[0].content.parts[0].text;
                return JSON.parse(contentText);
            } catch (error) {
                console.error("Fetch Exception:", error);
                throw error;
            }
        }

        stopBtn.addEventListener('click', () => {
            isAborted = true;
            stopBtn.classList.add('opacity-50');
            stopBtn.innerText = "Aborting...";
        });

        resetBtn.addEventListener('click', () => {
            if (!confirm("Clear all results?")) return;
            resultsBody.innerHTML = '';
            resultsBody.appendChild(placeholderRow);
            placeholderRow.classList.remove('hidden');
            progressBar.style.width = '0%';
            progressText.innerText = '0%';
            progressContainer.classList.add('hidden');
        });

        startBtn.addEventListener('click', async () => {
            const domain = domainInput.value.trim();
            const location = document.getElementById('location').value.trim();
            const customKey = apiKeyInput.value.trim();
            const keywordList = document.getElementById('keywords').value.split('\n').filter(k => k.trim() !== "");

            if (!customKey || !domain || !keywordList.length) {
                showMessage("Please fill all fields.");
                return;
            }

            localStorage.setItem('seo_tracker_domain', domain);
            localStorage.setItem('seo_tracker_api_key', customKey);

            placeholderRow.classList.add('hidden');
            progressContainer.classList.remove('hidden');
            startBtn.classList.add('hidden');
            stopBtn.classList.remove('hidden', 'opacity-50');
            stopBtn.innerText = "Stop Process";
            
            isAborted = false;
            let completed = 0;

            for (const keyword of keywordList) {
                if (isAborted) break;

                const row = document.createElement('tr');
                row.className = "bg-white animate-pulse";
                row.innerHTML = `
                    <td class="px-8 py-6 font-bold">${keyword}</td>
                    <td colspan="2" class="px-8 py-6 italic text-slate-400 text-xs">Scanning SERP...</td>
                    <td class="px-8 py-6 text-center"><i class="fas fa-spinner fa-spin text-indigo-500"></i></td>
                `;
                resultsBody.appendChild(row);

                try {
                    const data = await callGemini(keyword, domain, location, customKey);
                    
                    if (isAborted) { row.remove(); break; }

                    row.classList.remove('animate-pulse');
                    const rankDisplay = data.rank ? `Rank #${data.rank}` : "Out of Top 100";
                    const rankClass = data.rank && data.rank <= 10 ? 'bg-emerald-100 text-emerald-700' : (data.rank ? 'bg-indigo-100 text-indigo-700' : 'bg-slate-100 text-slate-500');
                    const displayUrl = data.url ? data.url.replace(/^https?:\/\//, '').substring(0, 35) + '...' : '---';

                    row.innerHTML = `
                        <td class="px-8 py-6 text-slate-900 font-bold">${keyword}</td>
                        <td class="px-8 py-6"><span class="status-badge ${rankClass}">${rankDisplay}</span></td>
                        <td class="px-8 py-6 text-xs text-indigo-600 font-bold"><a href="${data.url || '#'}" target="_blank" class="hover:underline">${displayUrl}</a></td>
                        <td class="px-8 py-6 text-center"><i class="fas ${data.found ? 'fa-check-circle text-emerald-500' : 'fa-times-circle text-slate-200'} text-lg"></i></td>
                    `;
                } catch (err) {
                    row.innerHTML = `<td class="px-8 py-6 font-bold">${keyword}</td><td colspan="3" class="px-8 py-6 text-red-500 text-[10px] font-black uppercase tracking-widest">Error: ${err.message}</td>`;
                }

                completed++;
                const percentage = Math.round((completed / keywordList.length) * 100);
                progressBar.style.width = `${percentage}%`;
                progressText.innerText = `${percentage}%`;
            }

            startBtn.classList.remove('hidden');
            stopBtn.classList.add('hidden');
            showMessage(isAborted ? "Process stopped." : "Analysis completed.");
        });

        document.getElementById('copyResults').addEventListener('click', () => {
            const rows = Array.from(resultsBody.querySelectorAll('tr')).map(tr => Array.from(tr.querySelectorAll('td')).map(td => td.innerText).join('\t')).join('\n');
            const el = document.createElement('textarea');
            el.value = rows;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            showMessage("Results copied!");
        });
    </script>
</body>
</html>
