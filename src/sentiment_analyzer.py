# src/sentiment_analyzer.py
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure NLTK resources are available (usually handled in a central setup/pipeline)
# For the sake of this component, we assume NLTK resources are installed.

class SentimentAnalyzer:
    """
    Applies lexicon-based sentiment analysis (TextBlob or VADER) and classification.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Initialize VADER analyzer once
        self.sia = SentimentIntensityAnalyzer()
    
    # --- Helper Methods for Classification ---
    
    def _polarity_to_label_tb(self, p: float) -> str:
        """Classifies TextBlob polarity score."""
        if p > 0.1:
            return "Positive"
        elif p < -0.1:
            return "Negative"
        else:
            return "Neutral"

    def _polarity_to_label_vader(self, c: float) -> str:
        """
        Classifies VADER compound score using standard thresholds.
        """
        if c >= 0.05:
            return "Positive"
        elif c <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    # --- Core Analysis Methods ---

    def analyze_textblob(self) -> pd.DataFrame:
        """
        Computes TextBlob polarity and assigns the final sentiment label.
        """
        print("Starting sentiment analysis using TextBlob...")
        
        # Calculate Polarity and Subjectivity
        self.df["tb_polarity"] = self.df["review_text"].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )
        self.df["tb_subjectivity"] = self.df["review_text"].apply(
            lambda x: TextBlob(str(x)).sentiment.subjectivity
        )
        
        # Assign Sentiment Label
        self.df["tb_sentiment"] = self.df["tb_polarity"].apply(self._polarity_to_label_tb)
        
        print("TextBlob analysis complete.")
        return self.df

    def analyze_vader(self) -> pd.DataFrame:
        """
        Computes VADER compound score and assigns the final sentiment label.
        """
        print("Starting sentiment analysis using VADER...")
        
        def vader_compound(text):
            # Ensure text is treated as a string to prevent errors
            return self.sia.polarity_scores(str(text))["compound"]
            
        # VADER compound score
        self.df["vader_compound"] = self.df["review_text"].apply(vader_compound)
        
        # Assign Sentiment Label
        self.df["vader_sentiment"] = self.df["vader_compound"].apply(self._polarity_to_label_vader)
        
        print("VADER analysis complete.")
        return self.df