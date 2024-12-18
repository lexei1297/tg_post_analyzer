import pandas as pd
from matplotlib import pyplot as plt

class FileHandler:
    def __init__(self):
        pass
    def create_df(self, posts:list)-> pd.DataFrame:
        df = pd.DataFrame(posts)
        df = df[["date", "semantic_tag", "topic"]]
        return df
    def create_semantic_timeline(self, csv_path)->plt:
        df = pd.read_csv(csv_path)

        semantic_map = {'Negative': -1, 'Neutral': 0, 'Positive': 1}

        df['semantic_tag'] = df['semantic_tag'].map(semantic_map)

        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')

        daily_sum = df.groupby('date')[
            'semantic_tag'].sum().reset_index()  # use reset_index to convert the date into a column

        full_of_date = pd.date_range(start=daily_sum['date'].min(),
                                         end=daily_sum['date'].max())
        daily_sum = daily_sum.set_index('date').reindex(full_of_date,
                                                         fill_value=0).reset_index()
        daily_sum.columns = ['Date', 'Semantic Tag Sum']

        plt.figure(figsize=(15, 5))
        plt.plot(daily_sum['Date'], daily_sum['Semantic Tag Sum'], marker='o', color="black")
        plt.title('Semantic Tag Timeline', fontweight="bold")
        plt.xlabel('date', fontweight="bold")
        plt.ylabel('Semantic Tag Sum', fontweight="bold")
        plt.xticks(daily_sum['Date'], rotation=45)
        plt.tight_layout()
        return plt

