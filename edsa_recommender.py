"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
import pyarrow as pa
# Data handling dependencies
import pandas as pd
import numpy as np
import os
import ast
import time
import sys

from cometML import Experiment, log_metrics, log_model
# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model
#from streamlit_extras.stateful_button import button as stateful_button




# # Use the obtained information as needed
# st.write("App Mode:", app_mode)
# st.write("Command Line Args:", command_line_args)

#experiment = Experiment(api_key="5GQUeJbYop4ZaqBrtCQ12YaXh", project_name="unsupervised", workspace="vascoeti")


# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')
###############
if "active_page" not in st.session_state:
    st.session_state.active_page = "Movie List"

# Function to handle user input for movie ratings and reviews
def rate_movie(movie_title):
    st.write(f"Review and rate the movie: {movie_title}")

    # Check if the movie has already been rated
    if movie_title in st.session_state.watch_again_rating_list:
        st.write("You have already rated and reviewed this movie.")
        return

    # Get user's rating and review
    rating = st.slider(f"Rating (out of 5 stars) for {movie_title}", min_value=1, max_value=5, step=1, key=f"rating_{movie_title}")
    review = st.text_area(f"Your review for {movie_title}", key=f"review_{movie_title}")

    # Use the movie_title as part of the key for the st.button widget
    if st.button("Submit Rating and Review", key=f"submit_{movie_title}"):
        # Store the rating and review in the watch_again_rating_list
        rating_data = {"Title": movie_title, "Rating": rating, "Review": review}
        st.session_state.watch_again_rating_list.append(rating_data)
        st.write(f"Thank you for rating and reviewing {movie_title}!")

def rating_page():
    st.title("Rating and Review")
    watch_again_list = st.session_state.watch_again_list
    if watch_again_list.empty:  # Check if the DataFrame is empty
        st.write("No movies in the Watch Again list.")
    else:
        for movie_title in watch_again_list["Title"]:
            rate_movie(movie_title)
    
###############
# Function to add recommended movies to the session state
def add_recommended_movies(movie_list):
    st.session_state.recommended_movies.extend(movie_list)
# Function to initialize watchlist, favorite list, and watch-again list as session state variables
def initialize_lists():
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = pd.DataFrame(columns=["Title", "Category"])

    if "favorite_list" not in st.session_state:
        st.session_state.favorite_list = pd.DataFrame(columns=["Title", "Category"])

    if "watch_again_list" not in st.session_state:
        st.session_state.watch_again_list = pd.DataFrame(columns=["Title", "Category"])

# Function to add a movie to the watchlist
# Initialize session state variables for watchlist, favorite list, and watch-again list
if "watchlist" not in st.session_state:
    st.session_state.watchlist = pd.DataFrame(columns=["Title", "Category"])

if "favorite_list" not in st.session_state:
    st.session_state.favorite_list = pd.DataFrame(columns=["Title", "Category"])

if "watch_again_list" not in st.session_state:
    st.session_state.watch_again_list = pd.DataFrame(columns=["Title", "Category"])

# Function to add a movie to the watchlist
import streamlit as st
import pandas as pd

# Function to add a movie to the watchlist
def add_to_watchlist(movie_title, movie_category):
    watchlist_df = st.session_state.watchlist

    if "Title" not in watchlist_df.columns:
        # Initialize DataFrame with "Title" and "Category" columns
        watchlist_df = pd.DataFrame(columns=["Title"])

    # Check if the DataFrame is empty
    if watchlist_df.empty:
        new_row = pd.DataFrame({"Title": [movie_title]})
        st.session_state.watchlist = pd.concat([watchlist_df, new_row], ignore_index=True)
    else:
        # Check if the movie title is not already in the DataFrame's "Title" column
        if movie_title not in watchlist_df["Title"].values.tolist():
            new_row = pd.DataFrame({"Title": [movie_title]})
            st.session_state.watchlist = pd.concat([watchlist_df, new_row], ignore_index=True)
        else:
            st.warning(f"{movie_title} is already in the watchlist. Please add a different movie.")

# Function to add a movie to the favorite list
def add_to_favorite_list(movie_title, movie_category):
    favorite_list_df = st.session_state.favorite_list

    if "Title" not in favorite_list_df.columns:
        # Initialize DataFrame with "Title" and "Category" columns
        favorite_list_df = pd.DataFrame(columns=["Title", "Category"])

    # Check if the DataFrame is empty
    if favorite_list_df.empty:
        new_row = pd.DataFrame({"Title": [movie_title], "Category": [movie_category]})
        st.session_state.favorite_list = pd.concat([favorite_list_df, new_row], ignore_index=True)
    else:
        # Check if the movie title is not already in the DataFrame's "Title" column
        if movie_title not in favorite_list_df["Title"].values.tolist():
            new_row = pd.DataFrame({"Title": [movie_title], "Category": [movie_category]})
            st.session_state.favorite_list = pd.concat([favorite_list_df, new_row], ignore_index=True)
        else:
            st.warning(f"{movie_title} is already in the favorite list. Please add a different movie.")

# Function to add a movie to the watch-again list
def add_to_watch_again_list(movie_title, movie_category):
    watch_again_list_df = st.session_state.watch_again_list

    if "Title" not in watch_again_list_df.columns:
        # Initialize DataFrame with "Title" and "Category" columns
        watch_again_list_df = pd.DataFrame(columns=["Title", "Category"])

    # Check if the DataFrame is empty
    if watch_again_list_df.empty:
        new_row = pd.DataFrame({"Title": [movie_title], "Category": [movie_category]})
        st.session_state.watch_again_list = pd.concat([watch_again_list_df, new_row], ignore_index=True)
    else:
        # Check if the movie title is not already in the DataFrame's "Title" column
        if movie_title not in watch_again_list_df["Title"].values.tolist():
            new_row = pd.DataFrame({"Title": [movie_title], "Category": [movie_category]})
            st.session_state.watch_again_list = pd.concat([watch_again_list_df, new_row], ignore_index=True)
        else:
            st.warning(f"{movie_title} is already in the watch-again list. Please add a different movie.")

def convert_dataframe_to_arrow(df):
    df["Title"] = df["Title"].astype(str)  # Convert "Title" column to string data type
    for col in df.columns:
        if df[col].dtype == np.float64:
            # Convert float64 columns to float32 to be compatible with Arrow
            df[col] = df[col].astype(np.float32)
    return pa.Table.from_pandas(df)

# Function to display the MovieList page
def movie_list_page():
    st.title("Recommended Movies")
    recommended_movies = st.session_state.recommended_movies

    if not recommended_movies:
        st.write("No movie recommendations found.")
    else:
        for i, movie_title in enumerate(recommended_movies):
            st.write(f"{i + 1}. {movie_title}")

            # Buttons to add the movie to different lists
            col1, col2, col3 = st.columns(3)
            if col1.button(f"Add to Watchlist", key=f"watchlist_{i}"):
                add_to_watchlist(movie_title, "Category")  # Replace "Category" with the actual category
            if col2.button(f"Add to Favorite", key=f"favorite_{i}"):
                add_to_favorite_list(movie_title, "Category")  # Replace "Category" with the actual category
            if col3.button(f"Add to Watch Again", key=f"watch_again_{i}"):
                add_to_watch_again_list(movie_title, "Category")  # Replace "Category" with the actual category

    # Display watchlist, favorite list, and watch-again list data frames
    st.title("Watchlist")
    watchlist_df = st.session_state.watchlist
    watchlist_table = convert_dataframe_to_arrow(watchlist_df)
    st.dataframe(watchlist_table)

    st.title("Favorite List")
    favorite_list_df = st.session_state.favorite_list
    favorite_list_table = convert_dataframe_to_arrow(favorite_list_df)
    st.dataframe(favorite_list_table)

    st.title("Watch Again List")
    watch_again_list_df = st.session_state.watch_again_list
    watch_again_list_table = convert_dataframe_to_arrow(watch_again_list_df)
    st.dataframe(watch_again_list_table)

    if st.button("Rate and Review Movies in Watch Again List"):
        selected_movies = watch_again_list_df["Title"].tolist()
        st.session_state.selected_movies = selected_movies
        st.session_state.movie_to_rate_index = 0
        st.experimental_rerun()
    # Display ratings and reviews for movies in the "Watch Again" list
    st.title("Ratings and Reviews for Movies in Watch Again List")
    watch_again_rating_list = st.session_state.watch_again_rating_list
    if not watch_again_rating_list:
        st.write("No ratings and reviews available for movies in the Watch Again list.")
    else:
        for rating_data in watch_again_rating_list:
            st.write(f"Movie: {rating_data['Title']}")
            st.write(f"Rating: {rating_data['Rating']} stars")
            st.write(f"Review: {rating_data['Review']}")    

###############
# Function to add a movie to the DataFrame
# Function to load the data and create a CometML experiment
# Function to load the data and create a CometML experiment
def load_data_and_experiment(sys, fav_movies):
    # Load data and initialize lists
    title_list = load_movie_titles('resources/data/movies.csv')
    initialize_lists()

    # App declaration
    st.write("# Movie Recommender Engine")
    st.write("### EXPLORE Data Science Academy Unsupervised Predict")
    st.image('resources/imgs/Image_header.png', use_column_width=True)

    # ... (Rest of the code for the recommender system)

    # Create a CometML experiment and log metrics and model
    if sys == 'Content Based Filtering':
        if st.button("Recommend"):
            with st.spinner('Crunching the numbers...'):
                start_time = time.time()
                top_recommendations = content_model(movie_list=fav_movies, top_n=10)
                recommendation_time = time.time() - start_time

                # Log metrics in the experiment
                experiment.log_metric("Number of Recommendations", len(top_recommendations))
                experiment.log_metric("Recommendation Time", recommendation_time)

                # Log the trained model
                model = content_model(fav_movies, top_n=10)  # Assuming you return the trained model from content_model()
                experiment.log_model(model, "Content-Based Model")

                st.title("We think you'll like:")
                for i, j in enumerate(top_recommendations):
                    st.subheader(str(i + 1) + '. ' + j)
   
# App declaration
def main():
    
    movies_list = []

    ##################################
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = pd.DataFrame(columns=["Title", "Category"])

    if "favorite_list" not in st.session_state:
        st.session_state.favorite_list = pd.DataFrame(columns=["Title", "Category"])

    if "watch_again_list" not in st.session_state:
        st.session_state.watch_again_list = pd.DataFrame(columns=["Title", "Category"])

    if "watch_again_rating_list" not in st.session_state:
        st.session_state.watch_again_rating_list = []

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Movie List"
    #####################################
      
   # active_page = st.session_state.active_page
     # Initialize the recommended_movies list and movie_data DataFrame as global variables
    #Initialize session state variables
    if "movie_data" not in st.session_state:
        st.session_state.movie_data = pd.DataFrame(columns=["Title", "Category"])
    if "recommended_movies" not in st.session_state:
        st.session_state.recommended_movies = []


    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    #page_options = ["Welcome","Recommender System","Analysis","Solution Overview",'MovieList']
    page_options = ["Welcome","Meet our team", "Recommender System", "Solution Overview", "MovieList","Rating & Review"]
    st.session_state.page_selection = st.sidebar.selectbox("Choose Option", page_options)
    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
   # page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if st.session_state.page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))
        

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)
            st.markdown('<style>@keyframes blink {0% {opacity: 1;} 50% {opacity: 0.2;} 100% {opacity: 1;}}</style>', unsafe_allow_html=True)

            if st.button("Recommend"):
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                        add_recommended_movies(top_recommendations)
                    st.title("The best you'll like:")
                    for i, (movie_title, genres, rating) in enumerate(top_recommendations):
                       st.subheader(f"{i + 1}. {movie_title}")
                       st.write(f"Genres: {genres}")

                       if rating is not None:
                         st.write(f"Average Rating: {rating:.2f} stars")
                       else:
                          st.write("No ratings available.")
                    
                       st.write("--------------------")
                       

        if sys == 'Collaborative Based Filtering':
            st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)
            st.markdown('<style>@keyframes blink {0% {opacity: 1;} 50% {opacity: 0.2;} 100% {opacity: 1;}}</style>', unsafe_allow_html=True)

            if st.button("Recommend"):
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                        add_recommended_movies(top_recommendations)
                    st.title("We think you'll like:")
                    for i, (movie_title, genres,predicted_rating) in enumerate(top_recommendations):
                       st.subheader(f"{i + 1}. {movie_title}")
                       st.write(f"Genres: {genres}")
                       st.write(f"Predicted Rating: {predicted_rating:.2f} stars")
                     # Display the stars using st.write()
                       full_stars = int(round(predicted_rating))
                       half_star = round(predicted_rating - full_stars) == 0.5
                       stars_html = ''.join([
                                             f'<span style="color:gold; animation: blink 1s infinite;">★</span>' for _ in range(full_stars)
                                                                                                             ])
                       if half_star:
                              stars_html += '<span style="color:gold; animation: blink 1s infinite; font-family: FontAwesome;">&#xf089;</span>'
                       st.markdown(stars_html, unsafe_allow_html=True)

                       st.write(f"Predicted Rating: {predicted_rating:.2f} stars")
                       
    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
     #html_template = """
     #   <div style="background-color:black;padding:10px;border-radius:10px;margin:10px;">
     #   <h1 style="color:Blue;text-align:center;">EDSA Movie Recommendation Challenge</h1>
      #  </div>
        

    if st.session_state.page_selection == "Welcome":
        st.title("Welcome to the Data Detectives: ReelWise app")
        
        # Display the image
        #st.image('resources/imgs/Home.jpg', use_column_width=True)
        st.image('resources/imgs/Data_Detectives_Logo-removebg-preview.png', 
                 #caption="Photo Credit: Hello I'm, Data Detective",
                 use_column_width=True)
        
        # Display formatted text using Markdown
        st.markdown("""
        # ReelWise App
        
        Welcome to our Movie Recommender App! We hope you'll find some great movie recommendations here.
        
        ### How it works:
        
        1. Select your three favorite movies from the drop-down lists.
        2. Choose either Content Based Filtering or Collaborative Based Filtering.
        3. Click the "Recommend" button to get personalized movie recommendations.
        
        
        
        Happy movie watching!
        """)
        # Display the second image
        st.image('resources/imgs/Image2.png', use_column_width=True)
        
        # Display the third image
        st.image('resources/imgs/Image3.jpg', use_column_width=True)
        
        # Display the fourth image
        st.image('resources/imgs/Image4.jpg', use_column_width=True)

   
        
    if st.session_state.page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.
    if st.session_state.page_selection == "MovieList":
        initialize_lists()
        movie_list_page()
    if st.session_state.page_selection == "Rating & Review":
        rating_page()
    if st.session_state.page_selection == "Meet our team":
        #st.title("Data Detective team")
        st.subheader("Meet the Data Detectives Team")
        #st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("",unsafe_allow_html=True)
        #st.write("  ")
        st.markdown(
            """
            <style>
            .center {
                display: flex;
                justify-content: center;
                margin-top: -100px; /* Adjust the value to shift the image as desired */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Display the image with the 'center' class
        # st.image('resources/imgs/Data_Detectives_Logo-removebg-preview.png', 
                 #caption="Photo Credit: Hello I'm, Data Detective",
                 #use_column_width=True)
        

        team_members = {
        #"Team Member 1": "Data Science Lead\nResponsible for overseeing data science projects and guiding the team to deliver effective solutions.",
        "Maseru": "Machine Learning Engineer\nDeveloping and implementing machine learning models for various projects.",
        "AyandaN": "Data Analyst\nAnalyzing and interpreting data to provide insights for business decisions.",
        "Thebe": "Data Engineer\nBuilding and maintaining the data infrastructure and pipelines for data processing.",
        "Vasco": "AI Researcher\nExploring cutting-edge AI techniques and conducting research to improve the team's capabilities.",
        "Katsila": "Data Visualization Specialist\nCreating interactive and informative data visualizations to communicate insights effectively.",
        "AyandaW": "Natural Language Processing (NLP) Specialist\nWorking on NLP projects and developing language models for text analysis.",
    }
        st.image('resources/imgs/Moshibudi.png', caption="Moshibudi: Team Lead", width=200)
        st.write("Team Lead: Responsible for overseeing data science projects, providing technical guidance to the team, and ensuring the successful delivery of data-driven solutions. They collaborate with stakeholders to define project objectives, lead model development, and interpret results for actionable insights.")
        css_style = """
        <style>
        .image-with-description {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .image-with-description img {
            width: 200px;
            height: 100px; /* Set the desired height for the image */
            object-fit: cover;
            border-radius: 50%;
        }
        </style>
        """
        #st.markdown(css_style, unsafe_allow_html=True)


        left_description = True
        # Create two columns for the second row
        col1, col2 = st.columns(2)
        for idx, (team_member, job_description) in enumerate(team_members.items()):
            col1, col2 = st.columns([1, 2])

            if idx % 2 == 0:
                # Even index, description on the left, image on the right
                with col1:
                    st.markdown("<br><br><br>", unsafe_allow_html=True)
                    #st.write("Job Description:")
                    st.write(job_description)
                    st.markdown("<br><br><br>", unsafe_allow_html=True)
                with col2:
                    st.markdown("<br><br><br>", unsafe_allow_html=True)
                    st.image(f'resources/imgs/{team_member.split()[0]}.png', caption=team_member, width=200)
                    #st.markdown("<br><br><br>", unsafe_allow_html=True)
            else:
                # Odd index, image on the left, description on the right
                with col1:
                    
                    st.image(f'resources/imgs/{team_member.split()[0]}.png', caption=team_member, width=200)
                    
                with col2:
                    st.markdown("<br><br><br>", unsafe_allow_html=True)
                    #st.write("Job Description:")
                    st.write(job_description)
                    st.markdown("<br><br><br>", unsafe_allow_html=True)    


if __name__ == '__main__':
    main()
