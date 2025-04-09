from fastapi import FastAPI, Request

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.post("/api/py/versions/update_webhook")
async def update_webhook(request: Request):
    payload = await request.json()

    if not payload['action'] or not payload['release']:
        return {"Error": f"Unrecognized event: {payload}"}

    if payload['action'] == 'deleted':
        print("TODO: slack DevOps in case we need to delete a version")

    if payload['action'] == 'published':
        raw_release = payload['release']
        stripped_version = raw_release['tag_name'].lower().replace('v', '')
        release_date = raw_release['published_at'].replace('Z', '').replace('T', ' ')

        product = f"Insert new product versions row: (1, {stripped_version}, NULL, 1, NULL, {release_date}, 1)"
        print(product)
        return {"message": product}

