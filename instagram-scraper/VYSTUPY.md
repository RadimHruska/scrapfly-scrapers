# Výstupy Instagram Scraperu

Scraper generuje **2 hlavní JSON soubory** s daty o Instagram profilu a příspěvcích.

## 📁 Výstupní soubory

### 1. `{username}-user.json` - Informace o profilu
Obsahuje kompletní data o Instagram profilu uživatele.

**Struktura dat:**
```json
{
  "name": "Jméno uživatele",
  "username": "username",
  "id": "Instagram ID",
  "category": "Kategorie profilu",
  "business_category": "Business kategorie",
  "phone": "Telefon (pokud je business)",
  "email": "Email (pokud je business)",
  "bio": "Bio text",
  "bio_links": ["url1", "url2"],
  "homepage": "URL na homepage",
  "followers": 1234,
  "follows": 567,
  "facebook_id": "Facebook ID",
  "is_private": false,
  "is_verified": false,
  "profile_image": "URL profilového obrázku",
  "video_count": 10,
  "videos": [...],
  "image_count": 50,
  "images": [...],
  "saved_count": 0,
  "collections_count": 0,
  "related_profiles": ["username1", "username2"]
}
```

**Klíčová pole:**
- `name` - Celé jméno
- `username` - Instagram username
- `followers` - Počet sledujících
- `follows` - Počet sledovaných
- `image_count` - Počet obrázků
- `video_count` - Počet videí
- `profile_image` - URL profilového obrázku
- `bio` - Bio text
- `is_private` - Zda je profil soukromý
- `is_verified` - Zda je profil ověřený

---

### 2. `{username}-posts.json` - Všechny příspěvky
Pole objektů - každý objekt reprezentuje jeden příspěvek.

**Struktura jednoho příspěvku:**
```json
{
  "id": "ID příspěvku",
  "shortcode": "Krátký kód příspěvku (pro URL)",
  "caption": "Text popisku",
  "taken_at": 1761425519,
  "video_versions": null,
  "image_versions2": {
    "candidates": [
      {
        "url": "https://...",
        "height": 854,
        "width": 854
      },
      {
        "url": "https://...",
        "height": 720,
        "width": 720
      }
      // ... více velikostí
    ]
  },
  "original_height": 854,
  "original_width": 854,
  "link": null,
  "title": null,
  "comment_count": 5,
  "top_likers": [...],
  "like_count": 42,
  "usertags": [...],
  "clips_metadata": null,
  "comments": [...]
}
```

**Klíčová pole pro obrázky:**
- `id` - Unikátní ID příspěvku
- `shortcode` - Kód pro URL: `instagram.com/p/{shortcode}/`
- `caption` - Text popisku příspěvku
- `taken_at` - Unix timestamp kdy byl příspěvek vytvořen
- `image_versions2.candidates[]` - Pole obrázků v různých velikostech
  - `url` - URL adresa obrázku
  - `height` - Výška v pixelech
  - `width` - Šířka v pixelech
- `like_count` - Počet lajků
- `comment_count` - Počet komentářů
- `comments` - Pole komentářů (pokud jsou dostupné)

**Klíčová pole pro videa:**
- `video_versions` - Pole video souborů v různých kvalitách
  - `url` - URL adresa videa
  - `height` - Výška
  - `width` - Šířka
  - `type` - Typ videa

---

## 📊 Příklad použití dat

### Získání URL všech obrázků z příspěvků:

```python
import json

with open('results/kovobroza-posts.json', 'r') as f:
    posts = json.load(f)

for post in posts:
    if post.get('image_versions2'):
        # Nejvyšší rozlišení je obvykle první
        highest_res = post['image_versions2']['candidates'][0]
        print(f"URL: {highest_res['url']}")
        print(f"Rozlišení: {highest_res['width']}x{highest_res['height']}")
```

### Získání všech URL obrázků do seznamu:

```python
import json

with open('results/kovobroza-posts.json', 'r') as f:
    posts = json.load(f)

all_image_urls = []
for post in posts:
    if post.get('image_versions2'):
        for candidate in post['image_versions2']['candidates']:
            all_image_urls.append(candidate['url'])

# Odstranění duplicit
unique_urls = list(set(all_image_urls))
print(f"Celkem {len(unique_urls)} unikátních URL obrázků")
```

### Získání nejvyššího rozlišení každého obrázku:

```python
import json

with open('results/kovobroza-posts.json', 'r') as f:
    posts = json.load(f)

high_res_images = []
for post in posts:
    if post.get('image_versions2') and post['image_versions2'].get('candidates'):
        # První candidate má obvykle nejvyšší rozlišení
        img = post['image_versions2']['candidates'][0]
        high_res_images.append({
            'url': img['url'],
            'width': img['width'],
            'height': img['height'],
            'shortcode': post.get('shortcode'),
            'caption': post.get('caption')
        })
```

---

## 📍 Umístění výsledků

Všechny výsledky se ukládají do složky:
```
instagram-scraper/results/
  ├── {username}-user.json      # Profil uživatele
  └── {username}-posts.json      # Všechny příspěvky
```

---

## 🔍 Důležité poznámky

1. **Obrázky v různých velikostech**: Každý příspěvek obsahuje obrázky v několika velikostech (240px, 320px, 480px, 640px, 720px, 854px, atd.). První v seznamu je obvykle nejvyšší rozlišení.

2. **Shortcode**: Použijte pro vytvoření URL: `https://www.instagram.com/p/{shortcode}/`

3. **Timestamp**: `taken_at` je Unix timestamp. Pro převod na datum:
   ```python
   from datetime import datetime
   timestamp = 1761425519
   date = datetime.fromtimestamp(timestamp)
   ```

4. **Komentáře**: Ne všechny příspěvky mají komentáře načtené. Pokud je `comments: null`, komentáře nebyly načteny.

5. **Videa**: Pokud je `video_versions: null`, příspěvek je obrázek. Pokud obsahuje data, je to video.

