# Sjösättning askeridrett.no – GitHub Pages + Cloudflare DNS

*Skapad: 2026-08-20 | Uppdaterad: 2026-08-20 (replikera befintlig andersjansson.dev-setup)*
*Status: Deploy-mappen klar, väntar på domänkoppling i Cloudflare*

## Uppsättning (samma som andersjansson.dev fungerar redan)
- **Host:** GitHub Pages (statisk)
- **DNS/proxy/HTTPS:** Cloudflare (Add a site, orange moln)
- **Huvuddomän:** `askeridrett.no`
- **Redirect:** `aktivasker.no` → `askeridrett.no` (301)

## Redan klart
- [x] Deploy-mappen `askeridrett-deploy/` färdig (index + 162 undersidor, 764 KB)
- [x] Cloudflare-konto finns redan (andersjansson.dev ligger där som "Add a site")
- [x] Innehåll verifierat identiskt med det publicerade på GitHub Pages

## Steg 1 – GitHub-repo + Pages
1. Skapa nytt repo på github.com (t.ex. `askeridrett` – kan vara privat)
2. Ladda upp innehållet i `askeridrett-deploy/` till repots rot (`index.html` i roten)
3. Aktivera GitHub Pages på repot: Settings → Pages → Source: branch `main` / root
4. Sätt custom domain `askeridrett.no`: Settings → Pages → Custom domain → spara (GitHub skapar CNAME-filen)
5. GitHub visar dig vilka IP-adresser/records som krävs (se steg 3)

## Steg 2 – Lägg till askeridrett.no i Cloudflare (som en ny "Add a site")
1. Cloudflare Dashboard → **Add a site** → `askeridrett.no` → **Free**
2. Cloudflare ger 2 namneservers → byt hos **Webhuset** (där domänen är köpt)
3. Vänta på att Cloudflare bekräftar (upp till ~24 h, oftast snabbare)

## Steg 3 – DNS-record (kopiera mönstret från andersjansson.dev)
- Kolla hur DNS-servern för `andersjansson.dev` ser ut i Cloudflare och **replikera samma record-typ** för `askeridrett.no`:
  - Antingen **A-post** → GitHub Pages IP (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`) för apex
  - Eller **CNAME** → `<användare>.github.io` (Cloudflare flattenar apex automatiskt)
- Orange moln **på** (proxy) → gratis HTTPS + CDN
- Lägg även `www.askeridrett.no` → peka på samma / redirect till apex

## Steg 4 – 301-redirect aktivasker.no → askeridrett.no
1. Lägg till `aktivasker.no` som en site i Cloudflare (Add a site, Free, samma nameserver-byte hos Webhuset)
2. **Rules → Redirect Rules → Create**
   - När host = `aktivasker.no` (och `www.aktivasker.no`) → 301 till `https://askeridrett.no`

## Steg 5 – E-post (valfritt, gratis)
- Cloudflare → `askeridrett.no` → **Email Routing** → `post@askeridrett.no` → din e-post

## Uppdatera sidan (framöver)
- Redigera i GitHub-repot → push → GitHub Pages publicerar automatiskt (Cloudflare levererar)

## Säkerhetsnotis
- En GitHub-token ligger i klartext i `andersjansson-dev/verifiera_domain.py` + `satt_domain.py`
- Rekommendation: **rotera/återkalla** den token i GitHub (Developer settings → Personal access tokens) när vi är klara
