#!/usr/bin/env python3
"""
Genererer sitemap.xml for askeridrett.no
Basert på alle .html-filer i repo-roten (unntatt index.html og hjelpefiler).
"""
import os
import datetime

BASE_URL = "https://askeridrett.no"
REPO_DIR = os.path.dirname(os.path.abspath(__file__))

# Filer som IKKE skal være egne URL-er i sitemap
SKIP = {"index.html", "klubber-uten-epost.html"}

def main():
    files = sorted(f for f in os.listdir(REPO_DIR)
                   if f.endswith(".html") and f not in SKIP)

    # Siste endret dato fra filsystemet (brukes som lastmod)
    def lastmod(fname):
        mtime = os.path.getmtime(os.path.join(REPO_DIR, fname))
        return datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    # Startsiden
    lines.append('  <url>')
    lines.append(f'    <loc>{BASE_URL}/</loc>')
    lines.append(f'    <lastmod>{lastmod("index.html")}</lastmod>')
    lines.append('  </url>')
    # Alle undersider
    for f in files:
        lines.append('  <url>')
        lines.append(f'    <loc>{BASE_URL}/{f}</loc>')
        lines.append(f'    <lastmod>{lastmod(f)}</lastmod>')
        lines.append('  </url>')
    lines.append('</urlset>')

    out = os.path.join(REPO_DIR, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"Generert {out} med {len(files) + 1} URL-er")

if __name__ == "__main__":
    main()
