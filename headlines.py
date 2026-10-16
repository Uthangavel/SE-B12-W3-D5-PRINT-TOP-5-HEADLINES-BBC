"""Print the first five unique BBC News headlines in page order.

Install dependencies: python -m pip install requests beautifulsoup4
Run: python headlines.py

Inspected BBC HTML: <h2 data-testid="card-headline" class="...">...</h2>.
The classes are generated, so use the observed data-testid attribute.
Browser console check:
    [...document.querySelectorAll('h2[data-testid="card-headline"]')]
        .map(element => element.textContent.trim()).slice(0, 5)
"""

import sys

import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"
SELECTOR = 'h2[data-testid="card-headline"]'
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}


def extract_headlines(html, limit=5):
    soup = BeautifulSoup(html, "html.parser")
    headlines = []
    seen = set()
    for element in soup.select(SELECTOR):
        headline = " ".join(element.get_text(" ", strip=True).split())
        key = headline.casefold()
        if not headline or key in seen:
            continue
        seen.add(key)
        headlines.append(headline)
        if len(headlines) == limit:
            break
    return headlines


def main():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=30)
        # Check the status before passing any response HTML to BeautifulSoup.
        if response.status_code != 200:
            print(f"Could not fetch BBC News: HTTP {response.status_code}.", file=sys.stderr)
            return 1
    except requests.RequestException as exc:
        print(f"Could not fetch BBC News: {exc}", file=sys.stderr)
        return 1

    headlines = extract_headlines(response.content)
    for number, headline in enumerate(headlines, start=1):
        print(f"{number}. {headline}")

    if len(headlines) < 5:
        print(
            f"Only {len(headlines)} unique headlines found; expected 5. "
            "Inspect the HTML: BBC may have changed its markup or returned a challenge page.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
