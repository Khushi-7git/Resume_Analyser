import streamlit as st
import pdfplumber
import spacy
import sqlite3

# --- Load spaCy NLP model ---
nlp = spacy.load("en_core_web_sm")

# --- Classes ---

class ResumeDB:
    """Handles SQLite operations"""
    def __init__(self, db_name="resumes.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                resume_text TEXT
            )
            """)
            conn.commit()

    def insert_resume(self, name, resume_text):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO candidates (name, resume_text) VALUES (?, ?)",
                    (name, resume_text)
                )
                conn.commit()
            return True, "💾 Resume saved in database."
        except sqlite3.IntegrityError:
            return False, "⚠️ This candidate name already exists."
        except sqlite3.OperationalError as e:
            return False, f"⚠️ Database error: {e}"

    def get_all_candidates(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM candidates")
            return cursor.fetchall()

    def get_resume_by_id(self, candidate_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT resume_text FROM candidates WHERE id=?", (candidate_id,))
            result = cursor.fetchone()
            return result[0] if result else None


class ResumeProcessor:
    """Extracts text and skills from resume"""
    @staticmethod
    def extract_text(uploaded_file):
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    @staticmethod
    def extract_skills(resume_text):
        doc = nlp(resume_text.lower())
        skills = set()
        for token in doc:
            if token.pos_ in ["PROPN", "NOUN"] and len(token.text) > 2:
                skills.add(token.text)
        return skills

    @staticmethod
    def match_skills(resume_skills, job_description):
        job_skills = set([skill.strip().lower() for skill in job_description.split(",")])
        missing = job_skills - resume_skills
        matched = job_skills - missing
        match_score = round(len(matched)/len(job_skills)*100,2) if job_skills else 0
        return matched, missing, match_score


class CareerChatbot:
    """Simple rule-based chatbot for career advice"""
    faq = {
        "frontend developer": "A Frontend Developer builds the UI of websites or apps. Skills: HTML, CSS, JavaScript, React, UI/UX design.",
        "backend developer": "A Backend Developer works on server-side logic, databases, and APIs. Skills: Python, Node.js, Java, SQL, REST APIs.",
        "fullstack developer": "A Fullstack Developer handles both frontend and backend development. Skills: HTML, CSS, JS, React, Python/Node, SQL/NoSQL.",
        "improve skills": "You can improve your skills by taking online courses, building projects, and practicing coding challenges.",
        "resume": "Make sure your resume is concise, highlights your key skills, and matches the job requirements."
    }

    @staticmethod
    def get_answer(user_input):
        user_input = user_input.lower()
        for key, answer in CareerChatbot.faq.items():
            if key in user_input:
                return answer
        return "Keep learning and practicing! Focus on the skills required for your desired job."


# --- Streamlit App ---

st.set_page_config(page_title="🤖 Smart AI Recruiter", layout="wide")
st.title("🤖 Smart AI Recruiter with OOP & SQLite")
st.markdown("Upload resumes, match skills, and get career advice!")

# Instantiate objects
db = ResumeDB()
processor = ResumeProcessor()
chatbot = CareerChatbot()

# --- Candidate Upload Section ---
with st.container():
    st.subheader("📄 Candidate Resume Upload")
    col1, col2 = st.columns([2,3])
    
    with col1:
        name = st.text_input("Enter Candidate Name")
    with col2:
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    if uploaded_file and name:
        resume_text = processor.extract_text(uploaded_file)
        st.success("✅ Resume uploaded successfully!")

        # Store in DB
        success, msg = db.insert_resume(name, resume_text)
        if success:
            st.info(msg)
        else:
            st.warning(msg)

        # Display skills
        resume_skills = processor.extract_skills(resume_text)
        st.subheader("🔍 Extracted Skills")
        st.markdown(f"**Skills:** {', '.join(list(resume_skills)[:50])}" + ("..." if len(resume_skills) > 50 else ""))

        # Job Description & Skill Matching
        job_description = st.text_area("💼 Enter Job Description / Required Skills (comma-separated)")
        if st.button("✅ Match Skills"):
            if job_description.strip() != "":
                matched, missing, score = processor.match_skills(resume_skills, job_description)
                st.markdown(f"**Skill Match Score:** {score}%")
                if missing:
                    st.warning(f"⚠️ Missing Skills: {', '.join(missing)}")
                else:
                    st.success("🎉 All required skills are present!")
            else:
                st.warning("Please enter a job description.")

# --- Career Chatbot ---
with st.container():
    st.subheader("💬 Career Advice Chatbot")
    user_input = st.text_input("Ask a career-related question")
    if st.button("Ask AI Chatbot"):
        if user_input.strip() != "":
            answer = chatbot.get_answer(user_input)
            st.info(f"🤖 AI Answer: {answer}")
        else:
            st.warning("Please type a question to get an answer.")
