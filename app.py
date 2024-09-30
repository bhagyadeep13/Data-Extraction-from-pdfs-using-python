from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import fitz
import re
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure the folder to save uploaded files exists
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Use your existing functions (some may require minor modifications)

def extract_text_and_data(pdf_path, heading, num_words=3):
    try:
        pdf = fitz.open(pdf_path)
        text = ""
        for page in pdf:
            text += page.get_text("text")
        pdf.close()

        title = extract_title(pdf_path)

        journal_pattern = r'\b(journal|proceedings|conference|transactions|magazine|review|letters)\b(?:\s+\w+){0,' + str(num_words) + '}'
        journal_match = re.search(journal_pattern, text, flags=re.IGNORECASE)

        date_match = re.search(r'\b\d{1,2},\s+[A-Z][a-z]+\s+\d{4}\b', text)

        if not date_match:
            footer_text = extract_footer_text(pdf_path)
            year_match = re.search(r'\b(194[7-9]|19[5-9]\d|20[0-1]\d|202[0-4])\b', footer_text)
            date_match = year_match

        emails = ', '.join(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text))

        return title, journal_match.group(0) if journal_match else "Journal Phrase Not Found", date_match.group(0) if date_match else "Not Found", emails if emails else "Not Found"
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return "Error", "Error", "Error", "Error"

def extract_text_before_heading(pdf_path, heading="Abstract"):
    text_before_heading = ""
    try:
        pdf = fitz.open(pdf_path)
        heading_found = False
        
        for page in pdf:
            text_blocks = page.get_text("blocks")
            for block in text_blocks:
                block_text = block[4].strip()
                normalized_text = block_text.lower()

                if heading.lower() in normalized_text:
                    heading_found = True
                    break
                text_before_heading += block_text + ' '

            if heading_found:
                break

        pdf.close()
        return text_before_heading.strip() if text_before_heading else "Not Found"
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return "Error"

# In app.py or another imported file
def split_text_into_chunks(text, chunk_size=5):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def extract_title(pdf_path):
    try:
        pdf = fitz.open(pdf_path)
        first_page = pdf[0]  # Assuming the title is on the first page
        text_blocks = first_page.get_text("blocks")
        
        sorted_blocks = sorted(text_blocks, key=lambda block: block[3] - block[1], reverse=True)
        title = None
        for block in sorted_blocks:
            block_text = block[4].strip()
            if 10 < len(block_text) < 150:
                title = block_text
                break
        pdf.close()
        return title if title else "Title Not Found"
    except Exception as e:
        print(f"Error extracting title from {pdf_path}: {e}")
        return "Error"
        
# Similarly, include other helper functions here (extract_text_before_heading, etc.)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        heading = request.form['heading']

        all_text_chunks = []
        all_main_data = []
        
        # Save uploaded files and process them
        for file in files:
            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Call your processing functions
                title, journal_phrase, first_date, emails = extract_text_and_data(file_path, heading)
                text_before_abstract = extract_text_before_heading(file_path, heading)
                text_chunks = split_text_into_chunks(text_before_abstract, chunk_size=5)
                all_text_chunks.extend([(chunk,) for chunk in text_chunks])
                all_main_data.append((title, journal_phrase, first_date, emails))
        
        # Convert data to Pandas DataFrame
        text_df = pd.DataFrame(all_text_chunks, columns=["Text Before Abstract"])
        main_data_df = pd.DataFrame(all_main_data, columns=["Title", "Journal Phrase", "First Date", "Emails"])

        # Save results to Excel files
        text_path = os.path.join(UPLOAD_FOLDER, 'text_before_abstract.xlsx')
        main_data_path = os.path.join(UPLOAD_FOLDER, 'main_data.xlsx')

        text_df.to_excel(text_path, index=False)
        main_data_df.to_excel(main_data_path, index=False)

        return render_template('result.html', text_file=text_path, data_file=main_data_path)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
