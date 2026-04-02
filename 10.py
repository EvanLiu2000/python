import re
import requests

url = "https://en.wikipedia.org/wiki/Java_(programming_language)"
headers: dict[str, str] = {
    "User-Agent": "WikiLinkAnalyzer/1.0 (Educational Purpose)"
}
response: requests.Response = requests.get(url=url, headers=headers)
response.raise_for_status()
html: str = response.text
start: int = html.find('<div id="mw-content-text" class="mw-body-content">')
end: int = html.find(
    '<div id="catlinks" class="catlinks" data-mw-interface="">')
content: str = html[start:end]

links: list[str] = re.findall(
    r'<a\s+[^>]*href="([^"]*)"[^>]*>',
    content
)

wiki_links: list[str] = []

for link in links:
    if link.startswith("/wiki/") and ":" not in link:
        wiki_links.append(link)

for link in wiki_links[:10]:
    print(f"https://en.wikipedia.org{link}")
# https://en.wikipedia.org/wiki/JavaScript
# https://en.wikipedia.org/wiki/Open_frame
# https://en.wikipedia.org/wiki/Javanese_language
# https://en.wikipedia.org/wiki/Programming_paradigm
# https://en.wikipedia.org/wiki/Programming_paradigm#Multi-paradigm
# https://en.wikipedia.org/wiki/Generic_programming
# https://en.wikipedia.org/wiki/Object-oriented_programming
# https://en.wikipedia.org/wiki/Class-based_programming
# https://en.wikipedia.org/wiki/Functional_programming
# https://en.wikipedia.org/wiki/Imperative_programming
