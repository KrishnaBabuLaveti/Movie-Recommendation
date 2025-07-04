import streamlit as st
import pandas as pd
import pickle
import difflib

# Load data and model globally
data = pd.read_csv('movies.csv')
movie_list = data['title'].tolist()
recommend_list = []

with open("movie_recommendation.sav", "rb") as file:
    loaded_model = pickle.load(file)


def get_prediction(input_data):
    global movie_list
    find_close_match = difflib.get_close_matches(input_data, movie_list)
    
    if not find_close_match:
        st.warning("No close match found for the movie name.")
        return []  # Return empty list instead of None

    close_match = find_close_match[0]
    index = data[data['title'] == close_match]['index'].values[0]
    similarity_score = list(enumerate(loaded_model[index]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    st.subheader(f"Top 15 recommendations similar to '{close_match}':")
    recommended_movies = []
    i = 1
    for movie in sorted_similar_movies:
        idx = movie[0]
        title = data.loc[idx, 'title']
        if i <= 15:
            recommended_movies.append(title)
            i += 1
    return recommended_movies
def main():
    st.title("Movie Recommendation System")
    input_movie = st.text_input("Enter the movie name")
    
    if st.button("Recommend") and input_movie.strip():
        recommend_list = get_prediction(input_movie)
        if not recommend_list:
            st.info("No recommendations available. Try a different movie name.")
        else:
            for i in range(len(recommend_list)):
                st.success(f"{i+1}. {recommend_list[i]}")

if __name__ == '__main__':
    main()