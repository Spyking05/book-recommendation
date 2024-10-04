import requests
import numpy as np
import pandas as pd
from scipy.stats import norm, ttest_ind, f_oneway, chi2_contingency
import matplotlib.pyplot as plt

class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

    def __repr__(self):
        return f"'{self.title}' by {self.author} ({self.genre})"

def fetch_books_from_api(query, max_results=40):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Error fetching data from Google Books API")

    books_data = response.json()
    books = []
    for item in books_data.get('items', []):
        title = item['volumeInfo'].get('title', 'Unknown Title')
        authors = item['volumeInfo'].get('authors', ['Unknown Author'])
        genres = item['volumeInfo'].get('categories', ['Unknown Genre'])

        # Handle cases where these attributes are missing
        books.append(Book(title or 'Unknown Title', 
                          authors[0] if authors else 'Unknown Author', 
                          genres[0] if genres else 'Unknown Genre'))
    return books


def get_user_preferences():
    genre = input("Enter your preferred genre (leave blank if none): ").strip().lower()
    author = input("Enter your preferred author (leave blank if none): ").strip().lower()
    return genre, author

def generate_recommendations(books, genre, author):
    recommendations = []
    for book in books:
        if (genre in book.genre.lower() or not genre) and (author in book.author.lower() or not author):
            recommendations.append(book)
    return recommendations

def display_recommendations(recommendations):
    if recommendations:
        print("\nRecommended books for you:")
        for book in recommendations:
            print(book)
    else:
        print("\nNo recommendations found based on your preferences.")

def simulate_user_ratings(books, n_users=100, n_days=30):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days).tolist()
    data = []
    for book in books:
        for _ in range(n_users):
            for date in dates:
                rating = np.random.randint(1, 6)
                data.append([book.title, book.author, book.genre, date, rating])
    return pd.DataFrame(data, columns=['Title', 'Author', 'Genre', 'Date', 'Rating'])

def main():
    query = input("Enter a search term for books (e.g., 'python programming'): ").strip()
    books = fetch_books_from_api(query)
    genre, author = get_user_preferences()
    recommendations = generate_recommendations(books, genre, author)
    display_recommendations(recommendations)

    # Simulate user ratings data
    user_ratings_df = simulate_user_ratings(books)

    # Perform statistical tests and analyses
    if recommendations:
        book_title = recommendations[0].title
        print(f"\nPerforming statistical tests and analyses for '{book_title}':")

if __name__ == "__main__":
    main()

