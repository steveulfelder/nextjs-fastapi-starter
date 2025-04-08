from fastapi import FastAPI, Request

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.post("/api/py/versions/update_webhook")
async def update_webhook(request: Request):
    payload = await request.json()
    print(payload)
    return {"message": payload}