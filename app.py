import sys
import streamlit as st
from PIL import Image

from helper import mine_document

# Title
st.title("AI-based Document Analysis")

# Instruction
st.write("Please upload a document for analysis")

# File uploader allows user to upload their PDF file
file = st.file_uploader("Upload a PDF document", type=['pdf'])

# check if a file is uploaded
if file is not None:

  # convert the file to bytes
  pdf_bytes = file.read()

  # Then use PyPDF2 or other PDF processing libraries to process the pdf file
  # note: this might require additional steps since file uploaded is in bytes

  # you may have to write the bytes data to a temporary file before using it
  with open("temp.pdf", "wb") as f:
    f.write(pdf_bytes)

  # call your mine_case or summarize_article function on the temp file
  result = mine_document('temp.pdf') # or summarize_article('temp.pdf')

  # display the results on Streamlit
  st.write(result)
