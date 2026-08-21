#!/usr/bin/env python3
"""
Legger til meta description på alle klubb-undersider i askeridrett.no-repoet.

Status 2026-08-21: 162/162 har unik <title>, men 0/162 har meta description.
Dette skriptet genererer en unik, SEO-vennlig meta description per underside
basert på klubbnavn + aktivitet, og setter den inn i <head>.

Kjør:  python legg_til_meta_description.py
"""
import os
import re
import html

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SKIP = {"index.html", "klubber-uten-epost.html"}

# Aktivitetstype per fil (manuell mapping for de viktigste; fallback = generisk)
# Nøkkel: filnavn uten .html → aktivitetsbeskrivelse på norsk
AKTIVITET = {
    "asker-golfklubb": "golf",
    "asker-svommeklubb": "svømming",
    "asker-skiklubb-alpint": "alpint",
    "asker-skiklubb-langrenn": "langrenn",
    "asker-skiklubb-fotball": "fotball",
    "asker-skiklubb-handball": "håndball",
    "asker-skiklubb-friidrett": "friidrett",
    "asker-skiklubb-orientering": "orientering",
    "asker-skiklubb-skiskyting": "skiskyting",
    "asker-skiklubb-kajakk": "kajakk",
    "asker-skiklubb-hopp": "skihopp",
    "asker-skiklubb-bandy": "bandy",
    "asker-skiklubb-barneidrett": "barneidrett",
    "asker-skiklubb-volleyball": "volleyball",
    "asker-skiklubb-snowboard-og-freestyle": "snowboard og freestyle",
    "asker-tennisklubb": "tennis",
    "asker-badmintonklubb": "badminton",
    "asker-innebandyklubb": "innebandy",
    "asker-judoklubb": "judo",
    "asker-karateklubb": "karate",
    "asker-taekwon-do-klubb": "taekwon-do",
    "asker-fekteklubb": "fekting",
    "asker-seilforening": "seiling",
    "asker-skoyteklubb": "skøyter",
    "asker-skytterlag": "skyting",
    "asker-cricket-klubb": "cricket",
    "asker-motorsportklubb": "motorsport",
    "asker-musikkorps": "musikkorps",
    "asker-drill": "drill",
    "asker-rideklubb": "ridning",
    "asker-schakklubb": "sjakk",
    "asker-kulturskole": "kulturskole",
    "asker-kulturskole-dans": "dans",
    "asker-kulturskole-musikk": "musikk",
    "asker-kulturskole-teater": "teater",
    "asker-kulturskole-korps": "korps",
    "asker-kulturskole-visuell-kunst": "visuell kunst",
    "asker-kulturskole-for-de-yngste": "kulturskole for de yngste",
    "il-ros-fotball": "fotball",
    "il-ros-handball": "håndball",
    "il-ros-basket": "basketball",
    "il-ros-badminton": "badminton",
    "il-ros-friidrett": "friidrett",
    "il-ros-svomming": "svømming",
    "il-ros-sykkel": "sykling",
    "il-ros-tennis": "tennis",
    "il-ros-turn": "turn",
    "il-ros-volleyball": "volleyball",
    "il-ros-boksing": "boksing",
    "il-ros-innebandy": "innebandy",
    "il-ros-skigruppa": "ski",
    "il-ros-allidrett": "allidrett",
    "holmen-if-fotball": "fotball",
    "holmen-if-handball": "håndball",
    "holmen-if-langrenn": "langrenn",
    "holmen-tennisklubb": "tennis",
    "holmen-klatreklubb": "klatring",
    "holmen-skolekorps": "skolekorps",
    "holmen-tropp-og-turn": "turn",
    "holmen-hockey": "ishockey",
    "holmen-kfuk-kfum-speidere": "speiding",
    "nesoya-il-fotball": "fotball",
    "nesoya-il-handball": "håndball",
    "nesoya-il-ishockey": "ishockey",
    "nesoya-il-seiling": "seiling",
    "nesoya-il-tennis": "tennis",
    "nesoya-il-allidrett": "allidrett",
    "nesoya-skolekorps": "skolekorps",
    "billingstad-if-fotball": "fotball",
    "billingstad-if-allidrett": "allidrett",
    "bodalen-if-fotball-og-allidrett": "fotball og allidrett",
    "bodalen-if-ski": "ski",
    "bodalen-if-skiskyting": "skiskyting",
    "dikemark-if-fotball": "fotball",
    "dikemark-if-langrenn": "langrenn",
    "dikemark-rideklubb": "ridning",
    "saetre-if-graabein-fotball": "fotball",
    "saetre-if-graabein-handball": "håndball",
    "saetre-if-graabein-allidrett": "allidrett",
    "slemmestad-if-fotball": "fotball",
    "slemmestad-if-handball": "håndball",
    "slemmestad-if-innebandy": "innebandy",
    "slemmestad-if-allidrett": "allidrett",
    "tofte-fremad-if-fotball": "fotball",
    "tofte-fremad-if-handball": "håndball",
    "tofte-fremad-if-allidrett": "allidrett",
    "tofte-triatlon": "triatlon",
    "hyggen-if-fotball": "fotball",
    "hyggen-if-allidrett": "allidrett",
    "hyggen-if-ski": "ski",
    "huringen-if-fotball": "fotball",
    "huringen-if-judo": "judo",
    "royken-seilforening": "seiling",
    "royken-taekwon-do-klubb": "taekwon-do",
    "royken-speidergruppe": "speiding",
    "roykenmila": "løp",
    "royken-hopp": "skihopp",
    "royken-o-lag": "orientering",
    "royken-og-aros-jeger-og-fisk": "jakt og fiske",
    "royken-og-hurum-klatreklubb": "klatring",
    "royken-teatergruppe": "teater",
    "hurum-seilforening": "seiling",
    "hurum-sjakklubb": "sjakk",
    "hurum-sportsskytterklubb": "skyting",
    "hurum-orienteringslag": "orientering",
    "sondre-hurum-jff": "jakt og fiske",
    "nordre-hurum-jff": "jakt og fiske",
    "kjekstad-golfklubb": "golf",
    "konglungen-rideklubb": "ridning",
    "konglungen-tennisklubb": "tennis",
    "steinseth-rideklubb": "ridning",
    "hvalstad-il-fotball": "fotball",
    "hvalstad-il-buegruppe": "bueskyting",
    "dnt-asker-turlag": "turliv",
    "dnt-asker-turlag-barnas-turlag": "barnas turliv",
    "dnt-asker-turlag-ung": "ungdoms turliv",
    "barnas-turlag-royken-og-hurum": "barnas turliv",
    "asker-rode-kors-hjelpekorps": "hjelpekorps",
    "asker-rode-kors-besoksvenn": "besøksvenn",
    "crossing-borders": "kultur",
    "dansesonen-dans": "dans",
    "ukm-asker": "kultur",
    "ec-play": "e-sport",
    "frisk-asker-fotball": "fotball",
    "frisk-asker-ishockey-jr": "ishockey",
    "amasone-fk": "fotball",
    "akk-asker-kunstlopklubb": "kunstløp",
    "arnestad-skolekorps": "skolekorps",
    "asker-1-og-1-skougum-speidergruppe": "speiding",
    "asker-aliens-herrer-og-damer": "fotball",
    "asker-ck-landeveissykling": "landeveissykling",
    "asker-ck-terrengsykling": "terrengsykling",
    "asker-jeger-og-fiskerforening": "jakt og fiske",
    "asker-kfuk-kfum-kulturskole": "kulturskole",
    "asker-kfuk-kfum-speidere": "speiding",
    "asker-ogamp-baerum-kickboxingklubb": "kickboxing",
    "asker-turnforening-turn-og-tropp": "turn",
    "blakstad-kfuk-kfum-speidere": "speiding",
    "bondi-ogamp-vettre-skolekorps": "skolekorps",
    "borgen-skolekorps": "skolekorps",
    "gui-sk-fotball": "fotball",
    "gui-sk-karate": "karate",
    "heggedal-og-blakstad-skolekorps": "skolekorps",
    "hwa-rang-heggedal": "kampsport",
    "musica-sinfonietta-asker-barne-og-ungdomsorkester": "orkester",
    "naersnes-og-aros-if-fotball": "fotball",
    "naersnes-sangkor": "sang",
    "saetre-barnekor": "sang",
    "saetre-og-folkestad-skolekorps": "skolekorps",
    "saetre-speidergruppe": "speiding",
    "slemmestad-kfuk-kfum-speiderne": "speiding",
    "slemmestad-og-omegn-turnforening": "turn",
    "slemmestad-skolekorps": "skolekorps",
    "tofte-skolekorps": "skolekorps",
    "vardasen-barne-og-ungdomskor": "sang",
}

def klubbnavn_fra_fil(filnavn):
    """Gjør filnavn til lesbart klubbnavn."""
    navn = filnavn.replace(".html", "").replace("-", " ").title()
    # Fiks vanlige forkortelser
    navn = navn.replace("Il ", "IL ").replace("If ", "IF ").replace("Fk ", "FK ")
    navn = navn.replace("Sk ", "SK ").replace("Dnt ", "DNT ").replace("Nif ", "NIF ")
    navn = navn.replace("Ogamp", "og").replace("Og", "og")
    return navn

def generer_description(filnavn):
    navn = klubbnavn_fra_fil(filnavn)
    nokkel = filnavn.replace(".html", "")
    aktivitet = AKTIVITET.get(nokkel, "idrett og fritid")
    return (f"{navn} tilbyr {aktivitet} i Asker. Se kontaktinfo, "
            f"nettside og adresse – og finn flere fritidsaktiviteter i Asker på askeridrett.no.")

def main():
    endret = 0
    for f in sorted(os.listdir(REPO_DIR)):
        if not f.endswith(".html") or f in SKIP:
            continue
        sti = os.path.join(REPO_DIR, f)
        with open(sti, "r", encoding="utf-8") as fh:
            innhold = fh.read()
        if '<meta name="description"' in innhold:
            continue  # har allerede description
        desc = generer_description(f)
        # Sett inn etter <title> eller i <head>
        if re.search(r'<title>.*?</title>', innhold, re.DOTALL):
            ny = re.sub(
                r'(<title>.*?</title>)',
                r'\1\n<meta name="description" content="' + html.escape(desc) + '">',
                innhold, count=1, flags=re.DOTALL
            )
        else:
            ny = innhold.replace("<head>", '<head>\n<meta name="description" content="' + html.escape(desc) + '">', 1)
        if ny != innhold:
            with open(sti, "w", encoding="utf-8") as fh:
                fh.write(ny)
            endret += 1
    print(f"Ferdig: la til meta description på {endret} undersider.")

if __name__ == "__main__":
    main()
