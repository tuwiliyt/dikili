import re

gen_path = '/content/dikili/repo/scripts/generate_final_app.py'
with open(gen_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for badge-jabu
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
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
"""
if '.badge-jabu' not in content:
    content = content.replace('</style>', css_jabu + '\n    </style>')

# 2. Add JS replacement in renderSair function
js_jabu = """
                // Highlight Jabu markers
                let formattedText = block.text.replace(/\\(Jābu\\)\\.?/gi, '<span class="badge-jabu">Jābu</span>');
                formattedText = formattedText.replace(/\\(jābu\\)\\.?/gi, '<span class="badge-jabu">Jābu</span>');
                // Replace newlines with <br> after escaping? The current code does textContent so it escapes HTML!
"""

# Wait! The current JS uses textContent for blocks to avoid XSS!
# Let's check how the JS renders blocks.
