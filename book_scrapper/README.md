# Book Scraper and CRUD API

## Overview
This project scrapes all book data from https://books.toscrape.com/, stores it in MongoDB, and provides a REST API for basic CRUD operations. It also stores the book details in books.json file

## Libraries Used
- requests, beautifulsoup4,pymongo, fastapi, uvicorn

## Features
- Pagination and scraping of all books
- Star rating converted to integer (1-5)
- CRUD API with filtering
- Stats:
  - Top 10 expensive books
  - Average price
  - Number in stock
  - Number of 5-star books

## Steps to run
- First, change directory to the project folder "cd book_scrapper"
- create an env using the command "python3 -m venv venv" where venv is the virtual environment name
- Activate the virtual environment using "source venv/bin/activate" (Linux/Mac) or "venv\Scripts\activate" (Windows)
- Install the required dependencies using "pip install -r requirements.txt"
- Make sure you have MongoDB installed and running on port 27017
- Run the scraper using "python scraper.py" to fetch and store book data in MongoDB
- Run the FastAPI server using "uvicorn crud:app --reload" to access the REST API
- Access the API documentation at "http://127.0.0.1:8000/docs" for testing and exploring endpoints

## Edge Cases or Assumptions:
- if the rating of the book is not 1-5 then it is defaulted as 0
- The Scraper clears the previoius db entries to make sure the values are not repeated