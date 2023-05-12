# -*- coding: utf-8 -*-
"""
Created on Fri May 12 16:32:30 2023

@author: mromg
"""

import pandas as pd 
from transformers import pipeline
import PyPDF2
from PyPDF2 import PdfReader
import docx
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_types = [('PDF Files', '*.pdf'), ('Word Files', '*.docx;*.doc')]
file_path = filedialog.askopenfilename(filetypes=file_types)


try:
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)
        
        # Get the number of pages in the PDF file
        num_pages = len(reader.pages)
        
        # Loop through all the pages and extract the text
        text = ''
        for page in range(num_pages):
            # Get the page object
            page_obj = reader.pages[page]
            
            # Extract the text from the page
            page_text = page_obj.extract_text()
            
            # Add the page text to the overall text
            text += page_text
except:
    doc = docx.Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    
summarize = pipeline("summarization", model = "philschmid/flan-t5-base-samsum")


new_text = summarize(text, max_length = input(), min_length = input())