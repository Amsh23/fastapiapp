from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from fastapi import File, UploadFile
import os
import resend

app = FastAPI()

# ================================
#  RESEND CONFIG
# ================================
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")  # از Render وارد می‌کنی
TO_EMAIL = os.environ.get("TO_EMAIL", "recipient@example.com")

resend.api_key = RESEND_API_KEY


# ================================
#  EMAIL ROUTE (RESEND)
# ================================
@app.post("/send-email")
def send_email(subject: str = "سلام از Python", body: str = "این یک ایمیل تستی ساده است"):
    try:
        response = resend.Emails.send({
            "from": "Project <onboarding@resend.dev>",  # لازم نیست عوضش کنی
            "to": TO_EMAIL,
            "subject": subject,
            "html": f"<p>{body}</p>",
        })

        return {"status": "ایمیل با موفقیت ارسال شد!", "response": response}

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
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/save_result")
async def save_result(file: UploadFile = File(...)):
    contents = await file.read()

    # ذخیره فایل روی سرور
    with open("uploaded_results.txt", "wb") as f:
        f.write(contents)

    return {"status": "file received", "filename": file.filename}

#========================newadded