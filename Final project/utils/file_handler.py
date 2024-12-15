import pandas as pd


class FileHandler:
    def save_to_csv(self, df, output_path):
        """
        Save DataFrame to CSV file.
        """
        df.to_csv(output_path, index=False, encoding="utf-8")
