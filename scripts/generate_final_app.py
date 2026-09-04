#!/usr/bin/env python3
"""
Generate the final Dikili web application.
Focuses on manuscript presentation (Sair structure), Arabic text quality,
and removes all references to PDF/book page numbers.
"""

import json

def main():
    with open('/content/dikili/repo/dikili_final.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    json_str = json.dumps(data, ensure_ascii=False)
    json_str = json_str.replace('</script>', '<\\/script>').replace('<!--', '<\\!--')
    
    template = r'''<!DOCTYPE html>
<html lang="id">
<head>\n    <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Naskah Dikili Gorontalo</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0c1117;
      --surface: #161b22;
      --surface-card: #1c2129;
      --surface-hover: #21272e;
      --border: #30363d;
      --text: #e6edf3;
      --text-muted: #8b949e;
      --text-dim: #484f58;
      --primary: #10b981;
      --primary-light: #34d399;
      --gold: #f59e0b;
      --gold-light: #fbbf24;
      --blue: #3b82f6;
      --font-arabic: 'Amiri', 'Traditional Arabic', 'Noto Naskh Arabic', serif;
      --font-ui: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --arabic-size: 28px;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: var(--font-ui);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    .app-header {
      background: linear-gradient(135deg, #064e3b 0%, #0c1117 100%);
      padding: 16px;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .app-title { font-size: 18px; font-weight: 900; color: var(--primary-light); }
    .app-subtitle { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
    
    .nav-bar {
      display: flex;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      overflow-x: auto;
      scrollbar-width: none;
    }
    .nav-item {
      padding: 12px 16px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      background: none;
      border: none;
      border-bottom: 2px solid transparent;
      cursor: pointer;
      white-space: nowrap;
    }
    .nav-item.active {
      color: var(--primary-light);
      border-bottom-color: var(--primary);
    }

    .toolbar {
      display: flex;
      gap: 8px;
      padding: 10px 16px;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
    }
    .tool-btn {
      padding: 4px 12px;
      background: var(--surface-card);
      color: var(--text-muted);
      border: 1px solid var(--border);
      border-radius: 4px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
    }
    .tool-btn:hover { background: var(--surface-hover); }

    .view-section { display: none; padding: 16px; max-width: 800px; margin: 0 auto; }
    .view-section.active { display: block; }
    
    .section-title { font-size: 18px; font-weight: 900; margin-bottom: 8px; color: var(--text); }
    .section-desc { font-size: 13px; color: var(--text-muted); margin-bottom: 20px; }

    /* Manuscript display styles */
    .sair-selector {
      width: 100%;
      padding: 10px;
      margin-bottom: 20px;
      background: var(--surface-card);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 14px;
      font-weight: 700;
    }

    .content-block {
      margin-bottom: 16px;
      padding: 12px 16px;
      border-radius: 8px;
      background: var(--surface-card);
      border: 1px solid var(--border);
    }
    
    .block-arabic {
      font-family: var(--font-arabic);
      font-size: var(--arabic-size);
      line-height: 2.2;
      color: var(--gold-light);
      text-align: right;
      direction: rtl;
      padding: 16px;
      background: rgba(245,158,11,0.05);
      border-left: 3px solid var(--gold);
    }
    
    .block-transliteration {
      font-size: 13px;
      font-style: italic;
      color: var(--primary-light);
      border-left: 3px solid var(--primary);
    }
    
    .block-translation {
      font-size: 13px;
      color: var(--text);
      border-left: 3px solid var(--blue);
      background: rgba(59,130,246,0.05);
    }
    
    .block-text {
      font-size: 13px;
      color: var(--text);
    }
    
    .block-footnote {
      font-size: 11px;
      color: var(--text-muted);
      border-top: 1px dashed var(--border);
      padding-top: 8px;
      background: transparent;
      border: none;
      border-top: 1px dashed var(--border);
      border-radius: 0;
    }

    /* Cards */
    .card {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 12px;
    }
    .card-title {
      font-size: 15px;
      font-weight: 800;
      color: var(--primary-light);
      margin-bottom: 8px;
    }
    .card-content {
      font-size: 13px;
      color: var(--text);
      line-height: 1.6;
    }

    /* Light Theme */
    body.light {
      --bg: #f6f8fa;
      --surface: #ffffff;
      --surface-card: #ffffff;
      --surface-hover: #f0f2f5;
      --border: #d0d7de;
      --text: #1f2328;
      --text-muted: #656d76;
      --gold-light: #b45309;
    }
  
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

    
        .badge-jabu {
            display: inline-block;
            background-color: rgba(234, 179, 8, 0.15);
            color: #eab308;
            border: 1px solid #ca8a04;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            font-style: normal;
            margin: 0 4px;
            vertical-align: middle;
            letter-spacing: 0.5px;
        }

    </style>
</head>
<body>
  <header class="app-header">
    <div class="app-title">📜 Naskah Dikili Gorontalo</div>
    <div class="app-subtitle" id="app-subtitle">Memuat data...</div>
  </header>

  <div class="toolbar">
    <button class="tool-btn" id="btn-font-dec">A−</button>
    <button class="tool-btn" id="btn-font-inc">A+</button>
    <button class="tool-btn" id="btn-theme">🌓 Tema</button>
  </div>

  <nav class="nav-bar">
    <button class="nav-item active" data-tab="tab-naskah">📖 Baca Naskah</button>
    <button class="nav-item" data-tab="tab-info">ℹ️ Info Naskah</button>
    <button class="nav-item" data-tab="tab-kearifan">🌿 Kearifan Lokal</button>
  </nav>

  <!-- BACA NASKAH -->
  <section id="tab-naskah" class="view-section active">
    <select id="sair-select" class="sair-selector"></select>
    <div id="naskah-content"></div>
  </section>

  <!-- INFO NASKAH -->
  <section id="tab-info" class="view-section">
    <h2 class="section-title">Informasi Naskah</h2>
    <p class="section-desc">Keterangan mengenai manuskrip yang menjadi landasan aplikasi ini.</p>
    <div id="info-content"></div>
  </section>

  <!-- KEARIFAN LOKAL -->
  <section id="tab-kearifan" class="view-section">
    <h2 class="section-title">Kearifan Lokal</h2>
    <p class="section-desc">Kearifan lokal yang terkandung dalam naskah Dikili.</p>
    <div id="kearifan-content"></div>
  </section>

  <script>
    const DATA = /*__DATA__*/null;
    let currentSairId = null;

    function init() {
      document.getElementById('app-subtitle').innerHTML = 
        `Suntingan Teks berdasarkan <strong>${DATA.info.manuscript_base}</strong>`;
      
      renderSairSelector();
      renderInfo();
      renderKearifan();
      setupEvents();
      
      if (DATA.sairs.length > 0) {
        loadSair(DATA.sairs[0].id);
      }
    }

    function renderSairSelector() {
      const select = document.getElementById('sair-select');
      DATA.sairs.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = s.name;
        select.appendChild(opt);
      });
    }

    function loadSair(id) {
      currentSairId = id;
      document.getElementById('sair-select').value = id;
      const sair = DATA.sairs.find(s => s.id.toString() === id.toString());
      if (!sair) return;

      let html = `<h3 style="font-size:18px; font-weight:800; margin-bottom:16px; color:var(--text); text-align:center;">${sair.name}</h3>`;
      
      sair.blocks.forEach(b => {
        // Clean up text
        let text = b.text.trim();
        // Remove trailing quotes if empty line
        if (text === '"' || text === "'") return;
        
        // Remove page numbers that might have slipped through parser
        text = text.replace(/^\d+\s*$/, '');
        if (!text) return;

        
        // Highlight Jabu markers
        text = text.replace(/\(Jābu\)\.?/gi, '<span class="badge-jabu">Jābu</span>');
        text = text.replace(/\(jābu\)\.?/gi, '<span class="badge-jabu">Jābu</span>');
        
        let cssClass = 'block-text';

        if (b.type === 'arabic') cssClass = 'block-arabic';
        if (b.type === 'transliteration') cssClass = 'block-transliteration';
        if (b.type === 'translation') cssClass = 'block-translation';
        if (b.type === 'footnote') cssClass = 'block-footnote';

        html += `<div class="content-block ${cssClass}">${text.replace(/\n/g, '<br>')}</div>`;
      });

      document.getElementById('naskah-content').innerHTML = html;
      window.scrollTo(0, 0);
    }

    function renderInfo() {
      let html = `
        <div class="card">
          <div class="card-title">Penyusun Edisi Kritis</div>
          <div class="card-content">
            <strong>${DATA.info.authors}</strong><br>
            ${DATA.info.institution} (${DATA.info.year})<br>
            <em>${DATA.info.source || "Kearifan Lokal dalam Naskah Dikili"}</em>
          </div>
        </div>
        <div class="card">
          <div class="card-title">Naskah Landasan</div>
          <div class="card-content">${DATA.info.manuscript_base}</div>
        </div>
        <h3 style="margin: 20px 0 10px; font-size:16px;">Perbandingan Manuskrip</h3>
      `;

      DATA.manuscripts.forEach(m => {
        const isBase = m.is_base;
        html += `
          <div class="card" style="${isBase ? 'border-left: 3px solid var(--gold);' : ''}">
            <div class="card-title">Naskah ${m.code} ${isBase ? ' (Naskah Landasan)' : ''}</div>
            <div class="card-content">
              <strong>Pemilik:</strong> ${m.owner}<br>
              <strong>Fisik:</strong> ${m.pages} halaman, ${m.size}, ${m.lines_per_page}<br>
              <strong>Kolofon:</strong> ${m.colophon}<br>
              <strong>Kertas & Tinta:</strong> ${m.paper}, ${m.ink}<br>
              <strong>Aksara:</strong> ${m.script}<br>
              <strong>Isi:</strong> ${m.content}<br>
            </div>
            ${isBase && m.base_rationale ? `
              <div style="margin-top:10px; padding:10px; background:rgba(245,158,11,0.1); border-radius:6px; font-size:12px;">
                <strong>Alasan Pemilihan:</strong>
                <ul style="margin:4px 0 0 16px;">
                  ${m.base_rationale.map(r => `<li>${r}</li>`).join('')}
                </ul>
              </div>
            ` : ''}
          </div>
        `;
      });
      document.getElementById('info-content').innerHTML = html;
    }

    function renderKearifan() {
      let html = '';
      DATA.kearifan_lokal.forEach(k => {
        html += `
          <div class="card" style="border-left: 3px solid var(--primary);">
            <div class="card-title">${k.name}</div>
            <div class="card-content">${k.description}</div>
          </div>
        `;
      });
      document.getElementById('kearifan-content').innerHTML = html;
    }

    function setupEvents() {
      // Tabs
      document.querySelectorAll('.nav-item').forEach(btn => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
          document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
          btn.classList.add('active');
          document.getElementById(btn.getAttribute('data-tab')).classList.add('active');
          window.scrollTo(0, 0);
        });
      });

      // Selector
      document.getElementById('sair-select').addEventListener('change', (e) => {
        loadSair(e.target.value);
      });

      // Fonts
      let arSize = 28;
      document.getElementById('btn-font-inc').addEventListener('click', () => {
        arSize = Math.min(arSize + 2, 44);
        document.documentElement.style.setProperty('--arabic-size', arSize + 'px');
      });
      document.getElementById('btn-font-dec').addEventListener('click', () => {
        arSize = Math.max(arSize - 2, 20);
        document.documentElement.style.setProperty('--arabic-size', arSize + 'px');
      });

      // Theme
      document.getElementById('btn-theme').addEventListener('click', () => {
        document.body.classList.toggle('light');
      });
    }

    document.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
'''
    
    final_html = template.replace('/*__DATA__*/null', json_str)
    
    output_path = '/content/dikili/repo/index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Generated {output_path}")

if __name__ == '__main__':
    main()
