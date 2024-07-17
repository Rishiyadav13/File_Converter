# Fille_Converter:

This application is desinged to convert html to pdf or docx to pdf, the application is built on django and javascript is also used in it.


## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Things Implemented](#things-implemented)
  

## Features 

- Convert HTML files to PDF files. 
- Convert Word documents (.docx) to PDF files.
- Download and view section is there.
- Profile section to see or update profile.


## Setup 

Ensure you have the following installed:

- Python 3.6 or higher
- pip (Python package installer)


1. **Clone the repository:**

   ```bash
   git clone (https://github.com/Rishiyadav13/File_Converter.git)
   cd File_Converter
   ```
   
2. **Create a virtual environment and activate it:**
   
 ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   cd Converter
   ```
    
3. **Install the required packages:**
   
   ```bash
   pip install -r requirement.txt
   ```
   
5. **Run the application:**

   ```bash
   python manage.py runserver
   ``` 
Now you are good to go.


## Usage

### Convert HTML to PDF 

1. Upload a HTML file using the provided form.
2. Click on "HTML To PDF".
3. After uploading the file now you can choose whether to view online or to download it.

### Convert DOCX to PDF 

1. Upload a DOCX file using the provided form.
2. Click on "DOCX To PDF".
3. After uploading the file now you can choose whether to view online or to download it.


## Things Implemented

1. Capcha is implemnted in it.
2. Mail sending is done by using Signals in the project.
3. Logger is also there.
4. Nosql database is integrated in it(Mongodb).
5. Sentry is also implemented to detect the error befor it occur.
6. Payment integration.
7. Settings is distributed in to dev, prod and base.
    






