from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, jd_text):
    """
    Calculate similarity using TF-IDF vectorization and cosine similarity.
    
    Parameters:
    - resume_text: Preprocessed resume text
    - jd_text: Preprocessed job description text
    
    Returns:
    - Similarity score as percentage (0-100)
    """
    # Check if texts are not empty
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
    
    # Use TF-IDF with optimized parameters
    vectorizer = TfidfVectorizer(
        max_features=1000,          # Limit vocabulary size
        ngram_range=(1, 2),         # Use unigrams and bigrams
        min_df=1,                    # Minimum document frequency
        sublinear_tf=True            # Use sublinear term frequency scaling
    )
    
    try:
        # Fit and transform both texts
        vectors = vectorizer.fit_transform([resume_text, jd_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])
        
        # Convert to percentage and round
        score = round(similarity[0][0] * 100, 2)
        
        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, score))
        
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0