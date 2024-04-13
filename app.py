import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()  # load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst,
and big data engineer. Your task is to evaluate the resume based on the given job description.
give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
You must consider the job market is very competitive and you should provide
best assistance for improving the resumes. Assign the percentage Matching based
on JD and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords": [],"Profile Summary": ""}}
"""

# streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))

        # Display results
        st.subheader("Result:")
        st.json(response)

        # Allow users to choose to see the percentage
        show_percentage = st.checkbox("Show Percentage")
        if show_percentage:
            # Extract and display the percentage
            try:
                result_json = json.loads(response)
                jd_match_percentage = result_json.get("JD Match", "")
                st.text(f"JD Match Percentage: {jd_match_percentage}")
            except json.JSONDecodeError:
                st.warning("Unable to extract percentage from the response.")