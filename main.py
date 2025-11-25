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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# اطلاعات ایمیل فرستنده و گیرنده
EMAIL_ADDRESS = 'youremail@gmail.com'
EMAIL_PASSWORD = 'your_app_password'  # حتما از App Password استفاده کن
TO_EMAIL = 'recipient@example.com'

# ساخت پیام
msg = MIMEMultipart()
msg['From'] = EMAIL_ADDRESS
msg['To'] = TO_EMAIL
msg['Subject'] = 'سلام از Python'
msg.attach(MIMEText('این یک ایمیل تستی ساده است', 'plain'))

# اتصال به سرور SMTP و ارسال ایمیل
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    print("ایمیل با موفقیت ارسال شد!")
except Exception as e:
    print("خطا در ارسال ایمیل:", e)



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
