import json
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://github.com/orgs/google/repositories"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}
MAX_RETRY = 5


def fetch_html(page):
    params = {"q": "sort:name-asc", "page": page}
    for _ in range(MAX_RETRY):
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            return response.text
        wait = int(response.headers.get("Retry-After", 10))
        print(f"page {page}: status {response.status_code}, retry after {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"page {page}: failed to fetch")


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", attrs={"data-target": "react-app.embeddedData"})
    data = json.loads(script.string)
    route = data["payload"]["orgReposPageRoute"]

    repos = []
    for item in route["repositories"]:
        language = item["primaryLanguage"]["name"] if item["primaryLanguage"] else None
        repos.append(
            {
                "name": item["name"],
                "language": language,
                "stars": item["starsCount"],
            }
        )
    return repos, route["pageCount"]


def scrape_pages():
    page = 1
    page_count = 1
    while page <= page_count:
        html = fetch_html(page)
        repos, page_count = parse_html(html)
        print(f"page {page}/{page_count}: {len(repos)} repositories")
        yield repos
        page += 1
        time.sleep(1)
