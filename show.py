from database import select_repositories


def show_repositories():
    rows = select_repositories()
    print(f"{'ID':>5}  {'Repository':<50}  {'Language':<20}  {'Stars':>8}")
    print("-" * 89)
    for repo_id, name, language, stars in rows:
        print(f"{repo_id:>5}  {name:<50}  {language or '-':<20}  {stars:>8}")
    print("-" * 89)
    print(f"total: {len(rows)} repositories")


if __name__ == "__main__":
    show_repositories()
