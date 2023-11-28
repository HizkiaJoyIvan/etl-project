import pandas as pd

def transform(data):
    bins = [0, 40, 70, 100]
    labels = ['low', 'medium', 'high']

    data['duration'] = data['duration'] / 60000
    data['popularity_category'] = pd.cut(data['popularity'], bins=bins, labels=labels)

    return data