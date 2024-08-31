import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
from dotenv import load_dotenv


# Retrieve the API key from an environment variable
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

def getResponse(input_text, no_words, blog_style):
    prompt = f"Summarize the following patent in {no_words} words in a style suitable for {blog_style} and include examples if present in the following patent:\n\n{input_text}"
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

st.set_page_config(page_title="Generate Patent Summary",
                   page_icon='📖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Patent Summary 📖")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

## Creating two more columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('Number of Words', value='400')
with col2:
    blog_style = st.selectbox('Writing style for the summary',
                              ('Researchers', 'Data Scientist', 'Common People'), index=0)

submit = st.button("Generate Summary")

## Final response
if submit and uploaded_file is not None:
    input_text = extract_text_from_pdf(uploaded_file)
    response = getResponse(input_text, no_words, blog_style)
    st.write(response)
elif submit and uploaded_file is None:
    st.write("Please upload a PDF file to proceed.")
