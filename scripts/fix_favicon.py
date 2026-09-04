html_path = '/content/dikili/repo/index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Remove the old inline SVG favicon
html = re.sub(r'<link rel="icon" href="data:image/svg\+xml.*?>\n?', '', html)

# Add standard link
if '<link rel="icon" href="favicon.svg"' not in html:
    html = html.replace('<head>', '<head>\n    <link rel="icon" href="favicon.svg" type="image/svg+xml">', 1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
