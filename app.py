from flask import Flask, render_template, request, flash, redirect, url_for
# import mysql.connector
import sqlite3


import os
from dotenv import load_dotenv
from utils.text_extraction import extract_text
from utils.preprocessing import preprocess
from utils.similarity import calculate_similarity
from utils.skills import extract_skills, missing_skills

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database connection function using environment variables
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row   # so we can access columns by name
    return conn

# def get_db_connection():
#     try:
#         return mysql.connector.connect(
#             host=os.getenv('DB_HOST', 'localhost'),
#             user=os.getenv('DB_USER', 'root'),
#             password=os.getenv('DB_PASSWORD'),
#             database=os.getenv('DB_NAME', 'resume_db')
#         )
#     except mysql.connector.Error as err:
#         print(f"Database connection error: {err}")
#         raise

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            match_score REAL,
            missing_skills TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Validate file upload
            if "resume" not in request.files:
                flash("No file uploaded!", "error")
                return redirect(url_for("index"))
            
            file = request.files["resume"]
            
            if file.filename == "":
                flash("No file selected!", "error")
                return redirect(url_for("index"))
            
            # Validate file extension
            if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
                flash("Only PDF and DOCX files are allowed!", "error")
                return redirect(url_for("index"))
            
            jd = request.form.get("job_desc", "").strip()
            
            if not jd:
                flash("Job description is required!", "error")
                return redirect(url_for("index"))
            
            # Save file
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            
            # Extract resume text
            resume_text = extract_text(path)
            
            if not resume_text.strip():
                os.remove(path)
                flash("Could not extract text from resume!", "error")
                return redirect(url_for("index"))
            
            # Preprocess text
            resume_text = preprocess(resume_text)
            jd_text = preprocess(jd)

            # Extract skills
            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text)
            missing = missing_skills(resume_skills, jd_skills)

            # TF-IDF semantic similarity
            tfidf_score = calculate_similarity(resume_text, jd_text)

            # Skill match percentage (bounded, no inflation)
            matched_skills = set(resume_skills) & set(jd_skills)

            if jd_skills:
                skill_match_score = (len(matched_skills) / len(jd_skills)) * 100
            else:
                skill_match_score = 0

            # Hybrid final score
            score = round((0.6 * skill_match_score) + (0.4 * tfidf_score), 2)

            # Store in database
            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute(
                "INSERT INTO results (filename, match_score, missing_skills) VALUES (?, ?, ?)",
                (file.filename, score, ", ".join(missing) if missing else "None")
            )

            db.commit()
            cursor.close()
            db.close()
            # db = get_db_connection()
            # cursor = db.cursor()
            
            # cursor.execute(
            #     "INSERT INTO results (filename, match_score, missing_skills) VALUES (%s, %s, %s)",
            #     (file.filename, score, ", ".join(missing) if missing else "None")
            # )
            # db.commit()
            # cursor.close()
            # db.close()
            
            # Clean up uploaded file
            os.remove(path)
            
            # Interpret score
            if score >= 80:
                interpretation = "Excellent Match! 🎉"
                status = "excellent"
            elif score >= 60:
                interpretation = "Good Match ✓"
                status = "good"
            elif score >= 40:
                interpretation = "Moderate Match ⚠️"
                status = "moderate"
            else:
                interpretation = "Poor Match ❌"
                status = "poor"
            
            return render_template(
                "result.html",
                score=score,
                missing=missing,
                interpretation=interpretation,
                status=status,
                matched_skills=list(matched_skills),
                total_required=len(jd_skills)
            )
            
        except FileNotFoundError:
            flash("File processing error!", "error")
            return redirect(url_for("index"))
        # except mysql.connector.Error as db_err:
        #     flash(f"Database error: {str(db_err)}", "error")
        #     return redirect(url_for("index"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("index"))
    
    return render_template("index.html")

@app.route("/history")
def history():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT resume_id, filename, match_score, missing_skills, timestamp FROM results ORDER BY timestamp DESC LIMIT 50"
        )
        records = cursor.fetchall()
        cursor.close()
        db.close()
        
        return render_template("history.html", records=records)
        
    # except mysql.connector.Error as e:
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
