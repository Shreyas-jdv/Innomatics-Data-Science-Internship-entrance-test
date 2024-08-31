
import pandas as pd

# Load the CSV files
ratings_df = pd.read_csv('D:/Shreyas data/My Downloads/movie_data/ratings.csv')
movies_df = pd.read_csv('D:/Shreyas data/My Downloads/movie_data/movies.csv')
tags_df = pd.read_csv('D:/Shreyas data/My Downloads/movie_data/tags.csv')


# Load the datasets
ratings = pd.read_csv('ratings.csv')        # Columns: userId, movieId, rating
movies = pd.read_csv('movies.csv')          # Columns: movieId, title, genre
imdb_ratings = pd.read_csv('imdb_ratings.csv')  # Columns: movieId, imdb_rating
tags = pd.read_csv('tags.csv')               # Columns: userId, movieId, tag

# 1. Apply the mandatory operations

# Group ratings by movieId and calculate count and mean
ratings_grouped = ratings.groupby('movieId').agg({'rating': ['count', 'mean']})
ratings_grouped.columns = ['rating_count', 'rating_mean']

# Merge with movies dataframe
movies_with_ratings = movies.merge(ratings_grouped, on='movieId', how='inner')

# Filter movies with more than 50 ratings
movies_filtered = movies_with_ratings[movies_with_ratings['rating_count'] > 50]

# Merge with IMDb ratings dataframe
movies_filtered_with_imdb = movies_filtered.merge(imdb_ratings, on='movieId', how='inner')

# 2. Find the movie with the highest IMDb rating
highest_imdb_movie = movies_filtered_with_imdb.loc[movies_filtered_with_imdb['imdb_rating'].idxmax()]
highest_imdb_movie_id = highest_imdb_movie['movieId']
print(f"The movieId with the highest IMDb rating is: {highest_imdb_movie_id}")

# 3. Find the Sci-Fi movie with the highest IMDb rating
# Filter Sci-Fi movies
sci_fi_movies = movies[movies['genre'].str.contains('Sci-Fi', case=False, na=False)]

# Merge Sci-Fi movies with IMDb ratings
sci_fi_movies_with_imdb = sci_fi_movies.merge(imdb_ratings, on='movieId', how='inner')

# Merge with the filtered movies
sci_fi_movies_with_ratings = sci_fi_movies_with_imdb.merge(ratings_grouped, on='movieId', how='inner')

# Find the movie with the highest IMDb rating in Sci-Fi movies
highest_sci_fi_imdb_movie = sci_fi_movies_with_ratings.loc[sci_fi_movies_with_ratings['imdb_rating'].idxmax()]
highest_sci_fi_imdb_movie_id = highest_sci_fi_imdb_movie['movieId']
print(f"The movieId of the Sci-Fi movie with the highest IMDb rating is: {highest_sci_fi_imdb_movie_id}")

# 4. Find the top 5 popular movies based on the number of user ratings
top_5_movies = movies_filtered_with_imdb.sort_values(by='rating_count', ascending=False).head(5)
print("Top 5 popular movies based on number of user ratings:")
print(top_5_movies[['movieId', 'title', 'rating_count']])

# 5. Find the third most popular Sci-Fi movie based on number of user ratings
sci_fi_movies_with_ratings_sorted = sci_fi_movies_with_ratings.sort_values(by='rating_count', ascending=False)
third_most_popular_sci_fi_movie_id = sci_fi_movies_with_ratings_sorted.iloc[2]['movieId']
print(f"The movieId of the third most popular Sci-Fi movie based on the number of user ratings is: {third_most_popular_sci_fi_movie_id}")

# 6. Find the tags for "Matrix, The (1999)"
# Identify the movieId for "Matrix, The (1999)"
matrix_id = movies[movies['title'] == 'Matrix, The (1999)']['movieId'].values[0]

# Filter the tags for this movieId
matrix_tags = tags[tags['movieId'] == matrix_id]['tag'].unique()
print("Tags for 'Matrix, The (1999)':")
print(matrix_tags)

# 7. Calculate the average user rating for "Terminator 2: Judgment Day (1991)"
# Identify the movieId for "Terminator 2: Judgment Day (1991)"
terminator_id = movies[movies['title'] == 'Terminator 2: Judgment Day (1991)']['movieId'].values[0]

# Filter the ratings for this movieId
terminator_ratings = ratings[ratings['movieId'] == terminator_id]['rating']

# Calculate the average rating
average_rating = terminator_ratings.mean()
print(f"The average user rating for 'Terminator 2: Judgment Day (1991)' is: {average_rating}")
