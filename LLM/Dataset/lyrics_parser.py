import pandas as pd

if __name__ == "__main__":
    # Read the large CSV file
    large_dataset = pd.read_csv('all_song_lyrics.csv')

    # Define the main genres
    main_genres = ['pop', 'rap', 'rock', 'rb', 'country']

    # Create a dictionary to store DataFrames for each genre
    genre_dataframes = {genre: pd.DataFrame(columns=large_dataset.columns) for genre in main_genres}
    genre_dataframes['other'] = pd.DataFrame(columns=large_dataset.columns)

    # Group the data by the "tag" column and iterate through groups
    for tag, group in large_dataset.groupby('tag'):
        tag_lower = tag.lower()
        if tag_lower in main_genres:
            genre_dataframes[tag_lower] = pd.concat([genre_dataframes[tag_lower], group])
        else:
            genre_dataframes['other'] = pd.concat([genre_dataframes['other'], group])

    # Save each genre-specific DataFrame to a separate CSV file
    for genre, dataframe in genre_dataframes.items():
        dataframe.to_csv(f'{genre}_lyrics.csv', index=False)