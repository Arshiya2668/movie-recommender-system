
import streamlit as st
import pandas as pd
import re

# 🔹 Set background using custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1497032628192-86f99bcd76bc");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Optional: Make text readable */
    .block-container {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 10px;
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Load movie data
movies = pd.read_csv("data/movies.csv")

# 🔹 Extract year from title
def extract_year(title):
    match = re.search(r'\((\d{4})\)', title)
    return match.group(1) if match else "Unknown"

movies['year'] = movies['title'].apply(extract_year)

# 🔹 Clean genres
movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)

# 🔹 Streamlit UI
st.set_page_config(page_title="Movie Genre Finder", layout="centered")
st.title("🎭 Genre-Based Movie List")

# 🎯 Genre Input
genre_input = st.text_input("Enter a genre (e.g., Thriller, Comedy, Romance, Action)")

if genre_input:
    st.subheader(f"🎬 Movies in Genre: {genre_input.title()}")

    # Filter by genre using regex match
    filtered = movies[movies['genres'].str.contains(rf'\b{genre_input}\b', case=False, regex=True)]

    if filtered.empty:
        st.warning("No movies found in this genre.")
    else:
        for i, row in filtered[['title', 'year']].head(20).iterrows():
            # Remove duplicate year from title
            clean_title = re.sub(r'\(\d{4}\)', '', row['title']).strip()
            st.write(f"🎬 {clean_title} ({row['year']})")
