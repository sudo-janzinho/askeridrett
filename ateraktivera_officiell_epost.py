# -*- coding: utf-8 -*-
"""
Återaktiverar officiella (rollbaserade) e-postadresser på undersidorna,
men lämnar personliga e-postadresser bortkommenterade.

Officiell = prefix som post, styret, leder, info, admin, dagligleder, kasserer,
sekretar, sekreter, styreleder, medlem, medlemskap, okonomi, regnskap, fotball,
handball, ski, cup, fiske, jakt, hund, vakt, utleie, sponsor, proshop, material,
lopper, sosialkomiteen, arbeidsutvalget, korpsleder, kulturskole, kulturskolen,
asker, askerturlag, btasker, hovedstyret, fotballstyret, juniorkontoret,
allidrett, badminton, bordtennis, friidrett, innebandy, langrenn, hopp, bandy,
barneidrett, volleyball, skoyting, sykkel, tennis, hvalstad, gellumgrendehus,
hei, info, kontor, kontakt, medlemskap, medlem.

Personlig = gratis-domäner (gmail, hotmail, outlook, yahoo, online, live, icloud)
eller personnamn@företag (förnamn.efternamn@ eller förnamn@).

Körs från askeridrett-deploy-mappen.
"""
import glob
import re

# Officiella prefix (rollbaserade, anonyma)
OFFICIAL_PREFIXES = {
    'post', 'styret', 'leder', 'ledere', 'info', 'admin', 'dagligleder',
    'kasserer', 'sekretar', 'sekreter', 'styreleder', 'medlem', 'medlemskap',
    'okonomi', 'regnskap', 'fotball', 'handball', 'ski', 'cup', 'fiske',
    'jakt', 'hund', 'vakt', 'utleie', 'sponsor', 'proshop', 'material',
    'lopper', 'sosialkomiteen', 'arbeidsutvalget', 'korpsleder', 'kulturskole',
    'kulturskolen', 'asker', 'askerturlag', 'btasker', 'hovedstyret',
    'fotballstyret', 'juniorkontoret', 'allidrett', 'badminton', 'bordtennis',
    'friidrett', 'innebandy', 'langrenn', 'hopp', 'bandy', 'barneidrett',
    'volleyball', 'skoyting', 'sykkel', 'tennis', 'hvalstad', 'gellumgrendehus',
    'hei', 'kontor', 'kontakt', 'medlemskap', 'medlem',
}

# Gratis/personliga domäner att alltid exkludera
PERSONAL_DOMAINS = {
    'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'yahoo.no',
    'live.no', 'live.com', 'icloud.com', 'me.com', 'online.no',
}

def is_official_email(email):
    """Returnerar True om e-postadressen är officiell/rollbaserad."""
    email = email.strip().lower()
    if '@' not in email:
        return False
    local, domain = email.split('@', 1)
    local = local.strip()
    domain = domain.strip().lower()

    # Exkludera gratis/personliga domäner
    if domain in PERSONAL_DOMAINS:
        return False

    # Behåll om prefixet är officiellt
    if local in OFFICIAL_PREFIXES:
        return True

    return False

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # Hitta bortkommenterade E-post-block:
    # <!-- <div><strong>E-post:</strong> ... </div> -->
    # Vi matchar hela kommentaren och kollar e-postadressen inuti.
    pattern = re.compile(
        r'<!--\s*(<div><strong>E-post:</strong>.*?</div>)\s*-->',
        re.DOTALL
    )

    def repl(m):
        inner = m.group(1)
        # Extrahera alla e-postadresser i blocket
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', inner)
        # Om ALLA e-postadresser är officiella, återaktivera
        if emails and all(is_official_email(e) for e in emails):
            return inner  # ta bort kommentarerna
        else:
            return m.group(0)  # behåll kommenterad

    html = pattern.sub(repl, html)

    if html != original:
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
    print(f"Bearbetade {len(files)} undersidor, återaktiverade officiell e-post i {changed}.")

if __name__ == '__main__':
    main()
