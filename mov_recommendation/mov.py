import streamlit as st
import pandas as pd
import pickle
import requests
import base64

# TMDB API Key
TMDB_API_KEY = "904b3e396ca693edf8ddab02de78bd76"  # Replace with your actual TMDB API key

# Function to get movie poster from TMDB


st.set_page_config(page_title="Movie App", page_icon="lo.png", layout="wide")
# Function to convert the image to Base64 encoding
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Convert the local image to Base64
background_img = get_img_as_base64("back1.jpg")
# Inject CSS into the Streamlit app
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{background_img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
.st-emotion-cache-1104ytp {{
    font-family: "Source Sans Pro", sans-serif;
    font-size: 1rem;
    margin-bottom: -1rem;
    color: rgb(255 255 255);
}}
p, ol, ul, dl {{
    margin: 0px 0px 1rem;
    padding: 0px;
    font-size: 1rem;
    color: white;
    font-weight: 400;
}}
.st-emotion-cache-1r4qj8v {{
    position: absolute;
    background: rgb(255 121 121);
    color: rgb(49, 51, 63);
    inset: 0px;
    color-scheme: light;
    overflow: hidden;
    color: black;
    content-visibility: visible;
}}




</style>
"""


        
   


# Apply the CSS
st.markdown(page_bg_img, unsafe_allow_html=True)



def Line_Break(width=100):
    line_code = f"""
    <hr style="border: none; height: 2px; width: {width}%; 
        background: linear-gradient(90deg, rgba(216,82,82,1) 13%, rgba(237,242,6,1) 57%, rgba(226,0,255,1) 93%); 
        margin: 0 auto;" />
    """
    st.markdown(line_code, unsafe_allow_html=True)

def Line_Break_start(width=100):
    line_code = f"""
    <hr style="border: none; height: 2px; width: {width}%; 
        background: linear-gradient(90deg, rgba(216,82,82,1) 13%, rgba(237,242,6,1) 57%, rgba(226,0,255,1) 93%);" />
    """
    st.markdown(line_code, unsafe_allow_html=True)

def heading(heading="h1", color="black", text="Default Heading"):
    heading_code = f"""
    <{heading} style='text-align: center; color: {color};'>{text}</{heading}>
    """
    st.markdown(heading_code, unsafe_allow_html=True)




# Add custom CSS to style the sidebar
st.markdown(
    """
    <style>

            [data-testid="stHeader"] {
            display: none;
        
        }


           [data-testid="stSidebar"] {
            background-color: #388ecb; /* Example background color */
            border: 2px solid white; /* Add white border */
            border-radius: 10px; /* Optional: Add rounded corners */
            padding: 10px; /* Optional: Add padding for spacing */
        }
    

    
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
with st.sidebar:
    st.image("lo.png", use_container_width=True)
    
    # Displaying the subheader with custom styling
    st.markdown(
    '<p style="color:white; font-size:16px; font-weight:bold;"><i>Movie Recommendation System</i></p>', 
    unsafe_allow_html=True
)
    

    # HTML and CSS for the GitHub button
    github_button_html = """
    <div style="text-align: center; margin-top: 50px;">
        <a class="button" href="https://github.com/Munsif311" target="_blank" rel="noopener noreferrer">Visit my GitHub</a>
    </div>

    <style>
        /* Button styles */
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #ffc107;
            color: black;
            text-decoration: none;
            border-radius: 20px;
            text-align: center;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #000345;
            color: white;
            text-decoration: none; /* Remove underline on hover */
        }
    </style>
    """

    # Display the GitHub button in the sidebar
    st.markdown(github_button_html, unsafe_allow_html=True)
    
    # Footer HTML and CSS
    footer_html = """
    <div style="padding:10px; text-align:center;margin-top: 10px;">
        <p style="font-size:20px; color:white;">Created by Munsif Khan</p>
    </div>
    """

    # Display footer in the sidebar
    st.markdown(footer_html, unsafe_allow_html=True)



def get_movie_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            poster_path = data["results"][0]["poster_path"]
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None  # Return None if no poster found

# Load the data
with open("data.pkl", "rb") as file:
    mydata = pickle.load(file)  # This should be a DataFrame
with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)  # This is a similarity matrix

# Extract movie titles as a list
movie_list = mydata['title'].tolist()

# Streamlit UI
st.title(" Movie Recommendation System")

select_movie = st.selectbox(
    "Which movie do you select?",
    movie_list
)

# Recommendation function
def recommend(movie):
    try:
        # Find the index of the selected movie
        index = mydata[mydata["title"] == movie].index[0]
        distances = similarity[index]  # Get similarity scores

        sorted_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

        recommended_movies = []
        recommended_movies_poster = []
        
        for i in sorted_movies[1:6]:  # Get top 5 similar movies
            title = mydata.iloc[i[0]]["title"]
            recommended_movies.append(title)  # Fetch movie titles
            
            recommended_movies_poster.append(get_movie_poster(title))  # Fetch poster URLs
        
        return recommended_movies, recommended_movies_poster

    except IndexError:
        return ["Movie not found in dataset."], []

# Display recommendations
  # Custom CSS for button styling
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #ff5733; /* Change button background */
        color: white; /* Change text color */
        border-radius: 10px; /* Rounded corners */
        font-size: 18px; /* Increase font size */
        padding: 10px 20px; /* Adjust padding */
    }
    div.stButton > button:hover {
        background-color: #ff2e00; /* Change button color on hover */
    }
    </style>
""", unsafe_allow_html=True)

if st.button("🎬 Recommend Movies"):
    recommendation, posters = recommend(select_movie)
    
    # Show recommendations with posters
    cols = st.columns(5)  # Create 5 columns for 5 recommended movies
    
    for i in range(len(recommendation)):
        with cols[i]:  # Display in separate columns
            st.text(recommendation[i])  # Movie title
            if posters[i]:  # Check if poster exists
                st.image(posters[i], width=120)  # Show poster
            else:
                st.write("No Poster Found")
