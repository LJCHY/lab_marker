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

# Student Information
st.header("Student Information")
col1, col2 = st.columns(2)
with col1:
    student_id = st.text_input("Student ID")
with col2:
    student_name = st.text_input("Student Name")

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
    "bad_no_template": "The submitted file didn't use the provided markdown file as its template.",
    "bad_too_long": "The submitted file has more than 80 pages in total.",
    "bad_filename": "The submitted file name does NOT follow the format of studentid_firstname_labs1_5.pdf",
    "bad_structure": "The submitted file has a poorly/unstructured structure, e.g., no headings, blurring screenshots/pictures."
}

st.write("Select all applicable presentation criteria:")
presentation_selection = []
for key, description in presentation_options.items():
    if st.checkbox(description, key=f"pres_{key}"):
        presentation_selection.append(key)

# Calculate presentation grade
def calculate_presentation_grade(selections):
    if not selections:
        return "No Selection"
    
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
st.subheader(f"Presentation Grade: **{presentation_grade}**")

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
            "Explanations of used commands in creating an EC2 instance using awscli are missing",
            "Explanations of python code in creating an EC2 instance are missing",
            "The code to create an EC2 instance is missing",
            "The instance name does NOT start with a student number",
            "The instance type is not t3.micro",
            "The code to Build and run an httpd container has little explanation",
            "Explanations of used commands about Docker are missing",
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
    }
}

# Create tabs for each lab
lab_tabs = st.tabs(["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5"])

lab_grades = {}
lab_feedback = {}

for i, (lab_name, tab) in enumerate(zip(lab_criteria.keys(), lab_tabs)):
    with tab:
        st.subheader(f"{lab_name} - Description Evaluation")
        
        # Overall description quality - use checkbox instead of radio
        desc_excellent = st.checkbox(
            "The descriptions are sufficient and steps are clear with detailed descriptions.",
            key=f"{lab_name}_desc_excellent"
        )
        
        # Missing criteria selection - use individual checkboxes
        st.write(f"Select missing/insufficient criteria for {lab_name}:")
        missing_criteria = []
        for criterion in lab_criteria[lab_name]["bad_criteria"]:
            if st.checkbox(criterion, key=f"{lab_name}_{criterion}"):
                missing_criteria.append(criterion)
        
        # Calculate grade for this lab
        def calculate_lab_grade(desc_excellent, missing_count, bad_threshold, lab_name):
            if desc_excellent and missing_count == 0:
                return "Excellent"
            elif missing_count >= bad_threshold:
                return "Bad"
            elif lab_name in ["Lab 2", "Lab 3", "Lab 4", "Lab 5"] and missing_count <= 4:
                return "Good"
            elif lab_name == "Lab 1" and missing_count <= 2:
                return "Good"
            else:
                return "Average"
        
        missing_count = len(missing_criteria)
        lab_grade = calculate_lab_grade(
            desc_excellent, 
            missing_count, 
            lab_criteria[lab_name]["bad_threshold"],
            lab_name
        )
        
        lab_grades[lab_name] = lab_grade
        lab_feedback[lab_name] = {
            "excellent": desc_excellent,
            "missing_criteria": missing_criteria,
            "missing_count": missing_count
        }
        
        # Display grade with color coding
        if lab_grade == "Excellent":
            st.success(f"**{lab_name} Grade: {lab_grade}**")
        elif lab_grade == "Good":
            st.info(f"**{lab_name} Grade: {lab_grade}**")
        elif lab_grade == "Average":
            st.warning(f"**{lab_name} Grade: {lab_grade}**")
        else:
            st.error(f"**{lab_name} Grade: {lab_grade}**")
        
        if missing_criteria:
            st.write(f"Missing/Insufficient items ({missing_count}):")
            for criterion in missing_criteria:
                st.write(f"• {criterion}")

st.markdown("---")

# SUMMARY SECTION
st.header("📊 Summary & Feedback")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Overall Grades")
    st.write(f"**Presentation:** {presentation_grade}")
    
    for lab, grade in lab_grades.items():
        color_map = {
            "Excellent": "🟢",
            "Good": "🔵", 
            "Average": "🟡",
            "Bad": "🔴"
        }
        icon = color_map.get(grade, "⚪")
        st.write(f"**{lab}:** {icon} {grade}")

with col2:
    st.subheader("Quick Stats")
    if lab_grades:
        grade_counts = {}
        for grade in lab_grades.values():
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        for grade, count in grade_counts.items():
            st.write(f"{grade}: {count} lab(s)")

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
    if lab_data["excellent"] and not lab_data["missing_criteria"]:
        return f"The description is {grade.lower()} because the descriptions are sufficient and steps are clear with detailed descriptions."
    elif not lab_data["missing_criteria"]:
        return f"The description is {grade.lower()}."
    
    missing_items = lab_data["missing_criteria"]
    
    if len(missing_items) == 1:
        return f"The description is {grade.lower()} because {missing_items[0].lower()}."
    elif len(missing_items) == 2:
        return f"The description is {grade.lower()} because {missing_items[0].lower()} and {missing_items[1].lower()}."
    else:
        items_text = ", ".join(missing_items[:-1]) + f", and {missing_items[-1]}"
        return f"The description is {grade.lower()} because {items_text.lower()}."

feedback_text = f"**Student:** {student_name} ({student_id})\n"
feedback_text += f"**Evaluation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

# Presentation feedback
feedback_text += "**PRESENTATION EVALUATION:**\n"
presentation_feedback = generate_presentation_feedback(presentation_grade, presentation_selection)
feedback_text += presentation_feedback + "\n\n"

# Lab feedback
feedback_text += "**DESCRIPTION EVALUATION:**\n"
for lab_name, grade in lab_grades.items():
    lab_data = lab_feedback[lab_name]
    lab_feedback_text = generate_lab_feedback(lab_name, grade, lab_data)
    feedback_text += f"\n{lab_name}: {lab_feedback_text}\n"

st.text_area("Detailed Feedback", feedback_text, height=300)

# Add individual copy buttons for each section
col1, col2, col3 = st.columns(3)
with col1:
    presentation_feedback_only = generate_presentation_feedback(presentation_grade, presentation_selection)
    if st.button("📋 Copy Presentation Feedback"):
        st.code(presentation_feedback_only, language=None)

with col2:
    description_feedback_only = ""
    for lab_name, grade in lab_grades.items():
        lab_data = lab_feedback[lab_name]
        lab_feedback_text = generate_lab_feedback(lab_name, grade, lab_data)
        description_feedback_only += f"{lab_name}: {lab_feedback_text}\n"
    
    if st.button("📋 Copy Description Feedback"):
        st.code(description_feedback_only, language=None)

with col3:
    if st.button("📋 Copy Complete Feedback"):
        st.code(feedback_text, language=None)

# Export options
st.subheader("Export Options")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Copy Feedback to Clipboard"):
        st.code(feedback_text, language=None)

with col2:
    # Prepare data for CSV export
    csv_data = {
        "Student_ID": [student_id],
        "Student_Name": [student_name],
        "Presentation_Grade": [presentation_grade],
        "Lab1_Grade": [lab_grades.get("Lab 1", "")],
        "Lab2_Grade": [lab_grades.get("Lab 2", "")],
        "Lab3_Grade": [lab_grades.get("Lab 3", "")],
        "Lab4_Grade": [lab_grades.get("Lab 4", "")],
        "Lab5_Grade": [lab_grades.get("Lab 5", "")],
        "Evaluation_Date": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    }
    
    df = pd.DataFrame(csv_data)
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"marking_results_{student_id}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col3:
    # JSON export
    json_data = {
        "student_id": student_id,
        "student_name": student_name,
        "presentation": {
            "grade": presentation_grade,
            "selected_issues": presentation_selection
        },
        "labs": lab_feedback,
        "lab_grades": lab_grades,
        "evaluation_date": datetime.now().isoformat(),
        "feedback": feedback_text
    }
    
    st.download_button(
        label="Download JSON",
        data=json.dumps(json_data, indent=2),
        file_name=f"marking_results_{student_id}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

# Reset button
if st.button("🔄 Reset All Fields"):
    st.session_state.clear()
    st.experimental_rerun()

# Instructions
with st.expander("📖 Instructions"):
    st.markdown("""
    **How to use this marking tool:**
    
    1. **Student Information**: Enter the student ID and name
    2. **Presentation Evaluation**: Select all applicable presentation issues
    3. **Description Evaluation**: For each lab:
       - Select overall description quality
       - Mark any missing/insufficient criteria
    4. **Review Summary**: Check the generated grades and feedback
    5. **Export**: Copy feedback or download results as CSV/JSON
    
    **Grading Logic:**
    - **Presentation**: Excellent (no issues) → Medium (some issues) → Bad (major issues)
    - **Labs**: Excellent (perfect) → Good (≤4 issues for most labs, ≤2 for Lab 1) → Average → Bad (threshold varies by lab)
    
    **Time Estimates:**
    - Lab 1: ~1 min/submission
    - Lab 2: ~1.5 min/submission  
    - Lab 3: ~1.5 min/submission
    - Lab 4: ~1.5 min/submission
    - Lab 5: ~1.5 min/submission
    """)
