from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def caesar_cipher(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + key) % 26 + base)
        else:
            result += char
    return result


# ---------- ENCRYPT PAGE ----------
@app.get("/encrypt", response_class=HTMLResponse)
def encrypt_page(request: Request):
    return templates.TemplateResponse(
        "encrypt.html", {"request": request, "result": ""}
    )


@app.post("/encrypt", response_class=HTMLResponse)
def encrypt_text(
    request: Request,
    text: str = Form(...),
    key: int = Form(...)
):
    result = caesar_cipher(text, key)
    return templates.TemplateResponse(
        "encrypt.html", {"request": request, "result": result}
    )


# ---------- DECRYPT PAGE ----------
@app.get("/decrypt", response_class=HTMLResponse)
def decrypt_page(request: Request):
    return templates.TemplateResponse(
        "decrypt.html", {"request": request, "result": ""}
    )


@app.post("/decrypt", response_class=HTMLResponse)
def decrypt_text(
    request: Request,
    text: str = Form(...),
    key: int = Form(...)
):
    result = caesar_cipher(text, -key)
    return templates.TemplateResponse(
        "decrypt.html", {"request": request, "result": result}
    )
