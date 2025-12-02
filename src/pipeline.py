import os
import pandas as pd
import numpy as np

# --- Import Configuration ---
# from config import DATA_PATHS 

# --- Import Modular Components ---
from preprocessor import ReviewPreprocessor
from sentiment_analyzer import SentimentAnalyzer
from thematic_analyzer import ThematicAnalyzer

# Input: Output of Task 1 clean data
CLEANED_INPUT_PATH = 'data/processed/reviews_processed.csv'
# Output: Final results for Task 2
FINAL_OUTPUT_PATH ='data/processed/reviews_final.csv'

df = pd.read_csv('data/processed/reviews_processed.csv')
df.head()

def run_analysis_pipeline():
    """
    Orchestrates the data analysis flow using class components.
    """
    print("--- Starting Review Data Analysis Pipeline ---")
    
    # 1. Load Data (Task 1 Output)
    try:
        # DataPreprocessor.load_data is assumed to handle the path successfully
        # df = ReviewPreprocessor.load_data(CLEANED_INPUT_PATH)
        df = pd.read_csv(CLEANED_INPUT_PATH)
        df.head()
    except FileNotFoundError as e:
        print(e)
        return


    # 2. Sentiment Analysis (Task 2 - VADER)
    # Assumes analyze_vader() creates 'vader_compound' and 'vader_sentiment'
    sentiment_processor = SentimentAnalyzer(df=df.copy())
    df_with_sentiment = sentiment_processor.analyze_vader()
    
    # 3. Thematic Analysis (Task 2 - Rule-Based)
    thematic_processor = ThematicAnalyzer(df=df_with_sentiment)
    
    # Run TF-IDF setup (preprocesses text, calculates keywords)
    thematic_processor.extract_keywords_tfidf() 
    
    # Assign themes (creates the 'theme' column)
    df_final_analyzed = thematic_processor.assign_themes(top_k=1)

    # 4. Final Column Standardization and Save
    print("\n4. Saving Final Analysis Output...")
    
    # Select and rename columns for the final file/database load
    output_df = df_final_analyzed[[
        'review_id', 
        'review_text',             # Raw review text
        'vader_sentiment',    # Sentiment label
        'vader_compound',     # Sentiment score
        'theme',              # Rule-based theme
        'rating',
        'bank_name'
    ]].rename(columns={

        'vader_sentiment': 'sentiment_label',
        'vader_compound': 'sentiment_score'
    })

    # Save the final results to CSV using the path from config.py
    # os.path.dirname handles the path structure correctly (e.g., '../data/processed')
    os.makedirs(os.path.dirname(FINAL_OUTPUT_PATH), exist_ok=True)
    output_df.to_csv(FINAL_OUTPUT_PATH, index=False)
    print(f"✅ Pipeline Complete. Final results saved to {FINAL_OUTPUT_PATH}")

if __name__ == "__main__":
    run_analysis_pipeline()