import datetime
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from actions.utils import speak
import re

def extract_best_fact(soup):
    # 1. Look for <article> or definition block first
    main_area = soup.find("article")
    if not main_area:
        # Try fallback sections like <main> or <section>
        for tag in ["main", "section", "div"]:
            main_area = soup.find(tag, class_=lambda c: c and 'content' in c.lower())
            if main_area:
                break

    search_space = main_area if main_area else soup

    # 2. Try formulas/code
    for tag in search_space.find_all(["code", "pre", "tt"]):
        text = tag.get_text(strip=True)
        if text and any(char in text for char in "=√+-*/"):
            return text

    # 3. First real paragraph (avoid nav/sidebar garbage)
    for para in search_space.find_all("p"):
        text = para.get_text(strip=True)
        if 50 < len(text) < 400 and not text.lower().startswith("related") and "cookie" not in text.lower():
            return text

    return None

def handle_local_datetime_queries(query: str) -> bool:
    now = datetime.datetime.now()
    q = query.lower()

    if "time" in q:
        speak(f"The current time is {now.strftime('%I:%M %p')}")
        return True
    elif "date" in q:
        speak(f"Today's date is {now.strftime('%B %d, %Y')}")
        return True
    elif "day" in q:
        speak(f"Today is {now.strftime('%A')}")
        return True
    elif "year" in q:
        speak(f"The current year is {now.year}")
        return True

    return False  # Not a known local time query

def web_query(command: str):
    query = command.strip()
    print(f"📥 Query: {query}")

    if handle_local_datetime_queries(query):
        return  # We already answered it

    try:
        results = list(search(query, num_results=1))
        if not results or not results[0].startswith("http"):
            speak(f"Sorry, I couldn't find anything useful about {query}.")
            return

        url = results[0]
        print(f"🔗 Top Result: {url}")

        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        fact = extract_best_fact(soup)

        if fact:
            speak(fact[:300])
        else:
            speak("I found a page, but couldn't extract a clear answer.")
    except Exception as e:
        print("Web query error:", e)
        speak("Sorry, I ran into a problem fetching the info.")
