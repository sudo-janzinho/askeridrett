# -*- coding: utf-8 -*-
"""
Kommenterar bort privatpersoners kontaktinfo (Kontakt, Tlf, E-post) i alla
klubb-undersidor, men behåller Nettside och Adresse.

Använder HTML-kommentarer <!-- ... --> så att det är lätt att återaktivera
när klubben bekräftar att de vill ha sin kontakt publicerad.

Körs från askeridrett-deploy-mappen.
"""
import os
import re
import glob

# Mönster för de tre fält vi vill kommentera bort.
# Varje fält är ett <div><strong>X:</strong> ...</div>
# Vi matchar hela <div>...</div> för respektive fält.

def comment_out_field(html, field_label):
    """Kommenterar bort ett helt <div><strong>FIELD:</strong>...</div>-block."""
    # Matcha <div><strong>Kontakt:</strong> ... </div>
    # Fältet kan innehålla nästlade <a>...</a> men inga nästlade <div>.
    pattern = re.compile(
        r'<div><strong>' + re.escape(field_label) + r':</strong>.*?</div>',
        re.DOTALL
    )
    def repl(m):
        return '<!-- ' + m.group(0) + ' -->'
    return pattern.sub(repl, html)

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # Kommentera bort Kontakt, Tlf, E-post (i den ordningen)
    for label in ['Kontakt', 'Tlf', 'E-post']:
        html = comment_out_field(html, label)

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def main():
    files = glob.glob('*.html')
    files = [f for f in files if f != 'index.html']
    changed = 0
    for f in files:
        if process_file(f):
            changed += 1
    print(f"Bearbetade {len(files)} undersidor, ändrade {changed}.")

if __name__ == '__main__':
    main()
