import joblib
import requests
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors


MODEL = joblib.load(open('./model/model', 'rb'))
MOVIES = joblib.load(open('./features/data', 'rb'))
VECTORS = joblib.load(open('./features/vectors', 'rb'))
TITLES = MOVIES['title'].values.tolist()


def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(title):

    ind = MOVIES[MOVIES['title'] == title].index[0] # get index of movie input
    loc = MOVIES.index.get_loc(ind)  # get iloc of movie
    neighbors = MODEL.kneighbors(VECTORS[loc].reshape(1, -1), n_neighbors=21)[1]  # get most similar movies
    rec_movies = []
    rec_movie_posters = []
    for loc in neighbors.flatten()[1:]:
        rec_movies.append(MOVIES.iloc[loc].title)
        movie_id = MOVIES.iloc[loc].movie_id
        rec_movie_posters.append(fetch_poster(movie_id))

    return rec_movies, rec_movie_posters


def display_movies(rec_movies, rec_movie_posters, ind, num_cols):

    col1, col2, col3, col4 = st.columns(num_cols)

    with col1:
        st.text(rec_movies[ind])
        st.image(rec_movie_posters[ind])
    with col2:
        st.text(rec_movies[ind + 1])
        st.image(rec_movie_posters[ind + 1])

    with col3:
        st.text(rec_movies[ind + 2])
        st.image(rec_movie_posters[ind + 2])
    with col4:
        st.text(rec_movies[ind + 3])
        st.image(rec_movie_posters[ind + 3])


def main(selected_movie):

    rec_movies, rec_movie_posters = recommend(selected_movie)
    num_rows = 5
    num_cols = 4
    ind = 0

    for row in range(num_rows):
        display_movies(rec_movies, rec_movie_posters, ind, num_cols)
        ind += num_cols


# to get and add background image
def add_bg_img():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.ibb.co/7nv62WT/flowers.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


# add background image
add_bg_img()

# show app title
st.title('Movie Recommendations')

# show and select a movie
selected_movie = st.selectbox('select or search a movie from the dropdown and click on Show Recommendations',
                                  TITLES, index=TITLES.index('Spider-Man 3'))

# button to get recommendations
st.button('Show Recommendations')
main(selected_movie)

# show recommendations on button click
if st.button('Recommendations'):
    main(selected_movie)


