import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Student Submission Marking Tool",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Student Submission Marking Tool")
st.markdown("---")

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = {}

# MARKING SCHEME
st.header("📊 Marking Scheme")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Presentation Marks")
    st.write("• **Excellent:** 1.5")
    st.write("• **Medium:** 0.8")
    st.write("• **Bad:** 0.3")

with col2:
    st.subheader("Lab Marks (Each)")
    st.write("• **Excellent:** 1.7")
    st.write("• **Good:** 1.3")
    st.write("• **Average:** 0.9")
    st.write("• **Bad:** 0.5")

st.markdown("---")

# PRESENTATION SECTION
st.header("🎨 Presentation Evaluation")

presentation_options = {
    "excellent": "The overall presentation is excellent/perfect.",
    "medium_signposts": "Some signposts are not clear, such as multi-level headings, indents, dot points, bolding, etc.",
    "medium_font": "The use of font (spacing, margins, etc.) is not consistent across labs.",
    "medium_grammar": "Many spelling and grammar mistakes.",
    "medium_screenshots": "Some screenshots/pictures are not clear.",
    "medium_formatting": "Some code, commands and/or variables are not well formatted to distinguish themselves from texts.",
    "bad_not_pdf": "The submitted file is NOT a PDF.",
    "bad_no_template": "The submitted file didn't follow(or use) the provided markdown file as its template (e.g. the cover sheet should be a separate page).",
    "bad_too_long": "The submitted file has more than 80 pages in total.",
    "bad_filename": "The submitted file name does NOT follow the format of studentid_firstname_labs1_5.pdf",
    "bad_structure": "The submitted file has a poorly/unstructured structure, e.g., no headings, blurring screenshots/pictures."
}

# Marking scheme for presentation
presentation_marks = {
    "Excellent": 1.5,
    "Medium": 0.8,
    "Bad": 0.3
}

st.write("Select all applicable presentation criteria:")
presentation_selection = []
for key, description in presentation_options.items():
    if st.checkbox(description, key=f"pres_{key}"):
        presentation_selection.append(key)

# Calculate presentation grade
def calculate_presentation_grade(selections):
    if not selections:
        return "Excellent"
    
    bad_criteria = [k for k in selections if k.startswith("bad_")]
    if bad_criteria:
        return "Bad"
    
    excellent_criteria = [k for k in selections if k == "excellent"]
    if excellent_criteria and len(selections) == 1:
        return "Excellent"
    
    medium_criteria = [k for k in selections if k.startswith("medium_")]
    if medium_criteria:
        return "Medium"
    
    return "No Valid Selection"

presentation_grade = calculate_presentation_grade(presentation_selection)
presentation_mark = presentation_marks.get(presentation_grade, 0)

# Display grade and mark with color coding
if presentation_grade == "Excellent":
    st.success(f"**Presentation Grade: {presentation_grade} ({presentation_mark} marks)**")
elif presentation_grade == "Medium":
    st.warning(f"**Presentation Grade: {presentation_grade} ({presentation_mark} marks)**")
elif presentation_grade == "Bad":
    st.error(f"**Presentation Grade: {presentation_grade} ({presentation_mark} marks)**")
else:
    st.info(f"**Presentation Grade: {presentation_grade} ({presentation_mark} marks)**")

# Generate and display presentation feedback immediately
def generate_presentation_feedback(grade, selections):
    if not selections:
        return f"The presentation is {grade.lower()}."
    
    selected_descriptions = [presentation_options[sel] for sel in selections]
    
    if len(selected_descriptions) == 1:
        return f"The presentation is {grade.lower()} because {selected_descriptions[0].lower()}"
    elif len(selected_descriptions) == 2:
        return f"The presentation is {grade.lower()} because {selected_descriptions[0].lower()} and {selected_descriptions[1].lower()}"
    else:
        descriptions_text = ", ".join(selected_descriptions[:-1]) + f", and {selected_descriptions[-1]}"
        return f"The presentation is {grade.lower()} because {descriptions_text.lower()}"

presentation_feedback = generate_presentation_feedback(presentation_grade, presentation_selection)
st.info("**Presentation Feedback:**")
st.write(presentation_feedback)

# Copy button for presentation feedback
if st.button("📋 Copy Presentation Feedback", key="copy_pres_main"):
    st.code(presentation_feedback, language=None)

st.markdown("---")

# DESCRIPTION SECTION
st.header("📝 Description Evaluation")

# Lab criteria definitions
lab_criteria = {
    "Lab 1": {
        "bad_criteria": [
            "Evidence of a working environment is missing",
            "Explanations of used commands in installing Linux packages are missing/insufficient",
            "Explanations of used commands in testing the installed environment are missing",
            "The code to tabulate the print-based output has not been completed",
            "The code to tabulate the print-based output has little explanation"
        ],
        "bad_threshold": 4
    },
    "Lab 2": {
        "bad_criteria": [
            "The explanation of the commands used to create an ec2 instance using AWS CLI is too short",
            "The code to create an ec2 instance has little explanation",
            "The code to create an EC2 instance is missing",
            "The instance name does NOT start with a student number",
            "The instance type is not t3.micro",
            "The code to Build and run an httpd container has little explanation",
            "The explanation of the docker commands is too short",
            "Evidence of getting 'Hello World!' is missing",
            "Evidence of listing the created instance via the console is missing",
            "Explanations of manual instance termination are missing"
        ],
        "bad_threshold": 8
    },
    "Lab 3": {
        "bad_criteria": [
            "Explanations of commands used to prepare files and directories are missing",
            "The bucket name does not follow the format of student ID-cloudstorage",
            "The code used to save to S3 is missing",
            "The S3 bucket has an incorrect layout of objects",
            "The code used to restore from S3 is missing",
            "Explanations of code used to save to S3 are missing",
            "Explanations of code used to restore from S3 are missing",
            "The code used to write attributes of each file in the S3 bucket into the CloudFiles table is missing",
            "Explanations of code used to write attributes of each file in the S3 bucket into the CloudFiles table are missing",
            "The DynamoDB should be created locally (not on AWS)",
            "Some retrieved attributes shown in the CloudFiles table are not correct"
        ],
        "bad_threshold": 9
    },
    "Lab 4": {
        "bad_criteria": [
            "The code used to apply a policy to restrict permission on bucket is missing",
            "Explanations of commands used to apply a policy to restrict permission on bucket are missing",
            "The template resource should be instantiated via your own S3 bucket",
            "Screenshots/outputs for the policy check are missing",
            "The code used to create a KMS key is missing",
            "Explanations of code used to create a KMS key are missing",
            "The code used to attach a policy to the created KMS key is missing",
            "Explanations of code used to attach a policy to the created KMS key are missing",
            "Screenshots/outputs for the key check are missing",
            "The code used to use the KMS key is missing",
            "Explanations of code used to use the KMS key are missing",
            "The code used to use the pycryptodome for encryption/decryption is missing",
            "Explanations of code used to use the pycryptodome for encryption/decryption are missing",
            "The answer to the question is not valid"
        ],
        "bad_threshold": 12
    },
    "Lab 5": {
        "bad_criteria": [
            "The two EC2 instances must be created in two different availability zones",
            "You should attach your evidence of creating 2 instances",
            "The instance name does NOT start with a student number",
            "The instance type is not t3.micro",
            "The code used to create an application load balancer is missing",
            "Explanations of code used to create an application load balancer are missing",
            "Explanations of commands used to test the application load balancer are missing",
            "The Apache web page does NOT show the correct instance name",
            "Explanations of manual instance termination are missing"
        ],
        "bad_threshold": 7
    },
    "Lab 6": {
        "bad_criteria": [
            "No screenshot/description of creating an EC2 (NOTE: students can use script or console)",
            "The EC2 instance type is not t3.micro",
            "No screenshot/description of creating a directory with a path, and cd into the directory",
            "The explanations of commands in installing python3 virtual environment packages are missing",
            "The explanations of commands in setting a python3 virtual environment are missing",
            "The explanations of commands in activating a python3 virtual environment are missing",
            "No description of the file contents of /etc/nginx/sites-enabled/default",
            "No screenshot/description of restarting nginx",
            "No screenshot of accessing the instance's IP address after restarting the web server",
            "No description of polls/views.py or /urls.py or lab/urls.py edited to set up django",
            "No screenshot of accessing the specific URL after restarting the web server",
            "No screenshot/description of creating an application load balancer (NOTE: students can use script or console)",
            "No screenshot/description of health check (NOTE: Django server showing requests or AWS console showing healthy status is sufficient)",
            "No screenshot/description of accessing the specific URL after health check",
            "No screenshot/description of creating an AWS DynamoDB table (NOTE: students can use script or console)",
            "No explanation of the given TEMPLATES section",
            "No explanation of the given files.html",
            "No explanation of the given views.py",
            "No screenshot/description of running a Django application",
            "No screenshot of accessing the web page",
            "No screenshot/description of deleting the instance",
            "No screenshot/description of deleting the load balancer",
            "No screenshot/description of deleting the AWS DynamoDB table"
        ],
        "bad_threshold": 17
    },
    "Lab 7": {
        "bad_criteria": [
            "No screenshot/description of creating an EC2 instance (NOTE: students can use script or console)",
            "The EC2 instance type is not t3.micro",
            "No screenshot/description of installing fabric",
            "No explanation of the config file",
            "No explanation of the fabric code that connects with the instance",
            "In fabric for automation, no description of code in installing/setting/activating the Python 3 virtual environment",
            "In fabric for automation, no description of code in installing/configuring/restarting nginx",
            "In fabric for automation, no description of code in creating and setting up django inside the created EC2 instance",
            "No screenshot/description of the url access in the end",
            "No screenshot/description of deleting the instance"
        ],
        "bad_threshold": 7
    },
    "Lab 8": {
        "bad_criteria": [
            "No explanation of the Dockerfile",
            "No screenshot/description of testing the image",
            "No explanation of the script that creates an ECR repository",
            "No explanation of the script that gets the Docker token",
            "No screenshot/description of explaining or running the output command",
            "No explanation of the tagging or pushing commands",
            "No screenshot/description of pushing the local Docker image onto ECR successfully",
            "No explanation of the script that creates a task definition for an ECS task",
            "No explanation of the script that creates an ECS service",
            "No screenshot/description of creating the ECS service successfully",
            "No explanation of the command that gets a public IP address",
            "No explanation of the three installed libraries",
            "No explanation of code in preparing a SageMaker session",
            "No explanation of commands used in downloading or unzipping the dataset",
            "No or incorrect answer to the first question (Answer: job, marital, education, default, housing, loan, contact, month, day_of_week, poutcome)",
            "No or incorrect answer to the second question (Answer: age, duration, campaign, pdays, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed)",
            "The explanation of code in reading the dataset into Pandas data frame is missing",
            "The explanation of code in processing the data is missing",
            "The explanation of code in removing the economic features and duration is missing",
            "The explanation of code in splitting the data is missing",
            "The explanation of code in copying the file to the S3 bucket is missing",
            "The explanation of code in setting up hyperparameter tuning is missing",
            "The explanation of code in specifying the XGBoost algorithm is missing",
            "No screenshot/description of launching hyperparameter tuning job",
            "No screenshot of the success of completing the tuning job",
            "No screenshot/description of deleting the S3 bucket",
            "No screenshot/description of deleting the ECR repository",
            "No screenshot/description of deleting the ECS service"
        ],
        "bad_threshold": 21
    },
    "Lab 9": {
        "bad_criteria": [
            "The code in detecting 4 different languages from text is missing",
            "The explanation of the code in detecting 4 different languages from text is missing",
            "The code in analyzing sentiment is missing",
            "The explanation of the code in analyzing sentiment is missing",
            "The code in detecting entities is missing",
            "The explanation of the code in detecting entities is missing",
            "No or incorrect answer to the question of describing what entities are",
            "The code in detecting keyphrases is missing",
            "The explanation of the code in detecting keyphrases is missing",
            "No or incorrect answer to the question of describing what keyphrases are",
            "The code in detecting syntaxes is missing",
            "The explanation of the code in detecting syntaxes is missing",
            "No or incorrect answer to the question of describing what syntaxes are",
            "The code of creating a S3 bucket and adding 4 images to the S3 bucket is missing",
            "The explanation of the code in label recognition is missing",
            "The explanation of the code in image moderation is missing",
            "The explanation of the code in facial analysis is missing",
            "The explanation of the code in text extraction is missing"
        ],
        "bad_threshold": 13
    }
}

# Marking scheme for labs
lab_marks = {
    "Lab 1": {"Excellent": 1.7, "Good": 1.3, "Average": 0.9, "Bad": 0.5},
    "Lab 2": {"Excellent": 1.7, "Good": 1.3, "Average": 0.9, "Bad": 0.5},
    "Lab 3": {"Excellent": 1.7, "Good": 1.3, "Average": 0.9, "Bad": 0.5},
    "Lab 4": {"Excellent": 1.7, "Good": 1.3, "Average": 0.9, "Bad": 0.5},
    "Lab 5": {"Excellent": 1.7, "Good": 1.3, "Average": 0.9, "Bad": 0.5},
    "Lab 6": {"Excellent": 1.7, "Good": 1.3, "Average": 0.9, "Bad": 0.5},
    "Lab 7": {"Excellent": 1.7, "Good": 1.3, "Average": 0.9, "Bad": 0.5},
    "Lab 8": {"Excellent": 2.55, "Good": 1.95, "Average": 1.35, "Bad": 0.75},
    "Lab 9": {"Excellent": 2.55, "Good": 1.95, "Average": 1.35, "Bad": 0.75}
}

# Create tabs for each lab
lab_tabs = st.tabs(["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5", "Lab 6", "Lab 7", "Lab 8", "Lab 9"])

lab_grades = {}
lab_feedback = {}

for i, (lab_name, tab) in enumerate(zip(lab_criteria.keys(), lab_tabs)):
    with tab:
        st.subheader(f"{lab_name} - Description Evaluation")
        
        # Missing criteria selection - use individual checkboxes
        st.write(f"Select missing/insufficient criteria for {lab_name}:")
        missing_criteria = []
        for criterion in lab_criteria[lab_name]["bad_criteria"]:
            if st.checkbox(criterion, key=f"{lab_name}_{criterion}"):
                missing_criteria.append(criterion)
        
        # Calculate grade for this lab based on the specific thresholds
        def calculate_lab_grade(missing_count, bad_threshold, lab_name):
            if missing_count == 0:
                return "Excellent"
            elif missing_count >= bad_threshold:
                return "Bad"
            else:
                # Lab-specific grading logic
                if lab_name == "Lab 1":
                    if missing_count <= 2:
                        return "Good"
                    else:
                        return "Average"
                elif lab_name in ["Lab 2", "Lab 3", "Lab 4", "Lab 5"]:
                    if missing_count <= 4:
                        return "Good"
                    else:
                        return "Average"
                elif lab_name == "Lab 6":
                    if missing_count <= 2:
                        return "Excellent"
                    elif missing_count <= 10:
                        return "Good"
                    elif missing_count <= 16:
                        return "Average"
                    else:
                        return "Bad"
                elif lab_name == "Lab 7":
                    if missing_count <= 1:
                        return "Excellent"
                    elif missing_count <= 3:
                        return "Good"
                    elif missing_count <= 6:
                        return "Average"
                    else:
                        return "Bad"
                elif lab_name == "Lab 8":
                    if missing_count <= 2:
                        return "Excellent"
                    elif missing_count <= 10:
                        return "Good"
                    elif missing_count <= 20:
                        return "Average"
                    else:
                        return "Bad"
                elif lab_name == "Lab 9":
                    if missing_count <= 2:
                        return "Excellent"
                    elif missing_count <= 8:
                        return "Good"
                    elif missing_count <= 12:
                        return "Average"
                    else:
                        return "Bad"
        
        missing_count = len(missing_criteria)
        lab_grade = calculate_lab_grade(
            missing_count, 
            lab_criteria[lab_name]["bad_threshold"],
            lab_name
        )
        
        lab_grades[lab_name] = lab_grade
        lab_feedback[lab_name] = {
            "missing_criteria": missing_criteria,
            "missing_count": missing_count
        }
        
        lab_mark = lab_marks.get(lab_name, {}).get(lab_grade, 0) if isinstance(lab_marks.get(lab_name, {}), dict) else lab_marks.get(lab_grade, 0)
        
        # Display grade with color coding and marks
        if lab_grade == "Excellent":
            st.success(f"**{lab_name} Grade: {lab_grade} ({lab_mark} marks)**")
        elif lab_grade == "Good":
            st.info(f"**{lab_name} Grade: {lab_grade} ({lab_mark} marks)**")
        elif lab_grade == "Average":
            st.warning(f"**{lab_name} Grade: {lab_grade} ({lab_mark} marks)**")
        else:
            st.error(f"**{lab_name} Grade: {lab_grade} ({lab_mark} marks)**")
        
        # Generate and display lab feedback immediately
        def generate_lab_feedback(lab_name, grade, lab_data):
            if not lab_data["missing_criteria"]:
                return f"The description is {grade.lower()}."
            
            missing_items = lab_data["missing_criteria"]
            
            if len(missing_items) == 1:
                return f"The description is {grade.lower()} because {missing_items[0].lower()}."
            elif len(missing_items) == 2:
                return f"The description is {grade.lower()} because {missing_items[0].lower()} and {missing_items[1].lower()}."
            else:
                items_text = ", ".join(missing_items[:-1]) + f", and {missing_items[-1]}"
                return f"The description is {grade.lower()} because {items_text.lower()}."
        
        lab_feedback_text = generate_lab_feedback(lab_name, lab_grade, lab_feedback[lab_name])
        st.info(f"**{lab_name} Feedback:**")
        st.write(lab_feedback_text)
        
        # Copy button for this lab's feedback
        if st.button(f"📋 Copy {lab_name} Feedback", key=f"copy_{lab_name}"):
            st.code(lab_feedback_text, language=None)

st.markdown("---")

# SUMMARY SECTION
st.header("📊 Summary & Feedback")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Overall Grades & Marks")
    st.write(f"**Presentation:** {presentation_grade} ({presentation_mark})")
    
    total_marks = presentation_mark
    for lab, grade in lab_grades.items():
        lab_mark = lab_marks.get(lab, {}).get(grade, 0) if isinstance(lab_marks.get(lab, {}), dict) else lab_marks.get(grade, 0)
        total_marks += lab_mark
        color_map = {
            "Excellent": "🟢",
            "Good": "🔵", 
            "Average": "🟡",
            "Bad": "🔴"
        }
        icon = color_map.get(grade, "⚪")
        st.write(f"**{lab}:** {icon} {grade} ({lab_mark})")
    
    st.markdown("---")
    # Update total to reflect different marks for labs 8-9
    max_total = 1.5 + (7 * 1.7) + (2 * 2.55)  # 1.5 for presentation + 7 labs at 1.7 each + 2 labs at 2.55 each
    st.write(f"**TOTAL MARKS: {total_marks}/{max_total}**")

with col2:
    st.subheader("Quick Stats")
    if lab_grades:
        grade_counts = {}
        for grade in lab_grades.values():
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        for grade, count in grade_counts.items():
            st.write(f"{grade}: {count} lab(s)")

with col3:
    st.subheader("Mark Breakdown")
    st.write(f"Presentation: {presentation_mark}")
    for lab, grade in lab_grades.items():
        lab_mark = lab_marks.get(lab, {}).get(grade, 0) if isinstance(lab_marks.get(lab, {}), dict) else lab_marks.get(grade, 0)
        st.write(f"{lab}: {lab_mark}")

# Generate detailed feedback
st.subheader("Generated Feedback")

def generate_presentation_feedback(grade, selections):
    if not selections:
        return f"The presentation is {grade.lower()}."
    
    selected_descriptions = [presentation_options[sel] for sel in selections]
    
    if len(selected_descriptions) == 1:
        return f"The presentation is {grade.lower()} because {selected_descriptions[0].lower()}"
    elif len(selected_descriptions) == 2:
        return f"The presentation is {grade.lower()} because {selected_descriptions[0].lower()} and {selected_descriptions[1].lower()}"
    else:
        descriptions_text = ", ".join(selected_descriptions[:-1]) + f", and {selected_descriptions[-1]}"
        return f"The presentation is {grade.lower()} because {descriptions_text.lower()}"

def generate_lab_feedback(lab_name, grade, lab_data):
    if not lab_data["missing_criteria"]:
        return f"The description is {grade.lower()}."
    
    missing_items = lab_data["missing_criteria"]
    
    if len(missing_items) == 1:
        return f"The description is {grade.lower()} because {missing_items[0].lower()}."
    elif len(missing_items) == 2:
        return f"The description is {grade.lower()} because {missing_items[0].lower()} and {missing_items[1].lower()}."
    else:
        items_text = ", ".join(missing_items[:-1]) + f", and {missing_items[-1]}"
        return f"The description is {grade.lower()} because {items_text.lower()}"

feedback_text = f"**Evaluation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

# Add total marks at the top
total_marks = presentation_mark
for lab, grade in lab_grades.items():
    lab_mark = lab_marks.get(lab, {}).get(grade, 0) if isinstance(lab_marks.get(lab, {}), dict) else lab_marks.get(grade, 0)
    total_marks += lab_mark

max_total = 1.5 + (7 * 1.7) + (2 * 2.55)  # 1.5 for presentation + 7 labs at 1.7 each + 2 labs at 2.55 each
feedback_text += f"**TOTAL MARKS: {total_marks}/{max_total}**\n\n"

# Presentation feedback
feedback_text += "**PRESENTATION EVALUATION:**\n"
presentation_feedback = generate_presentation_feedback(presentation_grade, presentation_selection)
feedback_text += f"{presentation_feedback} ({presentation_mark} marks)\n\n"

# Lab feedback
feedback_text += "**DESCRIPTION EVALUATION:**\n"
for lab_name, grade in lab_grades.items():
    lab_data = lab_feedback[lab_name]
    lab_feedback_text = generate_lab_feedback(lab_name, grade, lab_data)
    lab_mark = lab_marks.get(lab_name, {}).get(grade, 0) if isinstance(lab_marks.get(lab_name, {}), dict) else lab_marks.get(grade, 0)
    feedback_text += f"\n{lab_name}: {lab_feedback_text} ({lab_mark} marks)\n"

st.text_area("Detailed Feedback", feedback_text, height=400)

# Add individual copy buttons for each section
col1, col2, col3 = st.columns(3)
with col1:
    presentation_feedback_only = f"{generate_presentation_feedback(presentation_grade, presentation_selection)} ({presentation_mark} marks)"
    if st.button("📋 Copy Presentation Feedback"):
        st.code(presentation_feedback_only, language=None)

with col2:
    description_feedback_only = ""
    for lab_name, grade in lab_grades.items():
        lab_data = lab_feedback[lab_name]
        lab_feedback_text = generate_lab_feedback(lab_name, grade, lab_data)
        lab_mark = lab_marks.get(lab_name, {}).get(grade, 0) if isinstance(lab_marks.get(lab_name, {}), dict) else lab_marks.get(grade, 0)
        description_feedback_only += f"{lab_name}: {lab_feedback_text} ({lab_mark} marks)\n"
    
    if st.button("📋 Copy Description Feedback"):
        st.code(description_feedback_only, language=None)

with col3:
    if st.button("📋 Copy Complete Feedback"):
        st.code(feedback_text, language=None)

# Export options
st.subheader("Export Options")
col1, col2 = st.columns(2)

with col1:
    # Prepare data for CSV export
    csv_data = {
        "Presentation_Grade": [presentation_grade],
        "Presentation_Mark": [presentation_mark],
        "Lab1_Grade": [lab_grades.get("Lab 1", "")],
        "Lab1_Mark": [lab_marks.get("Lab 1", {}).get(lab_grades.get("Lab 1", ""), 0)],
        "Lab2_Grade": [lab_grades.get("Lab 2", "")],
        "Lab2_Mark": [lab_marks.get("Lab 2", {}).get(lab_grades.get("Lab 2", ""), 0)],
        "Lab3_Grade": [lab_grades.get("Lab 3", "")],
        "Lab3_Mark": [lab_marks.get("Lab 3", {}).get(lab_grades.get("Lab 3", ""), 0)],
        "Lab4_Grade": [lab_grades.get("Lab 4", "")],
        "Lab4_Mark": [lab_marks.get("Lab 4", {}).get(lab_grades.get("Lab 4", ""), 0)],
        "Lab5_Grade": [lab_grades.get("Lab 5", "")],
        "Lab5_Mark": [lab_marks.get("Lab 5", {}).get(lab_grades.get("Lab 5", ""), 0)],
        "Lab6_Grade": [lab_grades.get("Lab 6", "")],
        "Lab6_Mark": [lab_marks.get("Lab 6", {}).get(lab_grades.get("Lab 6", ""), 0)],
        "Lab7_Grade": [lab_grades.get("Lab 7", "")],
        "Lab7_Mark": [lab_marks.get("Lab 7", {}).get(lab_grades.get("Lab 7", ""), 0)],
        "Lab8_Grade": [lab_grades.get("Lab 8", "")],
        "Lab8_Mark": [lab_marks.get("Lab 8", {}).get(lab_grades.get("Lab 8", ""), 0)],
        "Lab9_Grade": [lab_grades.get("Lab 9", "")],
        "Lab9_Mark": [lab_marks.get("Lab 9", {}).get(lab_grades.get("Lab 9", ""), 0)],
        "Total_Marks": [total_marks],
        "Evaluation_Date": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    }
    
    df = pd.DataFrame(csv_data)
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"marking_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col2:
    # JSON export
    json_data = {
        "presentation": {
            "grade": presentation_grade,
            "mark": presentation_mark,
            "selected_issues": presentation_selection
        },
        "labs": lab_feedback,
        "lab_grades": lab_grades,
        "lab_marks": {lab: lab_marks.get(lab, {}).get(grade, 0) for lab, grade in lab_grades.items()},
        "total_marks": total_marks,
        "max_marks": max_total,
        "evaluation_date": datetime.now().isoformat(),
        "feedback": feedback_text
    }
    
    st.download_button(
        label="Download JSON",
        data=json.dumps(json_data, indent=2),
        file_name=f"marking_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# Reset button
if st.button("🔄 Reset All Fields"):
    st.session_state.clear()
    st.rerun()

# Instructions
with st.expander("📖 Instructions"):
    st.markdown(f"""
    **How to use this marking tool:**
    
    1. **Presentation Evaluation**: Select all applicable presentation issues using checkboxes
    2. **Description Evaluation**: For each lab:
       - Check if descriptions are excellent (sufficient and clear)
       - Mark any missing/insufficient criteria using checkboxes
    3. **Review Summary**: Check the generated grades, marks, and total score
    4. **Copy Feedback**: Use the copy buttons to get specific feedback text
    5. **Export**: Download results as CSV/JSON if needed
    
    **Marking Scheme:**
    - **Presentation**: Excellent (1.5) → Medium (0.8) → Bad (0.3)
    - **Labs 1-7**: Excellent (1.7) → Good (1.3) → Average (0.9) → Bad (0.5)
    - **Labs 8-9**: Excellent (2.55) → Good (1.95) → Average (1.35) → Bad (0.75)
    - **Total**: 18.5 marks (1.5 + 7×1.7 + 2×2.55)
    
    **Grading Logic:**
    - **Presentation**: Excellent (no issues) → Medium (some issues) → Bad (major issues)
    - **Labs 1-5**: Follow original thresholds
    - **Lab 6**: Excellent (0-2 missing) → Good (3-10) → Average (11-16) → Bad (>16)
    - **Lab 7**: Excellent (0-1 missing) → Good (2-3) → Average (4-6) → Bad (>6)
    - **Lab 8**: Excellent (0-2 missing) → Good (3-10) → Average (11-20) → Bad (>20)
    - **Lab 9**: Excellent (0-2 missing) → Good (3-8) → Average (9-12) → Bad (>12)
    
    **Time Estimates:**
    - Lab 1: ~1 min/submission
    - Lab 2: ~1.5 min/submission  
    - Lab 3: ~1.5 min/submission
    - Lab 4: ~1.5 min/submission
    - Lab 5: ~1.5 min/submission
    - Lab 6: ~2 min/submission
    - Lab 7: ~1.5 min/submission
    - Lab 8: ~2 min/submission
    - Lab 9: ~1.5 min/submission
    """)
