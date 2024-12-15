# tg_post_analyzer
Python CLI application that processes Telegram channel exports in HTML format, analyzes their content, and produces a CSV report. The solution uses Python's OOP principles and includes error handling, clear structure, and explanations.

Installation:

    pip install -r requirements.txt

Usage:

    python tg_post_analyzer.py 
    --input "path_to_html_or_folder" 
    --output "output.csv" 
    --method "bag_of_words" 
    --timeline "sport"

Example:

    Input: Telegram HTML files.
    Output: Date,Semantic tag,Label
    2024/11/15,POSITIVE,sport

Dependencies:

    beautifulsoup4
    sklearn (scilab-learn)
    transformers
    argsparse
    os
    pandas
    numpy
    joblib

Models: 

    Place models in the models folder.

Features:

    Flexible classification methods (bag_of_words, topic_classifier, zero_shot).
    Robust error handling and logging.
    Timeline generation for specific categories.

