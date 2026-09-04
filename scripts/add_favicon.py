import os

html_path = '/content/dikili/repo/index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Check if favicon already exists to avoid duplicates
if '<link rel="icon"' not in html:
    # Insert it right after <head>
    favicon_tag = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>📜</text></svg>">\n'
    html = html.replace('<head>', '<head>\n    ' + favicon_tag, 1)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Favicon added.")
else:
    print("Favicon already exists.")
