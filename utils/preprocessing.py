import re
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already present
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words("english"))

def preprocess(text):
    # Convert to lowercase
    text = text.lower()
    
    # Keep alphanumeric, spaces, hyphens, and plus signs
    # This preserves: C++, .NET, machine-learning, scikit-learn, etc.
    text = re.sub(r"[^a-z0-9\s\-\+\.]", " ", text)
    
    # Replace multiple spaces with single space
    text = re.sub(r"\s+", " ", text)
    
    # Tokenize
    tokens = text.split()
    
    # Remove stop words but keep meaningful single characters (like 'c' in 'c++')
    tokens = [w for w in tokens if w not in stop_words or len(w) == 1]
    
    # Join back
    return " ".join(tokens)