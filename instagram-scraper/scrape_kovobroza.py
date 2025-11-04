"""
Skript pro scrapování příspěvků z Instagram profilu kovobroza
"""
from pathlib import Path
from loguru import logger as log
import asyncio
import json
import instagram

output = Path(__file__).parent / "results"
output.mkdir(exist_ok=True)

USERNAME = "kovobroza"

async def run():
    # enable scrapfly cache?
    instagram.BASE_CONFIG["cache"] = True
    instagram.BASE_CONFIG["debug"] = True

    print(f"Scrapuji Instagram profil: {USERNAME}")
    print("Ukládám výsledky do ./results directory")

    # Scrapování informací o uživateli
    log.info("Načítám informace o uživateli...")
    user = await instagram.scrape_user(USERNAME)
    output.joinpath(f"{USERNAME}-user.json").write_text(
        json.dumps(user, indent=2, ensure_ascii=False), 
        encoding='utf-8'
    )
    log.success(f"Uloženo: {USERNAME}-user.json")
    print(f"Uživatel: {user.get('name', 'N/A')}")
    print(f"Počet příspěvků (obrázky): {user.get('image_count', 'N/A')}")
    print(f"Počet videí: {user.get('video_count', 'N/A')}")
    print(f"Sledující: {user.get('followers', 'N/A')}")
    print()

    # Scrapování všech příspěvků (fotek)
    log.info("Načítám všechny příspěvky...")
    posts_all = []
    post_count = 0
    async for post in instagram.scrape_user_posts(USERNAME, max_pages=None):
        posts_all.append(post)
        post_count += 1
        if post_count % 10 == 0:
            log.info(f"Načteno {post_count} příspěvků...")
    
    log.success(f"Celkem načteno {len(posts_all)} příspěvků")
    output.joinpath(f"{USERNAME}-posts.json").write_text(
        json.dumps(posts_all, indent=2, ensure_ascii=False), 
        encoding='utf-8'
    )
    log.success(f"Uloženo: {USERNAME}-posts.json")
    
    # Shrnutí
    print("\n=== SHRNUTÍ ===")
    print(f"Celkem načteno příspěvků: {len(posts_all)}")
    print(f"Výsledky uloženy v:")
    print(f"  - {output}/{USERNAME}-user.json")
    print(f"  - {output}/{USERNAME}-posts.json")


if __name__ == "__main__":
    asyncio.run(run())

