from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import os

# --- APP ---
app = FastAPI()


# --- MODELS ---
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


# --- ROUTES ---
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# ================================
#  EMAIL SYSTEM
# ================================
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

config = ConnectionConfig(
    MAIL_USERNAME="onrender",
    MAIL_PASSWORD="onrender",   # مهم
    MAIL_FROM="onrender",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

@app.post("/send-email")
async def send_email(email: str):
    msg = MessageSchema(
        subject="Hello from FastAPI",
        recipients=[email],
        body="Test message from API",
        subtype="plain"
    )
    fm = FastMail(config)
    await fm.send_message(msg)
    return {"status": "sent"}


# ================================
#  UPLOAD FILE
# ================================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # فولدر uploads اگر نیست بساز
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"file": file.filename, "status": "uploaded"}
