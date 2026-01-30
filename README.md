
# AI-Based Resume Screening and Skill Gap Analyzer

An automated resume matching system using **NLP** and **Machine Learning** to evaluate candidate-job compatibility.


## 🚀 Features

- ✅ PDF & DOCX resume support
- ✅ Hybrid scoring (60% skill match + 40% TF-IDF)
- ✅ Real-time skill gap identification
- ✅ Historical analysis tracking
- ✅ Clean, modern web interface  




## 🛠️ Tech Stack

- **Backend:** Python Flask
- **Database:** MySQL
- **ML/NLP:** scikit-learn, NLTK
- **Frontend:** HTML, CSS, JavaScript


## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)



## 🔧 How to Use

1. **Clone the repository**:
```bash
    git clone https://github.com/YOUR_USERNAME/resume-analyzer.git
    cd resume-analyzer
```
2. **Create virtual environment**:
  ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

3. **Install dependencies**:
  ```bash
    pip install -r requirements.txt
  ```



4. **Download NLTK data**:
```bash
  python -c "import nltk; nltk.download('stopwords')"
```

5. **Setup MySQL database**:
  ```sql
    CREATE DATABASE resume_db;
    USE resume_db;

    CREATE TABLE results (
      resume_id INT AUTO_INCREMENT PRIMARY KEY,
      filename VARCHAR(255) NOT NULL,
      match_score DECIMAL(5,2) NOT NULL,
      missing_skills TEXT,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  ```


6. **Create `.env` file**:
  ```env
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=resume_db
    SECRET_KEY=your-secret-key
  ```

7. **Run the application**:
  ```bash
    python app.py
  ```

8. **Open browser:** `http://localhost:5000`



## 📊 Usage

1. Upload resume (PDF/DOCX)
2. Paste job description
3. Click "Analyze Match"
4. View results and missing skills


## 📁 Project Structure
```
resume-analyzer/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── result.html
│   └── history.html
├── uploads/
└── utils/
    ├── text_extraction.py
    ├── preprocessing.py
    ├── similarity.py
    └── skills.py
```

## 🧪 Algorithm

Uses hybrid scoring approach:
- **60%** Skill Match (explicit skill detection)
- **40%** TF-IDF Semantic Similarity

Formula: `Final_Score = (0.6 × Skill_Score) + (0.4 × TF-IDF_Score)`


## 👨‍💻 Author

- **Arman Khan**  

## 📝 License

This project is licensed under the MIT License.
