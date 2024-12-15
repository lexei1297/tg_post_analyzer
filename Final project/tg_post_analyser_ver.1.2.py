import os
from utils.html_parser import TelegramHTMLParser
from utils.text_analyzer import TextAnalyzer
from utils.file_handler import FileHandler
import pandas as pd


class TelegramPostAnalyzer:
    def __init__(self, input_path, output_csv, method="bag_of_words", timeline_category=None):
        self.input_path = input_path
        self.output_csv = output_csv
        self.method = method
        self.timeline_category = timeline_category
        self.parser = TelegramHTMLParser()
        self.analyzer = TextAnalyzer(method=method)
        self.file_handler = FileHandler()

    def process_posts(self):
        try:
            # Parse HTML files
            posts = self.parser.parse_html_files(self.input_path)
            print(f"Successfully parsed {len(posts)} posts.")

            # Analyze and classify posts
            results = []
            for post in posts:
                date, content = post["date"], post["content"]
                sentiment, label = self.analyzer.analyze_content(content)
                results.append({"Date": date, "Semantic tag": sentiment, "Label": label})

            # Create and save CSV
            df = pd.DataFrame(results)
            self.file_handler.save_to_csv(df, self.output_csv)
            print(f"Results saved to {self.output_csv}")

            # Generate timeline if requested
            if self.timeline_category:
                self.generate_timeline(df)

        except Exception as e:
            print(f"Error during processing: {e}")

    def generate_timeline(self, df):
        try:
            # Filter by category and calculate timeline
            category_data = df[df["Label"] == self.timeline_category]
            timeline = (
                category_data.groupby("Date")
                .agg(
                    semantic_tag_sum=("Semantic tag", lambda x: sum(["POSITIVE", "NEUTRAL", "NEGATIVE"].index(i) - 1 for i in x)),
                    most_frequent_label=("Label", lambda x: x.mode()[0]),
                )
                .reset_index()
            )
            timeline_csv = f"output/timeline_{self.timeline_category}.csv"
            self.file_handler.save_to_csv(timeline, timeline_csv)
            print(f"Timeline saved to {timeline_csv}")

        except Exception as e:
            print(f"Error during timeline generation: {e}")


def main():
    print("Welcome to the Telegram Post Analyzer!")

    # Manual input for parameters
    input_path = input("Enter the path to input HTML file or folder: ").strip()
    while not os.path.exists(input_path):
        print("Invalid path. Please enter a valid path.")
        input_path = input("Enter the path to input HTML file or folder: ").strip()

    output_csv = input("Enter the path to output CSV file: ").strip()

    # Input and validation for the method
    method = input(
        "Choose a classification method (bag_of_words, topic_classifier, zero_shot) [default: bag_of_words]: "
    ).strip()
    if method not in ["bag_of_words", "topic_classifier", "zero_shot"]:
        if method == "":
            print("No method specified. Defaulting to 'bag_of_words'.")
            method = "bag_of_words"
        else:
            print(f"Invalid method '{method}'. Defaulting to 'bag_of_words'.")
            method = "bag_of_words"

    timeline_category = input("Enter a timeline category (optional, leave blank to skip): ").strip()
    if not timeline_category:
        timeline_category = None

    # Initialize the analyzer
    analyzer = TelegramPostAnalyzer(
        input_path=input_path,
        output_csv=output_csv,
        method=method,
        timeline_category=timeline_category,
    )
    analyzer.process_posts()


if __name__ == "__main__":
    main()
