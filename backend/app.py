import os
import random 
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

# check if api key is there
if not API_KEY:
    raise ValueError("TMDB_API_KEY is not set in the environment variables, please set it in the .env file.")

# out of the 500 pages, select a random one
random_page = random.randint(1, 500)

url = "https://api.themoviedb.org/3/discover/movie"
params = {
    "api_key": API_KEY,
    "language": "en-US",
    "page": random_page,
    "include_adult": "false",
    "vote_count.gte": 100,  # ensures the movies actually have reviews
}

response = requests.get(url,params=params)

if response.status_code == 200:
  data = response.json()  # Converts the raw text into a Python dictionary
  movie_list = data.get("results", [])

  if movie_list:
    movie = random.choice(movie_list)  # pick random movie from list

    print(f"Title: {movie['title']}")

  else:
    print("No movies found on this page.")
else:
  print(f"Error fetching data: {response.status_code}")