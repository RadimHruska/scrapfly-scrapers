# Nastavení GitHub Actions pro Instagram Scraper

## 📋 Požadavky

1. GitHub repository
2. Scrapfly API klíč

## 🔧 Nastavení

### 1. Přidání API klíče do GitHub Secrets

1. Jděte do vašeho GitHub repository
2. Klikněte na **Settings** → **Secrets and variables** → **Actions**
3. Klikněte na **New repository secret**
4. Název: `SCRAPFLY_KEY`
5. Hodnota: Váš Scrapfly API klíč (`scp-live-bb38d7c617a34ac5b396492946fa0989`)
6. Klikněte na **Add secret**

### 2. Nastavení GitHub Pages

1. Jděte do **Settings** → **Pages**
2. **Source**: Vyberte `Deploy from a branch`
3. **Branch**: Vyberte `main` (nebo `master`)
4. **Folder**: Vyberte `/docs`
5. Klikněte na **Save**

### 3. Povolení zápisu do repository

GitHub Actions potřebuje oprávnění k commitování změn:

1. Jděte do **Settings** → **Actions** → **General**
2. V sekci **Workflow permissions**:
   - Vyberte **Read and write permissions**
   - Zaškrtněte **Allow GitHub Actions to create and approve pull requests**
3. Klikněte na **Save**

## 🚀 Jak to funguje

1. **Automatické spouštění**: Workflow se spouští každých **5 hodin** automaticky
2. **Ruční spuštění**: Můžete také spustit ručně v **Actions** → **Instagram Scraper** → **Run workflow**
3. **Scrapování**: Spustí se oba scrapery:
   - `scrape_kovobroza.py`
   - `scrape_aj_sluzby.py`
4. **Uložení**: Výsledky se uloží do `docs/instagram/`
5. **Commit**: Změny se automaticky commitnou a pushnou do repository
6. **Deploy**: GitHub Pages automaticky nasadí nové soubory

## 📁 Struktura souborů

```
docs/
├── index.html              # Hlavní stránka s přehledem
├── .nojekyll              # Soubor pro GitHub Pages
└── instagram/
    ├── kovobroza-user.json
    ├── kovobroza-posts.json
    ├── aj_sluzby-user.json
    └── aj_sluzby-posts.json
```

## 🌐 Přístup k výsledkům

Po nastavení GitHub Pages budou výsledky dostupné na:
- `https://[vase-username].github.io/scrapfly-scrapers/`
- JSON soubory: `https://[vase-username].github.io/scrapfly-scrapers/instagram/kovobroza-user.json`

## 🔍 Ověření

1. Po prvním spuštění zkontrolujte **Actions** tab - workflow by měl proběhnout úspěšně
2. Zkontrolujte, že se soubory objevily v `docs/instagram/`
3. Ověřte, že GitHub Pages je aktivní a zobrazuje stránku

## ⚙️ Úprava četnosti spouštění

Pokud chcete změnit frekvenci spouštění, upravte v `.github/workflows/instagram-scraper.yml`:

```yaml
schedule:
  - cron: '0 */5 * * *'  # Každých 5 hodin
```

Syntax cron: `minuta hodina den měsíc den_v_týdnu`
- `0 */5 * * *` = každých 5 hodin
- `0 */1 * * *` = každou hodinu
- `0 0 * * *` = každý den v půlnoci

## 🐛 Řešení problémů

**Workflow se nespouští:**
- Zkontrolujte, že máte nastavený `SCRAPFLY_KEY` v Secrets
- Ověřte, že workflow soubor je v `.github/workflows/`

**GitHub Pages nezobrazuje soubory:**
- Zkontrolujte, že soubory jsou v `docs/` složce
- Ověřte nastavení Pages (Settings → Pages)

**Chyba při commitování:**
- Zkontrolujte Workflow permissions (musí být Read and write)

