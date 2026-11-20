from database import count_repositories, create_table, insert_repositories
from scraper import scrape_pages
from show import show_repositories


def main():
    create_table()
    for repos in scrape_pages():
        insert_repositories(repos)
    print(f"saved: {count_repositories()} repositories\n")
    show_repositories()


if __name__ == "__main__":
    main()
