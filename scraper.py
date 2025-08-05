# scraper.py
import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_and_store():
    url = "https://en.wikipedia.org/wiki/Sport"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Grab paragraph content
    paragraphs = soup.find_all("p")
    content = "\n".join([p.get_text() for p in paragraphs[:10]])

    # Store in DB
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, text TEXT)")
    c.execute("DELETE FROM data")  # Clear old data
    c.execute("INSERT INTO data (text) VALUES (?)", (content,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    scrape_and_store()
