from utils.html_parser import TelegramHTMLParser
from utils.text_analyzer import TextAnalyzer
from utils.file_handler import FileHandler
import pandas as pd # for test

def process_posts(html_path: str):
    """Read the html files and analyze the text content to produce csv output"""
    parser = TelegramHTMLParser()
    analyzer = TextAnalyzer()
    handler = FileHandler() # NOT IMPLEMENTED YET

    posts = parser.parse_html_files(html_path)
    # List of Dictionaries creation
    posts = analyzer.update_post(posts[:15])

    df = handler.create_df(posts)
    df.to_csv("output.csv")
def visualize_posts(csv_path: str):
    handler = FileHandler()
    plt = handler.create_semantic_timeline(csv_path)
    plt.savefig("timeline.png")

html_path = 'messages.html'
csv_path = "output.csv"

# process_posts(html_path)
visualize_posts(csv_path)