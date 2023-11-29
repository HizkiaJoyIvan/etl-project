import pandas as pd

def transform_trends(trends_filename, spotify_filename):
    trends_df = pd.read_csv(trends_filename)

    # Reshape the DataFrame to have a column for each date range
    melted_df = pd.melt(trends_df, id_vars='query', var_name='date_range', value_name='count')
    return melted_df

def transform_spotify(filename):
    df = pd.read_csv(filename)
    bins = [0, 40, 70, 100]
    labels = ['low', 'medium', 'high']

    df['duration'] = df['duration'] / 60000
    df['popularity_category'] = pd.cut(df['popularity'], bins=bins, labels=labels)

    return df

result_df = transform_trends("extracted_trends_data.csv", "extracted_spotify_data.csv")
print(result_df)