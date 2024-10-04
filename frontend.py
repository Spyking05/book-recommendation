from flask import Flask, request, jsonify, render_template
from backend import fetch_books_from_api, generate_recommendations  # Import the backend logic

app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')  # Assuming your HTML file is named index.html and in the 'templates' folder

# Handle book recommendation requests
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    query = data.get('query')
    genre = data.get('genre', '').lower()
    author = data.get('author', '').lower()

    books = fetch_books_from_api(query)
    recommendations = generate_recommendations(books, genre, author)

    return jsonify({'recommendations': [book.__repr__() for book in recommendations]})

if __name__ == "__main__":
    app.run(debug=True)
