# server_wit
פרויקט שרת בפייתון
CodeGuard – Code Analysis System
overview
CodeGuard is a code analysis system integrated with the wit push command to ensure high code quality in every commit. The system performs code quality checks and returns visual graphs with insights and data about issues in the code.

This simulates a basic form of Continuous Integration (CI), focused on code quality.
Technologies used:
Language: Python

Backend Framework: FastAPI

Code Analysis: ast (Abstract Syntax Tree)

Visualization: matplotlib
 Installation Instructions:
clone the repository
git clone https://github.com/nechamajobs/server_wit
cd server_wit
 Create a virtual environment & install dependencies
 python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
 Run the server
 uvicorn Main:app --reload
 Server will be available at: http://127.0.0.1:8001

 API Endpoints

 /analyze	POST	Accepts Python files and returns analysis graphs (PNG)
/alerts	POST	Accepts Python files and returns code issue alerts

code Quality checks

Function Length: Warn if a function is longer than 20 lines.

File Length: Warn if the entire file is longer than 200 lines.

Unused Variables: Warn if variables are defined but never used.

Missing Docstrings: Warn if a function has no documentation string.
 
Visualizations

Histogram – Distribution of function lengths

 Pie Chart – Number of issues by type
 
 Bar Chart – Number of issues by file

 •	Folder structure of the project
 static /histogram.png issues_pie.png issues_bar.png
 analyze
 diagram
 Main
