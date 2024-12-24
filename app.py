import pickle
import streamlit as st
import numpy as np
import random
import urllib.parse

# Set page layout as the very first command
st.set_page_config(page_title="Book Recommender System", page_icon="📚", layout="centered")

# Author Info Sidebar
st.sidebar.markdown("### Author: Nikita Mishra")
st.sidebar.markdown("### Email: nikita.edu4u@gmail.com")
st.sidebar.markdown("### Date: 2023-Oct-20")

# Add custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f7f7f7;
            font-family: 'Helvetica', sans-serif;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #2d2d2d;
            text-align: center;
        }
        .subheader {
            font-size: 18px;
            color: #555;
            text-align: center;
        }
        .book-card {
            background-color: #fff;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.3s;
        }
        .book-card:hover {
            transform: translateY(-10px);
        }
        .book-image {
            border-radius: 8px;
            width: 150px;
            height: 220px;
            object-fit: cover;
        }
        .button {
            background-color: #FF6347;
            color: white;
            padding: 12px 30px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .button:hover {
            background-color: #FF4500;
        }
        .footer {
            font-size: 14px;
            text-align: center;
            color: #777;
        }
    </style>
""", unsafe_allow_html=True)

# Page Title and Description
st.markdown("<div class='title'>📚 Book Recommender System Using Machine Learning 📚</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Welcome to the Book Recommender System! 📖</div>", unsafe_allow_html=True)
st.markdown("""
    Our system recommends books based on your chosen book. Simply select a book from the dropdown menu, 
    and we'll recommend similar books for you. Happy reading! 📚
""", unsafe_allow_html=True)

# Load the models and data
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_names.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))

# Function to fetch book posters, ratings, and generate URLs
def fetch_poster_and_rating(suggestion):
    book_names = []
    ids_index = []
    poster_url = []
    ratings = []
    links = []  # List to store book links

    # Extract book names from suggestion
    for book_id in suggestion:
        book_names.append(book_pivot.index[book_id])

    # Fetch the corresponding ids in final_rating to get URLs, ratings, and generate links
    for name in book_names:
        ids = np.where(final_rating['title'] == name)[0]
        
        # Ensure that the index exists before using it
        if len(ids) > 0:
            ids_index.append(ids[0])

    # Fetching the poster URLs, ratings, and generating links using the correct indices
    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        rating = final_rating.iloc[idx]['rating']  # Assuming 'rating' column exists
        # Generate a URL to Goodreads or Amazon
        book_link = generate_book_link(book_names[ids_index.index(idx)])
        poster_url.append(url)
        ratings.append(rating)
        links.append(book_link)

    return poster_url, ratings, links

# Function to generate book links (to Goodreads or Amazon)
def generate_book_link(book_title):
    # You can customize the search URLs depending on the platform
    # Example: Generate a Goodreads link
    base_url = "https://www.goodreads.com/search?q="
    encoded_title = urllib.parse.quote_plus(book_title)
    book_link = f"{base_url}{encoded_title}"
    return book_link

# Function to recommend books
def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    
    # Get recommendations from the model
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    # Fetch poster URLs, ratings, and links for recommended books
    poster_url, ratings, links = fetch_poster_and_rating(suggestion.flatten())  # Ensure suggestion is flattened
    
    # Prepare the list of recommended books
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)
    
    # Randomize the order of recommendations
    random_indices = list(range(len(books_list)))
    random.shuffle(random_indices)
    
    # Shuffle the books, posters, ratings, and links based on random indices
    randomized_books = [books_list[i] for i in random_indices]
    randomized_posters = [poster_url[i] for i in random_indices]
    randomized_ratings = [ratings[i] for i in random_indices]
    randomized_links = [links[i] for i in random_indices]

    return randomized_books, randomized_posters, randomized_ratings, randomized_links

# Dropdown to select a book
selected_books = st.selectbox(
    "🔍 Type or select a book from the dropdown",
    book_names
)

# Show recommendations on button click
if st.button('Show Recommendations 🚀', key='recommendation_btn', help="Get book recommendations based on your choice"):
    recommended_books, poster_url, ratings, links = recommend_book(selected_books)

    # Displaying the results in columns
    st.markdown("### Here are some book recommendations for you: ")

    col1, col2, col3, col4, col5 = st.columns(5)

    # Display the books in each column with their ratings and links
    with col1:
        st.markdown(f"<div class='book-card'><a href='{links[0]}' target='_blank'><img class='book-image' src='{poster_url[0]}' /></a><div>{recommended_books[0]}</div><div>⭐ {ratings[0]}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='book-card'><a href='{links[1]}' target='_blank'><img class='book-image' src='{poster_url[1]}' /></a><div>{recommended_books[1]}</div><div>⭐ {ratings[1]}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='book-card'><a href='{links[2]}' target='_blank'><img class='book-image' src='{poster_url[2]}' /></a><div>{recommended_books[2]}</div><div>⭐ {ratings[2]}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='book-card'><a href='{links[3]}' target='_blank'><img class='book-image' src='{poster_url[3]}' /></a><div>{recommended_books[3]}</div><div>⭐ {ratings[3]}</div></div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div class='book-card'><a href='{links[4]}' target='_blank'><img class='book-image' src='{poster_url[4]}' /></a><div>{recommended_books[4]}</div><div>⭐ {ratings[4]}</div></div>", unsafe_allow_html=True)
    
    # Adding footer with call to action and comment section
    st.markdown("""
        ---
        Enjoyed the recommendations? Let us know your thoughts! 💬
        Or feel free to try another book! 📚
    """, unsafe_allow_html=True)

    # User comment section
    user_comment = st.text_area("Your Comments:", placeholder="Enter your thoughts about the recommendations...", height=100)

    # Submit button for feedback
    submit_feedback = st.button("Submit Feedback", key="submit_feedback")

    if submit_feedback:
        if not user_comment.strip():  # Check if comment is empty
            st.warning("Please enter your comment before submitting.")  # Display warning if empty
        else:
            st.write("Thanks for your feedback! 💡")
            # Optionally, save the feedback to a file or a database
            # feedback_data = {"comment": user_comment}
            # save_feedback(feedback_data)
    
    st.markdown("<div class='footer'>Thanks for using the Book Recommender! 🙏</div>", unsafe_allow_html=True)
