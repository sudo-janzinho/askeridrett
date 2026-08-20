# -*- coding: utf-8 -*-
"""
Fyller i officiella e-postadresser som aktiv (synlig) e-post på undersidorna.

Mappning:
- GUI SK (alla grenar) -> dagligleder@guisk.no
- Nesøya IL (alla grenar utom skolekorps) -> post@nesoyail.no
- Asker Skiklubb (alla grenar) -> kontoret@asker-skiklubb.no
- Hyggen IF (allidrett, fotball, ski) -> hyggenif@gmail.com

Ersätter den bortkommenterade E-post-raden med en aktiv officiell e-post.
Lämnar Kontakt (namn) och Tlf (telefon) bortkommenterade.
"""
import glob
import re

# Mappning: filnamnsprefix -> officiell e-post
MAPPING = [
    ('gui-sk-', 'dagligleder@guisk.no'),
    ('nesoya-il-', 'post@nesoyail.no'),
    ('asker-skiklubb-', 'kontoret@asker-skiklubb.no'),
    ('hyggen-if-', 'hyggenif@gmail.com'),
]

# Undantag: filer som INTE ska få officiell e-post
EXCLUDE = [
    'nesoya-skolekorps.html',   # skolekorps, inte idrettslag
    'hyggen-speidergruppe.html',  # speidergruppe, inte idrettslag
]

def get_official_email(filename):
    for prefix, email in MAPPING:
        if filename.startswith(prefix):
            return email
    return None

def process_file(path):
    filename = path.split('/')[-1].split('\\')[-1]
    if filename in EXCLUDE:
        return False

    official = get_official_email(filename)
    if official is None:
        return False

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # Hitta den bortkommenterade E-post-raden och ersätt med aktiv officiell e-post.
    # Mönstret är: <!-- <div><strong>E-post:</strong> ... </div> -->
    # Vi ersätter hela kommentaren med en aktiv e-post-rad.
    pattern = re.compile(
        r'<!--\s*<div><strong>E-post:</strong>.*?</div>\s*-->',
        re.DOTALL
    )

    new_epost = (
        '<div><strong>E-post:</strong> '
        f'<a href="mailto:{official}">{official}</a></div>'
    )

    # Ersätt första förekomsten av den kommenterade E-post-raden
    html, count = pattern.subn(new_epost, html, count=1)

    if count > 0 and html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def main():
    files = [f for f in glob.glob('*.html') if f != 'index.html']
    changed = 0
    for f in files:
        if process_file(f):
            changed += 1
    print(f"Bearbetade {len(files)} undersidor, fyllde i officiell e-post i {changed}.")

if __name__ == '__main__':
    main()
