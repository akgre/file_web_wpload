from fastapi import FastAPI, Request, File, UploadFile
from fastapi. responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = FastAPI(title="my test app")

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
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
    return {"filename": file.filename}