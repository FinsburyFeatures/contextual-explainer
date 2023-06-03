import sys
import streamlit as st
from PIL import Image

from helper import mine_document
from audio import generate_audio_file

# Title
st.title("PreReader")

# Instruction
st.write("Please upload your document to get your pre-reading snippets")

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
    result = mine_document('temp.pdf')  # or summarize_article('temp.pdf')

    generate_audio_file(result, "explanations")
    with open('explanations.mp3', 'rb') as f:
        audio_data = f.read()

    # display the results on Streamlit
    st.write(result)
    st.download_button("Download as MP3", audio_data,
                       file_name="explanations.mp3")
