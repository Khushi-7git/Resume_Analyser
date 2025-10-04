# Resume_Analyser
🤖 Smart AI Recruiter with SQLite & Chatbot
Overview

This project is a demo AI Recruiter application built using Python, Streamlit, SQLite, and spaCy.
It allows users to:

Upload resumes in PDF format.

Extract skills automatically using NLP.

Match candidate skills with a job description.

Get a career advice chatbot for general guidance.

The project demonstrates database management, text processing, and basic AI chatbot integration, making it suitable for a Database Systems (DBS) project demo.

**Features**

1.Resume Upload

Users can upload resumes in PDF format.

2.Candidate information is stored in a SQLite relational database.

3.Skill Extraction

4.Automatically extracts relevant skills from the resume using spaCy NLP.

5.Skill Matching

6.Compares candidate skills with a job description.

Highlights missing skills.

1.Provides a match percentage score.

2.Career Advice Chatbot

3.Rule-based chatbot answering basic career and skill improvement questions.

**Example queries:**

*"What is a frontend developer?"

*"How to improve skills?"

*"Resume tips?"

**Object-Oriented Programming (OOP)**

Database operations handled by ResumeDB class.

Resume processing handled by ResumeProcessor class.

Chatbot handled by CareerChatbot class.

Clean modular code for maintainability and extension.

**Tech Stack**

1.Python 3.x

2.Streamlit for web interface

3.SQLite for relational database storage

4.spaCy for NLP skill extraction

5.pdfplumber for reading PDF resumes
