import pandas as pd

def transform_trends(filename):
    trends_df = pd.read_csv(filename)

    melted_df = pd.melt(trends_df, id_vars='query', var_name='date_range', value_name='count')
    
    # Extracting date range values as integers for comparison
    melted_df['date_range_start'] = melted_df['date_range'].str.extract(r'(\d+)')
    
    # Finding the lowest and highest values along with their date ranges
    lowest_values = melted_df.groupby('query')['count'].idxmin()
    highest_values = melted_df.groupby('query')['count'].idxmax()
    
    lowest_df = melted_df.loc[lowest_values, ['query', 'count', 'date_range']]
    lowest_df = lowest_df.rename(columns={'count': 'lowest_value', 'date_range': 'lowest_value_date_range'})
    
    highest_df = melted_df.loc[highest_values, ['query', 'count', 'date_range']]
    highest_df = highest_df.rename(columns={'count': 'highest_value', 'date_range': 'highest_value_date_range'})
    
    # Merging the lowest and highest value dataframes
    result_df = pd.merge(melted_df, lowest_df, on='query', how='left')
    result_df = pd.merge(result_df, highest_df, on='query', how='left')
    
    # Dropping unnecessary columns
    result_df = result_df[['query', 'lowest_value', 'lowest_value_date_range', 'highest_value', 'highest_value_date_range']]

    result_df['query'] = result_df['query'].str.rstrip('lirik').str.strip()
    # Drop duplicates
    result_df = result_df.drop_duplicates()
    
    return result_df

def transform_spotify(filename):
    df = pd.read_csv(filename)
    bins = [0, 40, 70, 100]
    labels = ['low', 'medium', 'high']

    df['duration'] = df['duration'] / 60000
    df['popularity_category'] = pd.cut(df['popularity'], bins=bins, labels=labels)

    # Remove text inside parentheses in the 'name' column
    df['name'] = df['name'].str.replace(r'\([^)]*\)', '', regex=True)
    
    # Remove text after hyphens in the 'name' column
    df['name'] = df['name'].str.split(' - ', n=1).str[0]

    df['name'] = df['name'].str.lower().str.strip()

    return df

def transform_merge(spotify_df, trends_df):
    # Clean the 'query' column in trends_df
    
    # Merging based on the "name" column from spotify_df and "query" column from trends_df
    merged_df = spotify_df.merge(trends_df, left_on='name', right_on='query', how='left')


    return merged_df

