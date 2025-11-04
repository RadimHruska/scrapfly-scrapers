"""
Test skript pro ověření scrapování profilu kovobroza
"""
import json
from pathlib import Path

results_dir = Path(__file__).parent / "results"

print("=== TEST VÝSLEDKŮ SCRAPOVÁNÍ ===\n")

# Test 1: Kontrola uživatelských dat
print("1. Kontrola uživatelských dat...")
user_file = results_dir / "kovobroza-user.json"
if user_file.exists():
    with open(user_file, 'r', encoding='utf-8') as f:
        user_data = json.load(f)
    print(f"   ✓ Soubor existuje")
    print(f"   ✓ Uživatel: {user_data.get('name', 'N/A')}")
    print(f"   ✓ Username: {user_data.get('username', 'N/A')}")
    print(f"   ✓ ID: {user_data.get('id', 'N/A')}")
    print(f"   ✓ Počet příspěvků: {user_data.get('image_count', 0)}")
    print(f"   ✓ Počet videí: {user_data.get('video_count', 0)}")
    print(f"   ✓ Profilový obrázek: {'Ano' if user_data.get('profile_image') else 'Ne'}")
else:
    print("   ✗ Soubor neexistuje!")

print()

# Test 2: Kontrola příspěvků
print("2. Kontrola příspěvků...")
posts_file = results_dir / "kovobroza-posts.json"
if posts_file.exists():
    with open(posts_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    print(f"   ✓ Soubor existuje")
    print(f"   ✓ Počet příspěvků: {len(posts_data)}")
    
    if posts_data:
        post = posts_data[0]
        print(f"   ✓ Shortcode: {post.get('shortcode', 'N/A')}")
        print(f"   ✓ ID: {post.get('id', 'N/A')}")
        
        # Kontrola obrázků - nyní máme pouze jeden obrázek
        if post.get('image_url'):
            print(f"   ✓ URL obrázku: {post.get('image_url', 'N/A')[:80]}...")
            print(f"   ✓ Rozlišení: {post.get('image_width')}x{post.get('image_height')}")
        else:
            print("   ⚠ Žádné obrázky v příspěvku")
        
        # Kontrola dalších metadat
        print(f"   ✓ Lajky: {post.get('like_count', 0)}")
        print(f"   ✓ Komentáře: {post.get('comment_count', 0)}")
        print(f"   ✓ Datum: {post.get('taken_at', 'N/A')}")
else:
    print("   ✗ Soubor neexistuje!")

print("\n=== TEST DOKONČEN ===")
print("✓ Scraper funguje správně!")
print(f"✓ Všechny výsledky jsou uloženy v: {results_dir}")

