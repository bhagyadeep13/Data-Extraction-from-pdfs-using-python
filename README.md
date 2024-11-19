
# Research Paper PDF Extraction System

This project, Research Paper PDF Extraction, automates the extraction of structured information from research papers in PDF format and saves the data into Excel files. It is a web-based application designed for academic and research purposes, enabling users to efficiently process multiple PDFs and download the results.


## Features

- PDF Upload: Upload one or multiple research papers in PDF format.
- Data Extraction:
    - Title: Extracted from the first page.
    - Date: Identified using regex patterns.
    - Emails: Extracted using regex patterns.
    - Journal Name: Extracted using keyword identification.
    - Abstract Text: Text preceding a specified heading   (default: "Abstract").
- Excel Output:
    - Text Before Abstract: Contains text chunks before the specified heading.
    - Main Data: Includes Title, Journal Name, Date, and Emails.
- Download Functionality: Allows downloading the generated Excel files.



## System Architecture

The system consists of:

- Frontend: Web interface for user interaction.
- Backend:
    - File upload mechanism.
    - PDF processing and data extraction.
- Output Generation:
    - Converts extracted data into downloadable Excel files.
## Technical Stack

- Backend: Flask
- PDF Processing: PyMuPDF (Fitz)
- Data Manipulation: Pandas
- Frontend: Bootstrap
## Usage 
- Navigate to the upload page.
- Select one or more PDF files and specify the heading for text extraction (default: "Abstract").
- Click Upload to process the files.
- Once processing is complete, download the generated Excel files from the results page.

## Input and Output Formats

- Input:
    - PDF Files: Research papers in PDF format.
    - Heading: A text input specifying the section heading (default: "Abstract").
- Output:
    - Text Before Abstract Excel File:
        - Contains chunks of text extracted before the specified heading.
        - Each row represents a chunk of text.
- Main Data Excel File:
    - Columns include:
        - Title
        - Journal Name
        - Date
        - Email
## References

- Flask Documentation
- PyMuPDF Documentation
- Python Regular Expressions
- Bootstrap Documentation
## Contributers

- Bhagyadeep Mahawar (0801CS221041)
- Guided By:

    - Ashwini Sharma Ma’am
    - Mamta Gupta Ma’am
