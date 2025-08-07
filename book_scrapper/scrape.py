import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json

BASE_URL = "https://books.toscrape.com/"
db_client = MongoClient("mongodb://localhost:27017/")
db = db_client.bookstore
collection = db.books

def get_star_rating(star_str):
    mapping = {
        "One": 1, "Two": 2, "Three": 3,
        "Four": 4, "Five": 5
    }
    return mapping.get(star_str, 0)

import re

def scraper():
    books = []
    page = 1
    while True:
        url = f"{BASE_URL}/catalogue/page-{page}.html"
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('article.product_pod')
        if not articles:
            break
        for article in articles:
            title = article.h3.a['title']
            price_text = article.select_one('.price_color').text.strip()
            # Extract numeric part from price using regex
            price_match = re.search(r'\d+\.\d+', price_text)
            if price_match:
                price = float(price_match.group())
            else:
                price = 0.0
            availability_text = article.select_one('.availability').text.strip()
            availability = 'In stock' in availability_text
            rating = get_star_rating(article.p['class'][1])
            url = BASE_URL + '/catalogue/' + article.h3.a['href']
            book = {
                'title': title,
                'price': price,
                'availability': availability,
                'rating': rating,
                'url': url
            }
            books.append(book)
        page += 1

    # Clear existing data and insert new data
    if books:
        collection.delete_many({})
        collection.insert_many(books)

    # Create a clean list for JSON dumping without any MongoDB ObjectId
    clean_books = []
    for book in books:
        clean_book = {k: v for k, v in book.items() if k != '_id'}
        clean_books.append(clean_book)

    # Dump the clean list to JSON
    with open('books.json', 'w') as f:
        json.dump(clean_books, f, indent=4)

    return books

if __name__ == "__main__":
    books = scraper()

    # Analysis
    expensive_books = sorted(books, key=lambda x: x["price"], reverse=True)[:10]
    avg = round(sum(b["price"] for b in books) / len(books), 2)
    availability = sum(1 for b in books if b["availability"])
    five_stars = sum(1 for b in books if b["rating"] == 5)

    print("Top 10 Expensive Books:")
    for b in expensive_books:
        print(f"{b['title']} - ${b['price']}")

    print("\nAverage Price:", avg)
    print("Books In Stock:", availability)
    print("5-Star Books:", five_stars)
