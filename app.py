import re
import io
from datetime import datetime

import streamlit as st
import plotly.express as px
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="ResumeAI | Smart Analyzer",
    page_icon="📄",
    layout="wide"
)

# -------------------- STYLE --------------------
st.markdown("""
<style>
.stApp { background: #f5f7fb; }
[data-testid="stSidebar"] { background: #111827; }
[data-testid="stSidebar"] * { color: white !important; }
.hero {
    padding: 28px; border-radius: 18px; color: white;
    background: linear-gradient(120deg, #172554, #2563eb);
    margin-bottom: 20px;
}
.hero h1 { color: white; margin-bottom: 6px; }
.small-note { color: #64748b; font-size: 0.92rem; }
</style>
""", unsafe_allow_html=True)

# -------------------- MODEL --------------------
@st.cache_resource
def load_semantic_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

# -------------------- SKILLS --------------------
SKILLS = [
    "python", "java", "c++", "sql", "machine learning",
    "deep learning", "artificial intelligence", "data analysis",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "html", "css", "javascript", "react", "flask", "django",
    "streamlit", "communication", "problem solving",
    "data visualization", "power bi", "excel", "statistics",
    "git", "github", "nlp", "computer vision", "aws", "docker"
]

ROLE_DESCRIPTIONS = {
    "AI / ML Intern": """AI/ML intern with Python, machine learning, SQL, Pandas,
NumPy, data analysis, statistics, Scikit-learn, model evaluation and problem solving.
Assist in developing machine learning models, cleaning datasets and evaluating model performance.""",
    "Python Developer": """Python developer with Python programming, object-oriented programming,
SQL, APIs, Git, debugging, problem solving, Flask or Django and software development.""",
    "Data Analyst": """Data analyst with SQL, Python, Excel, Pandas, NumPy, statistics,
data cleaning, data visualization, Power BI, dashboards and communication skills.""",
    "Web Developer": """Web developer with HTML, CSS, JavaScript, React, APIs, responsive design,
Git, debugging and web application development.""",
    "Software Developer": """Software developer with programming, Python or Java, data structures,
SQL, Git, testing, debugging, problem solving and software development practices."""
}

# -------------------- HELPERS --------------------
def extract_pdf_text(uploaded_file):
    try:
        pdf = PdfReader(uploaded_file)
        pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages).strip()
    except Exception as exc:
        st.error(f"Could not read this PDF: {exc}")
        return ""

def find_skills(text):
    text_lower = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found

def semantic_similarity(resume_text, job_text):
    model = load_semantic_model()
    embeddings = model.encode([resume_text, job_text], normalize_embeddings=True)
    raw_score = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
    # Cosine similarity can be negative; clamp for a readable percentage.
    return round(max(0.0, min(1.0, raw_score)) * 100, 1)

def make_report(score, resume_skills, job_skills, matched, missing, role):
    lines = [
        "RESUMEAI - RESUME ANALYSIS REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Target role: {role}",
        f"Semantic similarity: {score}%",
        "",
        "SKILLS FOUND IN RESUME:",
        ", ".join(resume_skills) if resume_skills else "No listed skills detected",
        "",
        "MATCHED SKILLS:",
        ", ".join(matched) if matched else "No matching listed skills detected",
        "",
        "POTENTIAL SKILL GAPS:",
        ", ".join(missing) if missing else "No gaps detected from the listed skills",
        "",
        "Note: Similarity is an automated text comparison, not an official ATS score or a prediction of hiring outcomes."
    ]
    return "\n".join(lines)

# -------------------- SIDEBAR --------------------
st.sidebar.title("📄 ResumeAI")
st.sidebar.caption("Smart Resume Analyzer")
page = st.sidebar.radio("Navigation", ["Dashboard", "How It Works", "About Project"])

if page == "Dashboard":
    st.markdown("""
    <div class="hero">
      <h1>AI Resume Analyzer</h1>
      <p>Compare your resume with a job description using semantic similarity and skill analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1])
    with left:
        uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
        target_role = st.selectbox("Target Job Role", list(ROLE_DESCRIPTIONS.keys()))
    with right:
        job_description = st.text_area(
            "Job Description",
            value=ROLE_DESCRIPTIONS[target_role],
            height=210,
            help="Paste the job description here. The selected role provides a starter description."
        )

    analyze = st.button("🔍 Analyze My Resume", type="primary", use_container_width=True)

    if analyze:
        if not uploaded_resume:
            st.warning("Please upload your resume as a PDF first.")
        elif not job_description.strip():
            st.warning("Please enter a job description.")
        else:
            with st.spinner("Reading your resume and comparing text meaning... First run may download the AI model."):
                resume_text = extract_pdf_text(uploaded_resume)
                if not resume_text:
                    st.error("No readable text was found. Please use a text-based PDF, not a scanned image PDF.")
                    st.stop()

                resume_skills = find_skills(resume_text)
                job_skills = find_skills(job_description)
                matched_skills = [skill for skill in job_skills if skill in resume_skills]
                missing_skills = [skill for skill in job_skills if skill not in resume_skills]
                score = semantic_similarity(resume_text, job_description)
                coverage = round((len(matched_skills) / len(job_skills)) * 100, 1) if job_skills else 0.0

            st.success("Analysis completed!")
            st.subheader("📊 Analysis Overview")
            c1, c2, c3 = st.columns(3)
            c1.metric("Semantic Similarity", f"{score}%")
            c2.metric("Skills Matched", f"{len(matched_skills)} / {len(job_skills)}")
            c3.metric("Potential Skill Gaps", len(missing_skills))

            st.caption(
                "Semantic similarity compares the meaning of the resume and job-description text. "
                "It is not an official ATS score or a hiring probability."
            )

            chart1, chart2 = st.columns(2)
            with chart1:
                st.markdown("#### Skills Overview")
                overview = {
                    "Skills found in resume": len(resume_skills),
                    "Skills in job description": len(job_skills),
                    "Matched skills": len(matched_skills),
                    "Potential gaps": len(missing_skills)
                }
                fig = px.bar(
                    x=list(overview.keys()), y=list(overview.values()),
                    labels={"x": "Category", "y": "Number of skills"},
                    title="Resume and Job Skill Overview"
                )
                fig.update_layout(showlegend=False, xaxis_tickangle=-20, margin=dict(t=50, b=80))
                st.plotly_chart(fig, use_container_width=True)

            with chart2:
                st.markdown("#### Skill Match Coverage")
                pie_values = [len(matched_skills), len(missing_skills)]
                pie_labels = ["Matched skills", "Potential gaps"]
                if sum(pie_values) == 0:
                    pie_values = [1]
                    pie_labels = ["No listed skills detected"]
                fig2 = px.pie(
                    names=pie_labels if sum([len(matched_skills), len(missing_skills)]) else pie_labels,
                    values=pie_values,
                    hole=0.55,
                    title="Job Description Skill Coverage"
                )
                st.plotly_chart(fig2, use_container_width=True)
                st.metric("Skill Match Coverage", f"{coverage}%")

            st.markdown("#### ✅ Matched Skills")
            if matched_skills:
                st.write(" · ".join(f"`{skill}`" for skill in matched_skills))
            else:
                st.info("No listed skill keywords matched. Check your resume wording and job description.")

            st.markdown("#### 🧩 Potential Skill Gaps")
            if missing_skills:
                st.write(" · ".join(f"`{skill}`" for skill in missing_skills))
                st.write("Suggestions:")
                for skill in missing_skills[:8]:
                    st.write(f"- If you genuinely have **{skill}** experience, add it clearly to your Skills or Projects section.")
            else:
                st.success("No potential skill gaps were found among the skills this tool checks.")

            st.markdown("#### 💡 Resume Improvement Tips")
            tips = []
            if len(resume_text.split()) < 100:
                tips.append("Your resume text is quite short. Consider adding relevant project details, responsibilities and measurable outcomes.")
            if not re.search(r"\b(project|projects)\b", resume_text, re.I):
                tips.append("Add a Projects section describing what you built, the tools used and the result.")
            if not re.search(r"\b(education|degree|university|college)\b", resume_text, re.I):
                tips.append("Make sure your Education section is clearly labelled.")
            tips.append("Use honest, specific examples of your skills; do not add skills you cannot explain in an interview.")
            for tip in tips:
                st.write(f"- {tip}")

            report = make_report(score, resume_skills, job_skills, matched_skills, missing_skills, target_role)
            st.download_button(
                "⬇️ Download Analysis Report (.txt)",
                data=report.encode("utf-8"),
                file_name="resume_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )

elif page == "How It Works":
    st.title("How It Works")
    st.write("1. Upload a text-readable PDF resume.")
    st.write("2. Choose a target role and review or paste the job description.")
    st.write("3. The app extracts PDF text and detects listed skills.")
    st.write("4. A pretrained Sentence Transformers model compares resume and job-description meaning.")
    st.write("5. Charts and a report summarize similarity, matched skills and potential gaps.")
    st.info("The first analysis may take longer because the pretrained model is downloaded and loaded.")

else:
    st.title("About ResumeAI")
    st.write("ResumeAI is an educational AIML mini-project built with Python and Streamlit.")
    st.write("Technologies: Sentence Transformers, scikit-learn, pypdf and Plotly.")
    st.write("Limitations: skill detection uses a fixed keyword list, PDF text extraction may not work on scanned PDFs, and similarity is not an official ATS score or hiring prediction.")