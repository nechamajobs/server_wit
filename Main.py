import ast
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from Diagram import (
    get_function_lengths,
    generate_histogram,
    generate_pie_chart,
    generate_bar_chart,
    count_of_problems,
    collect_all_warnings
)
from anslyze import analyze_code

import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# סיומות מותרים (ניתנים להרחבה)
ALLOWED_EXTENSIONS = {".py", ".js", ".java", ".c", ".cpp", ".cs"}

def is_code_file(filename: str) -> bool:
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

@app.post("/analyze")
async def analyze(files: List[UploadFile] = File(...)):
    file_contents = []
    filenames = []

    for file in files:
        if not is_code_file(file.filename):
            raise HTTPException(status_code=400, detail=f"❌ הקובץ {file.filename} אינו קובץ קוד נתמך.")
        try:
            content = (await file.read()).decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail=f"❌ הקובץ {file.filename} אינו קובץ טקסט קריא.")
        file_contents.append(content)
        filenames.append(file.filename)

    # גרף עמודות לכל הקבצים
    problems_per_file = count_of_problems(file_contents, filenames)
    generate_bar_chart(problems_per_file, "static/issues_bar.png")

    # גרף היסטוגרמה רק אם קובץ ראשון הוא פייתון
    try:
        if filenames[0].endswith(".py"):
            tree = ast.parse(file_contents[0])
            length = get_function_lengths(tree)
            generate_histogram(length, "static/histogram.png")
        else:
            generate_histogram([], "static/histogram.png")  # גרף ריק
    except Exception:
        generate_histogram([], "static/histogram.png")  # גרף ריק אם יש שגיאה

    # תרשים עוגה לכל הקבצים
    all_warnings = collect_all_warnings(file_contents)
    generate_pie_chart(all_warnings, "static/issues_pie.png")

    return {
        "histogram": "/static/histogram.png",
        "pie_chart": "/static/issues_pie.png",
        "bar_chart": "/static/issues_bar.png",
        "warnings": all_warnings,
        "file_warnings_count": problems_per_file
    }

@app.post("/alerts")
async def analyze_file(file: UploadFile = File(...)):
    try:
        if not is_code_file(file.filename):
            raise HTTPException(status_code=400, detail="❌ הקובץ שהועלה אינו קובץ קוד נתמך.")
            print("אחד הקבצים אינו קובץ קוד")
        source_code = (await file.read()).decode("utf-8")
        warnings = analyze_code(source_code)
        return {"warnings": warnings}
    except Exception as e:
        return {"error": f"שגיאה בניתוח הקובץ: {str(e)}"}
