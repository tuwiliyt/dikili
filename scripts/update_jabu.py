import re

gen_path = '/content/dikili/repo/scripts/generate_final_app.py'
with open(gen_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS
css_jabu = """
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
"""
if '.badge-jabu' not in content:
    content = content.replace('</style>', css_jabu + '\n    </style>')

# 2. Add JS regex replacement
js_jabu = """
        // Highlight Jabu markers
        text = text.replace(/\\(Jābu\\)\\.?/gi, '<span class="badge-jabu">Jābu</span>');
        text = text.replace(/\\(jābu\\)\\.?/gi, '<span class="badge-jabu">Jābu</span>');
        
        let cssClass = 'block-text';
"""
content = content.replace("let cssClass = 'block-text';", js_jabu)

with open(gen_path, 'w', encoding='utf-8') as f:
    f.write(content)

