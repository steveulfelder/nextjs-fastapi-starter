from fastapi import FastAPI, Request
import hashlib
import hmac

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

PRODUCT_IDS = {
    'ScormEngine': 1,
    'ContentController': 2,
    'Generator': 3,
    'RusticiCrossDomain': 4,
    'ScormDriver': 5
}

def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """

    if not signature_header:
        return False

    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        return False

    return True


@app.post("/api/py/versions/update_webhook")
async def update_webhook(request: Request):
    payload = await request.json()
    if verify_signature(payload, "secret", request.headers['X-Hub-Signature-256']):
        print("VERIFY PASS")

    # only process release events
    if not payload['action'] or not payload['release']:
        return { "Error": f"Unrecognized event: {payload}" }

    # make sure only events from main RusticiSoftware/ repos are processed
    repo = payload['repository']
    if not repo['full_name'].startswith('RusticiSoftware'):
        return { "Info": f"Fork detected, no action taken" }

    # only operate on repos matched in PRODUCT_IDs
    if repo['name'] not in PRODUCT_IDS:
        return { "Info": f"Unrecognized product, no action taken" }

    # TODO
    if payload['action'] == 'deleted':
        print("TODO: slack DevOps in case we need to delete a version")

    # insert
    if payload['action'] == 'published':
        release = payload['release']
        product_id = PRODUCT_IDS[repo['name']]
        stripped_version = release['tag_name'].lower().replace('v', '')
        release_date = release['published_at'].replace('Z', '').replace('T', ' ')

        product = f"Insert new product versions row: ({product_id}, {stripped_version}, NULL, 1, NULL, {release_date}, 1)"
        print(product)
        return {"message": product}

