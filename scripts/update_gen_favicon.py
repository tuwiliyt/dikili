gen_path = '/content/dikili/repo/scripts/generate_final_app.py'

with open(gen_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Remove the old inline SVG if it somehow got in there (it didn't, but just in case)
content = re.sub(r'<link rel=\\\"icon\\\" href=\\\"data:image/svg\+xml.*?>\\n?', '', content)

if 'favicon.svg' not in content:
    content = content.replace('<head>', '<head>\\n    <link rel="icon" href="favicon.svg" type="image/svg+xml">', 1)

with open(gen_path, 'w', encoding='utf-8') as f:
    f.write(content)
