from fastapi import FastAPI, Request

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.post("/api/py/versions/update_webhook")
async def update_webhook(request: Request):
    payload = await request.json()

    if not payload['action']:
        return {"Error": f"Unrecognized event: {payload}"}

    if payload['action'] == 'deleted':
        print("TODO: slack DevOps in case we need to delete a version")

    stripped_version = payload['tag_name'].lower().replace('v', '')
    release_date = payload['published_at'].replace('Z', '').replace('T', ' ')

    product = f"Insert new product versions row: (1, {stripped_version}, NULL, 1, NULL, {release_date}, 1)"
    print(product)
    return {"message": product}

