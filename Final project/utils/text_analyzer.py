from transformers import AutoTokenizer,AutoModelForSequenceClassification, pipeline
import torch

class TextAnalyzer:
    def __init__(self):
        self.stag_tokenizer = AutoTokenizer.from_pretrained("MonoHime/rubert-base-cased-sentiment-new")
        self.stag_model = AutoModelForSequenceClassification.from_pretrained("MonoHime/rubert-base-cased-sentiment-new")
        self.label_model = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

    def analyze_content(self, content:str):
        """
        Analyze post content and return sentiment and label.
        """
        placeholder_labels = ["видеоигры", "компьютеры", "люди", "технологии", "медиа"]
        output = self.label_model(content, placeholder_labels, multi_label=True)


        return output['labels'][0]
    def get_sentiment(self, content:str):
        labels = ["Positive", "Negative", "Neutral"]
        inputs = self.stag_tokenizer(content, padding=True, return_tensors="pt")

        with torch.no_grad():
            outputs = self.stag_model(**inputs)

        predicted_stag = torch.argmax(outputs.logits).item()
        return labels[predicted_stag]
    def update_post(self,posts:list[dict])->list[dict]:
        for post in posts:
            post["semantic_tag"] = self.get_sentiment(post["text"])
            post["topic"] = self.analyze_content(post["text"])
        return posts


