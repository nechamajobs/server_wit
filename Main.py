import ast

from fastapi import FastAPI,File,UploadFile
from Diagram import get_function_lengths,generate_histogram,generate_pie_chart,count_of_problems,generate_bar_chart,collect_all_warnings

from anslyze import analyze_code
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

@app.post("/analyze")
async def analyze(files: List[UploadFile] = File(...)):
    file_contents = []
    filenames = []

    for file in files:
        content = (await file.read()).decode("utf-8")
        file_contents.append(content)
        filenames.append(file.filename)


    problems_per_file = count_of_problems(file_contents, filenames)


    generate_bar_chart(problems_per_file, "static/issues_bar.png")



    tree = ast.parse(file_contents[0])
    length = get_function_lengths(tree)
    generate_histogram(length, "static/histogram.png")
    all_warnings = collect_all_warnings(file_contents)
    generate_pie_chart(all_warnings, "static/issues_pie.png")

    return {
        "histogram": "/static/histogram.png",
        "pie_chart": "/static/issues_pie.png",
        "bar_chart": "/static/issues_bar.png",
        "warnings": warnings,
        "file_warnings_count": problems_per_file
    }


@app.post("/alerts")
async def analyze_file(file: UploadFile = File(...)):
    try:
        source_code = (await file.read()).decode("utf-8")
        warnings = analyze_code(source_code)
        return {"warnings": warnings}
    except Exception as e:
        return {"error": str(e)}

app.mount("/static", StaticFiles(directory="static"), name="static")


