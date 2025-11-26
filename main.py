from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from fastapi import File, UploadFile
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# ================================
#  EMAIL CONFIG
# ================================
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", "youremail@gmail.com")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "your_app_password")  # App Password
TO_EMAIL = os.environ.get("TO_EMAIL", "recipient@example.com")


# ================================
#  EMAIL ROUTE
# ================================
@app.post("/send-email")
def send_email(subject: str = "سلام از Python", body: str = "این یک ایمیل تستی ساده است"):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return {"status": "ایمیل با موفقیت ارسال شد!"}
    except Exception as e:
        return {"status": "خطا در ارسال ایمیل", "detail": str(e)}


# ================================
#  OTHER ROUTES
# ================================
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

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
#  FILE UPLOAD
# ================================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file": file.filename, "status": "uploaded"}









#========================newadded
from pydantic import BaseModel

class GameResult(BaseModel):
    player: str
    moves: int
    time: int

@app.post("/save_result")
def save_result(data: GameResult):
    # اینجا دیتا را ذخیره می‌کنیم (فعلاً در یک فایل JSON)
    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(f"{data.player} - Moves: {data.moves} - Time: {data.time}\n")

    return {"status": "saved", "data": data}
#========================newadded