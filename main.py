from fastapi import FastAPI, Request, File, UploadFile
from fastapi. responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import csv
import string


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = FastAPI(title="my test app")

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.get('/hello')
def hello():
    """Return a friendly HTTP greeting.
    ![alt text](https://media.istockphoto.com/id/523495902/vector/wind-station-alternative-energy-generation-resource-nature-background-banner.webp?s=2048x2048&w=is&k=20&c=_Fm-iFeceJh0bR7pZQkk144sukdbfjgL0lC_mDBy5aQ=)"""
    return {'message': 'Hello World!', "additional": "bob"}


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    if "csv" not in file.content_type:
        return {"error": "Not a csv"}

    try:
        file_as_bytes = await file.read()
        file_as_string = file_as_bytes.decode("utf-8")

        # isprintable does not allow newlines, printable does not allow umlauts...
        if not all([c in string.printable or c.isprintable() for c in file_as_string]):
            raise csv.Error

        dialect = csv.Sniffer().sniff(file_as_string)

        file_content = csv.reader(file_as_string, delimiter=dialect.delimiter)

    except csv.Error:
        # Could not get a csv dialect -> probably not a csv.
        return {"error": "Could not get a csv dialect -> probably not a csv."}

    print(file_content)
    if any([cell.strip() == "" for cell in file_content[0]]):
        error_list = []
        for _count, cell in enumerate(file_content[0]):
            if cell == "":
                error_list.append(f"Header cell {_count+1} is empty")
        return {"filename": file.filename,
                "errors": error_list}

    return {"filename": file.filename, "dialect": dialect}
