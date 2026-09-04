import os
import re

gen_path = '/content/dikili/repo/scripts/generate_final_app.py'

with open(gen_path, 'r', encoding='utf-8') as f:
    content = f.read()

css_nav = """
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px dashed var(--border-color);
        }
        .nav-btn {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.95rem;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
            max-width: 48%;
        }
        .nav-btn:hover {
            background-color: var(--border-color);
        }
        .nav-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .nav-btn-label {
            font-size: 0.75rem;
            color: var(--text-dim);
            display: block;
            margin-bottom: 2px;
        }
        .nav-btn-title {
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .nav-btn-content {
            display: flex;
            flex-direction: column;
            text-align: left;
            overflow: hidden;
        }
        .nav-btn.next .nav-btn-content {
            text-align: right;
        }
"""

html_nav = """
            <div id="nav-buttons-container" class="nav-buttons" style="display: none;">
                <button id="btn-prev-sair" class="nav-btn prev" onclick="goToSair(-1)">
                    <span>←</span>
                    <div class="nav-btn-content">
                        <span class="nav-btn-label">Sebelumnya</span>
                        <span id="label-prev-sair" class="nav-btn-title">Sair</span>
                    </div>
                </button>
                <button id="btn-next-sair" class="nav-btn next" onclick="goToSair(1)">
                    <div class="nav-btn-content">
                        <span class="nav-btn-label">Selanjutnya</span>
                        <span id="label-next-sair" class="nav-btn-title">Sair</span>
                    </div>
                    <span>→</span>
                </button>
            </div>
"""

js_nav = """
        // Navigation buttons logic
        let currentSairIndex = 0;
        
        function updateNavButtons(index) {
            currentSairIndex = index;
            const container = document.getElementById('nav-buttons-container');
            const btnPrev = document.getElementById('btn-prev-sair');
            const btnNext = document.getElementById('btn-next-sair');
            const labelPrev = document.getElementById('label-prev-sair');
            const labelNext = document.getElementById('label-next-sair');
            
            if (activeTab !== 'naskah') {
                container.style.display = 'none';
                return;
            }
            
            container.style.display = 'flex';
            
            if (index > 0) {
                btnPrev.style.visibility = 'visible';
                labelPrev.textContent = dikiliData.sairs[index - 1].name;
            } else {
                btnPrev.style.visibility = 'hidden';
            }
            
            if (index < dikiliData.sairs.length - 1) {
                btnNext.style.visibility = 'visible';
                labelNext.textContent = dikiliData.sairs[index + 1].name;
            } else {
                btnNext.style.visibility = 'hidden';
            }
        }
        
        function goToSair(direction) {
            const newIndex = currentSairIndex + direction;
            if (newIndex >= 0 && newIndex < dikiliData.sairs.length) {
                const select = document.getElementById('sair-select');
                select.value = newIndex;
                renderSair(newIndex);
                window.scrollTo({top: 0, behavior: 'smooth'});
            }
        }
"""

if 'nav-buttons' not in content:
    content = content.replace('</style>', css_nav + '\n    </style>')
    content = content.replace('        </main>\\n    </div>', html_nav + '        </main>\\n    </div>')
    content = content.replace('function renderSair(index) {', js_nav + '\n        function renderSair(index) {')
    content = content.replace('contentDiv.innerHTML = html;', 'contentDiv.innerHTML = html;\\n            updateNavButtons(parseInt(index));')
    content = content.replace('document.getElementById(\\\'nav-kearifan\\\').classList.add(\\\'active\\\');\\n                renderKearifanLokal();', 'document.getElementById(\\\'nav-kearifan\\\').classList.add(\\\'active\\\');\\n                renderKearifanLokal();\\n                document.getElementById(\\\'nav-buttons-container\\\').style.display = \\\'none\\\';')
    content = content.replace('document.getElementById(\\\'nav-info\\\').classList.add(\\\'active\\\');\\n                renderInfo();', 'document.getElementById(\\\'nav-info\\\').classList.add(\\\'active\\\');\\n                renderInfo();\\n                document.getElementById(\\\'nav-buttons-container\\\').style.display = \\\'none\\\';')
    
    with open(gen_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated generate_final_app.py")
