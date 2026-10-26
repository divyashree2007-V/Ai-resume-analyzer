🤖 AI Resume Analyzer & Job Matching System

📌 Overview

    AI Resume Analyzer is a Python-based web application designed to analyze resumes and evaluate how well a candidate's skills match a given job description. The project combines natural language processing, machine learning techniques, and an interactive Streamlit dashboard to help job seekers understand their resume strengths and identify areas for improvement.
    The application extracts text from PDF resumes, analyzes relevant skills, and presents matching results through an interactive interface.

🚀 Features

  📄 **Resume Upload:** Upload resumes in PDF format for analysis.
  🧠 **AI-Powered Text Analysis:** Uses Sentence Transformers to compare resume content with job requirements.
  🎯 **Job Description Matching:** Evaluates the similarity between resume content and a given job description.
  📊 **Match Score Visualization:** Displays matching results using interactive charts.
  🛠️ **Skills Analysis:** Identifies relevant skills and highlights potential skill gaps based on the analysis.
  🔗 **GitHub Profile Link:** Displays a clickable GitHub profile hyperlink when a valid profile URL is found in the resume.
  📈 **Interactive Dashboard:** Presents resume analysis results using Streamlit and Plotly.
  💡 **Resume Improvement:** Helps candidates identify areas they may need to improve.

🛠️ Technologies Used

      Python
      Streamlit
      Sentence Transformers
      PyPDF
      Plotly
      Natural Language Processing (NLP)
      Machine Learning
      HTML/CSS 

⚙️ Installation and Setup

1. Clone the Repository


git clone https://github.com/divyashree2007-V/Ai-resume-analyzer


2. Navigate to the Project Folder


cd AI_Resume_Analyzer

3. Create a Virtual Environment 

python -m venv .venv


4. Activate the Virtual Environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1


5. Install Dependencies


python -m pip install -r requirements.txt


6. Run the Application


python -m streamlit run app.py


7. Open in Browser

 Open the local URL displayed in the terminal, usually:

http://localhost:8501

📖 How to Use

1. Launch the AI Resume Analyzer application.
2. Upload your resume in PDF format.
3. Enter the target job description, if requested by the interface.
4. Start the resume analysis.
5. Review the matching score and extracted information.
6. Check the identified skills and potential skill gaps.
7. Open the candidate's GitHub profile using the displayed hyperlink, when available.
8. Use the results to improve the resume for the target role.

🎯 Project Objective
      The objective of AI Resume Analyzer is to simplify resume evaluation and help candidates understand the relevance of their qualifications to specific job opportunities.
      By combining text similarity techniques, resume parsing, and an interactive dashboard, the project demonstrates how AI and machine learning can support career preparation and job application workflows.

🔮 Future Improvements

  Support additional resume formats such as DOCX.
  Improve technical skill extraction using advanced NLP techniques.
  Recommend suitable job roles based on resume content.
  Provide detailed, section-wise resume improvement suggestions.
  Add downloadable resume analysis reports.
  Integrate a larger job description database for matching.
  Deploy the application online for public access.


👩‍💻 Developer

Divyashree V B.E. Computer Science and Engineering (Artificial Intelligence and Machine Learning)

GitHub: https://github.com/divyashree2007-V

LinkedIn: https://www.linkedin.com/in/divyashree-vijayan-9397a432b

---

An AI/ML project exploring resume analysis, semantic text matching, and job-description relevance through an interactive web application.
