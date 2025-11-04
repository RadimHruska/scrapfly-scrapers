"""
Univerzální skript pro scrapování příspěvků z libovolného Instagram profilu
Použití: python scrape_profile.py username
Nebo: python scrape_profile.py aj_sluzby
"""
from pathlib import Path
from loguru import logger as log
import asyncio
import json
import sys
import instagram

output = Path(__file__).parent / "results"
output.mkdir(exist_ok=True)


async def scrape_instagram_profile(username: str):
    """Scrapuje Instagram profil a všechny jeho příspěvky"""
    # enable scrapfly cache?
    instagram.BASE_CONFIG["cache"] = True
    instagram.BASE_CONFIG["debug"] = True

    print(f"Scrapuji Instagram profil: {username}")
    print("Ukládám výsledky do ./results directory")
    print()

    # Scrapování informací o uživateli
    log.info("Načítám informace o uživateli...")
    try:
        user = await instagram.scrape_user(username)
        output.joinpath(f"{username}-user.json").write_text(
            json.dumps(user, indent=2, ensure_ascii=False), 
            encoding='utf-8'
        )
        log.success(f"Uloženo: {username}-user.json")
        print(f"Uživatel: {user.get('name', 'N/A')}")
        print(f"Počet příspěvků (obrázky): {user.get('image_count', 'N/A')}")
        print(f"Počet videí: {user.get('video_count', 'N/A')}")
        print(f"Sledující: {user.get('followers', 'N/A')}")
        print(f"Sleduje: {user.get('follows', 'N/A')}")
        print()
    except Exception as e:
        log.error(f"Chyba při načítání uživatelských dat: {e}")
        return

    # Scrapování všech příspěvků (fotek)
    log.info("Načítám všechny příspěvky...")
    posts_all = []
    post_count = 0
    try:
        async for post in instagram.scrape_user_posts(username, max_pages=None):
            # Extrahovat pouze jeden obrázek s nejvyšším rozlišením
            processed_post = {
                "id": post.get("id"),
                "shortcode": post.get("shortcode"),
                "caption": post.get("caption"),
                "taken_at": post.get("taken_at"),
                "image_url": post.get("image_url"),  # Pouze jeden obrázek
                "image_width": post.get("image_width"),
                "image_height": post.get("image_height"),
                "video_url": post.get("video_url"),  # Pouze jedno video (pokud existuje)
                "video_width": post.get("video_width"),
                "video_height": post.get("video_height"),
                "like_count": post.get("like_count"),
                "comment_count": post.get("comment_count"),
                "link": post.get("link"),
                "title": post.get("title")
            }
            posts_all.append(processed_post)
            post_count += 1
            if post_count % 10 == 0:
                log.info(f"Načteno {post_count} příspěvků...")
    except Exception as e:
        log.error(f"Chyba při načítání příspěvků: {e}")
    
    log.success(f"Celkem načteno {len(posts_all)} příspěvků")
    output.joinpath(f"{username}-posts.json").write_text(
        json.dumps(posts_all, indent=2, ensure_ascii=False), 
        encoding='utf-8'
    )
    log.success(f"Uloženo: {username}-posts.json")
    
    # Shrnutí
    print("\n=== SHRNUTÍ ===")
    print(f"Profil: {username}")
    print(f"Celkem načteno příspěvků: {len(posts_all)}")
    print(f"Výsledky uloženy v:")
    print(f"  - {output}/{username}-user.json")
    print(f"  - {output}/{username}-posts.json")
    
    # Statistiky obrázků
    image_count = sum(1 for p in posts_all if p.get('image_url'))
    video_count = sum(1 for p in posts_all if p.get('video_url'))
    print(f"\nStatistiky:")
    print(f"  - Obrázky: {image_count}")
    print(f"  - Videa: {video_count}")


async def main():
    """Hlavní funkce"""
    if len(sys.argv) < 2:
        print("Použití: python scrape_profile.py <username>")
        print("Příklad: python scrape_profile.py aj_sluzby")
        print("Příklad: python scrape_profile.py kovobroza")
        sys.exit(1)
    
    username = sys.argv[1].replace('@', '').strip()  # Odstranit @ pokud je tam
    await scrape_instagram_profile(username)


if __name__ == "__main__":
    asyncio.run(main())

