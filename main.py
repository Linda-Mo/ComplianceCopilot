# main.py
import os, json, time, uuid, jwt, asyncio, aiofiles
from datetime import datetime, timedelta
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Header
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

# --- Load environment ---
load_dotenv()
DEV_MODE = os.getenv("DEV_MODE", "true").lower() in ("1","true","yes")
print("DEV_MODE =", DEV_MODE)
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = "HS256"

app = FastAPI(title="ComplianceCopilot Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Partner placeholders ---
async def call_nebius(text, api_key=None):
    await asyncio.sleep(0.2)
    return {"provider":"nebius","result":f"simulated analysis for: {text}"}

async def call_mistral(text, api_key=None):
    await asyncio.sleep(0.2)
    return {"provider":"mistral","result":f"simulated summary for: {text}"}

async def call_ai_ml(text, api_key=None):
    await asyncio.sleep(0.2)
    return {"provider":"ai_ml","result":f"simulated ai flags for: {text}"}

# --- Models ---
class CreatePaymentReq(BaseModel):
    wallet_address: str
    rental_hours: int = 1
    amount: float = 0.1

# JWT helper
def issue_jwt(wallet: str, agent_id: str="agent-default", hours: int=1, dev_override: bool=False) -> str:
    """
    Create JWT token.
    dev_override=True will create a long-lived token for dev mode.
    """
    now = datetime.utcnow()
    if dev_override:
        exp_time = now + timedelta(days=1)  # 1 day
    else:
        exp_time = now + timedelta(hours=hours)
    payload = {
        "sub": wallet,
        "agent_id": agent_id,
        "iat": int(now.timestamp()),
        "exp": int(exp_time.timestamp())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALG)
    if isinstance(token, bytes):
        token = token.decode()
    return token

# --- Storage folders ---
os.makedirs("uploads/payments", exist_ok=True)
os.makedirs("uploads/docs", exist_ok=True)

# --- Static files ---
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print(f"[DEBUG] Serving static from: {static_dir}")
else:
    print("[WARN] static directory not found:", static_dir)

# --- Endpoints ---
@app.get("/health")
async def health():
    return {"status":"ok","time":time.time()}

@app.post("/create_payment")
async def create_payment(req: CreatePaymentReq):
    reference = str(uuid.uuid4())
    payment_request = {
        "reference": reference,
        "to": os.getenv("SOLANA_RECEIVER", "DemoReceiver1"),
        "amount": req.amount,
        "currency": "SOL",
        "message": f"Rental for {req.wallet_address}"
    }
    with open(f"uploads/payments/{reference}.json","w") as f:
        json.dump({"request": payment_request, "wallet": req.wallet_address}, f)
    return payment_request

# Dev-mode verification
@app.get("/verify_dev")
async def verify_dev(tx_signature: str="dev-ok", wallet_address: str="demo-wallet"):
    if DEV_MODE and tx_signature == "dev-ok":
        token = issue_jwt(wallet_address, dev_override=True)
        return {"status":"verified","token":token}
    raise HTTPException(status_code=400, detail="Only available in dev mode with tx_signature=dev-ok")

@app.post("/upload_document")
async def upload_document(file: UploadFile = File(...), Authorization: str = Header(None)):
    if Authorization is None or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    token = Authorization.split(" ",1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALG])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join("uploads/docs", filename)
    async with aiofiles.open(path, "wb") as out:
        await out.write(await file.read())

    analysis = {
        "ai_ml": await call_ai_ml(filename),
        "mistral": await call_mistral(filename),
        "nebius": await call_nebius(filename)
    }
    return {"status":"done","file":filename,"analysis":analysis,"owner":payload.get("sub")}

@app.get("/sse")
async def sse(request: Request, agentId: str = "web", agentDescription: str = ""):
    async def generator():
        yield f"data: {json.dumps({'event':'connected','agentId':agentId,'desc':agentDescription})}\n\n"
        while True:
            if await request.is_disconnected():
                break
            yield f"data: {json.dumps({'event':'heartbeat','ts':time.time()})}\n\n"
            await asyncio.sleep(2)
    return StreamingResponse(generator(), media_type="text/event-stream")

@app.get("/", include_in_schema=False)
async def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {"message":"Multi-Agent Interface is up and running!"}
