from fastapi import FastAPI

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = FastAPI(title="my test app")


@app.get('/')
def hello():
    """Return a friendly HTTP greeting.
    ![alt text](https://media.istockphoto.com/id/523495902/vector/wind-station-alternative-energy-generation-resource-nature-background-banner.webp?s=2048x2048&w=is&k=20&c=_Fm-iFeceJh0bR7pZQkk144sukdbfjgL0lC_mDBy5aQ=)"""
    return {'message': 'Hello World!', "additional": "bob"}