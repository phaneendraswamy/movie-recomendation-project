import streamlit as st
import pandas as pd
import requests
import numpy as np

# Function to fetch movie poster using OMDb API (based on movie title)
def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=584ab2ff"  
    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'True' and 'Poster' in data:
        return data['Poster']  # Return the poster URL
    else:
        return None  # Return None if no poster is found or response is not valid

# Function to recommend similar movies
def recommend(movie, movies, similarity):
    if movie not in movies['title'].values:
        return [], []  # Return empty lists if the movie is not found

    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []

    for i in distance[1:6]:  # Get top 5 similar movies
        movie_title = movies.iloc[i[0]].title
        
        # Fetch poster using OMDb API
        poster = fetch_poster(movie_title)
        
        recommend_movie.append(movie_title)
        recommend_poster.append(poster)  # Add the poster (or None)

    return recommend_movie, recommend_poster

# Load the movie data and similarity matrix (this part should be done based on your data)
def load_data():
    try:
        movies = pd.read_csv(r"C:\Users\Swamy\Downloads\top10K-TMDB-movies.csv\top10K-TMDB-movies.csv")  
    except Exception as e:
        st.error(f"Error loading movie data: {e}")
        return None, None

    similarity = np.random.rand(len(movies), len(movies))  # This is just a placeholder, replace it with your actual similarity data

    return movies, similarity

# Streamlit app
def main():
    # Load data
    movies, similarity = load_data()

    if movies is None or similarity is None:
        return  # Stop execution if data loading failed

    st.title("Movie Recommendation System")

    # Dropdown to select movie
    movie = st.selectbox("Select a Movie", movies['title'].tolist())

    if movie:
        st.write(f"Recommendations for: *{movie}*")
        
        # Get recommendations
        recommended_movies, posters = recommend(movie, movies, similarity)

        # Display recommended movies and posters side by side in columns
        num_recommendations = len(recommended_movies)
        
        # Create a grid of columns
        columns = st.columns(num_recommendations)

        for i in range(num_recommendations):
            with columns[i]:  # Use the specific column for each movie
                st.write(f"{recommended_movies[i]}")
                
                # Check if poster is None and display a default image if so
                if posters[i] is None:
                    st.write("No poster available.")
                    st.image("https://via.placeholder.com/200x300?text=No+Poster+Available", width=200)
                else:
                    # Only set the width (height will adjust automatically)
                    st.image(posters[i], width=200)  # You can adjust the width as needed

if __name__ == "__main__":
    main()

