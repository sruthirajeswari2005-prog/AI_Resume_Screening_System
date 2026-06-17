from flask import Flask, render_template, request 
import os
import re
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def clean_text(text):
    return re.sub(r'\s+', ' ', text)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['resume']
    job_description = request.form['job_description']

    if file:

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        # Extract PDF Text
        text = ""

        with open(filepath, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page in pdf_reader.pages:
                extracted = page.extract_text()

                if extracted:
                    text += extracted + " "

        cleaned_text = clean_text(text).lower()

        # Skills Database
        skills = [
            "Python",
            "Java",
            "SQL",
            "AWS",
            "HTML",
            "CSS",
            "JavaScript",
            "Flask",
            "Machine Learning",
            "Data Science",
            "Unix",
            "Shell Scripting",
            "Postman",
            "Tomcat",
            "WebLogic",
            "New Relic",
            "Dynatrace",
            "CloudWatch",
            "Java EE",
            "Oracle SQL"
        ]

        # Find Skills
        found_skills = []

        for skill in skills:
            if skill.lower() in cleaned_text:
                found_skills.append(skill)

        # Resume Score
        total_skills = len(skills)
        score = int((len(found_skills) / total_skills) * 100)

        # Recommendation
        if score >= 80:
            recommendation = "Highly Recommended"
        elif score >= 60:
            recommendation = "Recommended"
        elif score >= 40:
            recommendation = "Average Match"
        else:
            recommendation = "Need More Skills"

        # Job Match Score
        matched_skills = []

        for skill in skills:
            if (
                skill.lower() in cleaned_text
                and skill.lower() in job_description.lower()
            ):
                matched_skills.append(skill)

        match_score = int(
            (len(matched_skills) / total_skills) * 100
        )

        # Recommended Roles
        recommended_roles = []

        if "Java" in found_skills:
            recommended_roles.append("Java Developer")

        if "SQL" in found_skills:
            recommended_roles.append("Database Developer")

        if "AWS" in found_skills:
            recommended_roles.append("Cloud Support Engineer")

        if "Unix" in found_skills:
            recommended_roles.append("Application Support Engineer")

        if "Tomcat" in found_skills or "WebLogic" in found_skills:
            recommended_roles.append("Middleware Engineer")

        # Suggestions
        suggestions = []

        if "Python" not in found_skills:
            suggestions.append("Learn Python")

        if "Flask" not in found_skills:
            suggestions.append("Learn Flask")

        if "Machine Learning" not in found_skills:
            suggestions.append("Learn Machine Learning")

        if "Data Science" not in found_skills:
            suggestions.append("Learn Data Science")

        if "JavaScript" not in found_skills:
            suggestions.append("Improve Front-End Skills")

        # Interview Questions
        questions = []

        if "Java" in found_skills:
            questions.extend([
                "What is the difference between JDK and JRE?",
                "Explain multithreading in Java."
            ])

        if "SQL" in found_skills:
            questions.extend([
                "What is a JOIN?",
                "What is normalization?"
            ])

        if "AWS" in found_skills:
            questions.extend([
                "What is AWS CloudWatch?",
                "What is EC2?"
            ])

        return f"""
        <html>
        <body style="font-family:Arial;padding:20px;">

        <h1>AI Resume Screening Report</h1>

        <h3>Resume Score: {score}%</h3>
        <h3>Job Match Score: {match_score}%</h3>

        <h3>Recommendation:</h3>
        <p><b>{recommendation}</b></p>

        <h3>Skills Found:</h3>
        <ul>
        {''.join(f'<li>{skill}</li>' for skill in found_skills)}
        </ul>

        <h3>Recommended Roles:</h3>
        <ul>
        {''.join(f'<li>{role}</li>' for role in recommended_roles)}
        </ul>

        <h3>Resume Improvement Suggestions:</h3>
        <ul>
        {''.join(f'<li>{item}</li>' for item in suggestions)}
        </ul>

        <h3>Interview Questions:</h3>
        <ul>
        {''.join(f'<li>{q}</li>' for q in questions)}
        </ul>

        </body>
        </html>
        """

    return "No file selected"


if __name__ == '__main__':
    app.run(debug=True)

