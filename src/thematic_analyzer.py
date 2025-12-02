import pandas as pd
# Add the necessary imports for Gensim and NLTK
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
import nltk
from nltk.corpus import stopwords
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import LatentDirichletAllocation

# --- Ensure NLTK resources are available  ---
try:
    # Attempt download only if necessary, but this should ideally be in requirements setup
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')


class ThematicAnalyzer:
    """
    Performs TF-IDF for keyword extraction and rule-based thematic clustering.
    """
    # Documented grouping logic as required by the challenge
    THEME_MAPPINGS = {
        'Transaction Performance': ['slow', 'loading', 'transfer', 'delay', 'pending', 'stuck', 'money sent', 'transaction'],
        'App Stability & Bugs': ['crash', 'error', 'update', 'login error', 'bug', 'hang', 'fail'],
        'Account Access & Security': ['login', 'fingerprint', 'password', 'locked', 'otp', 'user name', 'security', 'username'],
        'User Experience (UI/Design)': ['ui', 'design', 'easy to use', 'confusing', 'user friendly', 'layout', 'simple']
    }

    def __init__(self, df):
        self.df = df
        
    def _preprocess_text(self, text: str) -> str:
        """
        Simple preprocessing for TF-IDF: lower-casing, removing digits, URLs, and punctuation.
        """
        if pd.isna(text) or not isinstance(text, str):
            return ""

        text = text.lower() 
        # Remove digits, URLs, excessive punctuation
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^\w\s]', ' ', text) # keep only alphanum + space
        text = re.sub(r'\s+', ' ', text).strip()
        return text
      
    def extract_keywords_tfidf(self):
            """
            Applies cleaning, creates the TF-IDF matrix, and calculates mean keyword scores.
            """
            print("Preprocessing text for TF-IDF...")
      
            # 1. Apply cleaning (assuming 'review' is the source column)
            self.df['cleaned_review'] = self.df['review_text'].apply(self._preprocess_text)
            
            # 2. Initialize and Fit TF-IDF Vectorizer
            tfidf_vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=5, max_df=0.85)
            X_tfidf = tfidf_vec.fit_transform(self.df["cleaned_review"])
            
            # 3. Calculate Mean TF-IDF Scores (The core analysis)
            tfidf_means = np.asarray(X_tfidf.mean(axis=0)).flatten()
            vocab_tfidf = np.array(tfidf_vec.get_feature_names_out())
            
            # 4. Create and Store the Resulting DataFrame
            self.tfidf_df = pd.DataFrame({"word": vocab_tfidf, "tfidf": tfidf_means})
            self.tfidf_df = self.tfidf_df.sort_values("tfidf", ascending=False).reset_index(drop=True)
          
            print(f"TF-IDF analysis complete. Found {X_tfidf.shape[1]} features.")
            return self.tfidf_df # Return the keyword analysis table

    def run_lda_topic_modeling(self, num_topics: int = 4, passes: int = 10):
        """
        Performs Tokenization, Stopword Removal, and runs LDA Topic Modeling using Gensim.
        
        """
        print(f"\n--- Starting LDA Topic Modeling ({num_topics} Topics) ---")
        
        # Ensure cleaning is done first (re-using the preprocessing logic)
        self.df['cleaned_review'] = self.df['review_text'].apply(self._preprocess_text)

        # 1. Tokenize text (Split based on whitespace created by cleaning)
        self.df["tokens"] = self.df["cleaned_review"].str.split()

        # 2. Stopword Removal
        stop_words = set(stopwords.words("english"))
        self.df["tokens_nostop"] = self.df["tokens"].apply(
            lambda words: [w for w in words if w not in stop_words and len(w) > 2] # Added minimum word length for quality
        )

        # 3. Create dictionary and corpus
        dictionary = Dictionary(self.df["tokens_nostop"])
        # Optional: Filter out tokens that appear in less than N documents or in more than M% of documents
        dictionary.filter_extremes(no_below=5, no_above=0.5) 
        
        corpus = [dictionary.doc2bow(tokens) for tokens in self.df["tokens_nostop"]]

        # 4. Train LDA Model
        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=num_topics,
            passes=passes,
            random_state=42
        )

        # 5. Extract and Format Topics
        topics_output = []
        topics = lda_model.show_topics(num_topics=num_topics, num_words=10, formatted=False)

        for i, topic in topics:
            topic_str = f"--- Topic {i+1} ---\n"
            for word, weight in topic:
                topic_str += f"{word:15s}  weight={weight:.4f}\n"
            topics_output.append(topic_str)

        print("LDA modeling complete.")
        return "\n".join(topics_output)
                      
    def _get_topics_for_subset(self, docs: list, n_topics: int = 4, top_n: int = 12) -> list:
        """
        Internal function to run Scikit-learn's LDA on a list of pre-cleaned documents.
        This is the encapsulated logic from the user's original function.
        """
        if len(docs) < 50:
            return []

        # Vectorize with stricter settings
        tfidf = TfidfVectorizer(
            max_df=0.85, 
            min_df=3, 
            ngram_range=(1, 2),
            stop_words='english',
            max_features=800,
            token_pattern=r'\b[a-zA-Z]{3,}\b'
        )
        X = tfidf.fit_transform(docs)
        
        lda = LatentDirichletAllocation(
            n_components=n_topics, 
            random_state=42,
            learning_method='online'
        )
        lda.fit(X)
        
        feature_names = tfidf.get_feature_names_out()
        topics = []
        for i, comp in enumerate(lda.components_):
            top_idx = comp.argsort()[-top_n:][::-1]
            top_words = [(feature_names[j], comp[j]) for j in top_idx]
            topics.append(top_words)
        return topics


    def run_lda_by_bank(self, n_topics: int = 4, top_n: int = 12) -> str:
        """
        Runs LDA topic modeling separately for each bank and returns formatted output.
        """
        if 'cleaned_review' not in self.df.columns:
            # Ensure text is cleaned before running LDA
            self.df['cleaned_review'] = self.df['review_text'].apply(self._preprocess_text)
            
        output = []
        
        # Iterate over unique banks
        for bank in self.df['bank_name'].unique():
            df_bank = self.df[self.df['bank_name'] == bank]
            
            # Filter very short reviews for quality
            docs = df_bank[df_bank['cleaned_review'].str.len() > 10]['cleaned_review'].tolist()

            topics = self._get_topics_for_subset(docs, n_topics, top_n)
            
            output.append(f"\n=== {bank} ({len(docs)} reviews) ===")
            
            if not topics:
                output.append("Insufficient data for reliable LDA modeling.")
                continue

            for i, topic in enumerate(topics):
                words = [w for w, _ in topic[:8]] # Only show top 8 words for conciseness
                output.append(f"Topic {i+1}: {', '.join(words)}")

        return "\n".join(output)
      
      
    def assign_themes(self, top_k: int = 1) -> pd.DataFrame:
        """
        Applies rule-based clustering based on predefined keywords and returns top-K theme(s).
        """
        print("Starting rule-based thematic clustering...")       
        
        def _get_themes_for_review(text, mapping, top_k):
          
            
            if pd.isna(text): return 'other'
            text = str(text).lower()
            scores = {}
            
            # Count keyword hits for each theme
            for theme, keywords in mapping.items():
                # Use strict membership check, as defined in the original logic
                score = sum(1 for kw in keywords if kw in text) 
                if score > 0:
                    scores[theme] = score
            
            # Return top-k themes, sorted by score
            return ', '.join(sorted(scores, key=scores.get, reverse=True)[:top_k]) or 'other'

        # Apply the theme assignment, creating the 'theme' column as per user's request

        # Using the raw 'review' column for matching
        self.df['theme'] = self.df['review_text'].apply(
            lambda x: _get_themes_for_review(x, self.THEME_MAPPINGS, top_k)
        )
        
        print("Thematic assignment complete.")
        return self.df