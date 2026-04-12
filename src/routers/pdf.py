from fastapi import APIRouter, UploadFile, File
from pypdf import PdfReader
import tempfile
import os
import re

router = APIRouter()

# --- odczyt PDF ---
def read_pdf(path: str) -> str:
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Błąd PDF: {e}")
        return ""

def summarize_text(text: str, max_sentences: int = 3) -> str:
    text = re.sub(r'\s+', ' ', text) 
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 50]
    summary = sentences[:max_sentences]
    return "\n- " + "\n- ".join(summary)

# --- klasyfikacja ---
def classify(text: str) -> str:
    t = text.lower()
    if "wezwanie" in t:
        return "wezwanie"
    elif "decyzja" in t:
        return "decyzja"
    elif "odpowiedź" in t or "odpowiedz" in t:
        return "odpowiedz"
    return "inne"

# --- ENDPOINT ---
@router.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    # zapis tymczasowy
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        text = read_pdf(tmp_path)

        if not text:
            return {
                "filename": file.filename,
                "error": "Brak tekstu (możliwy skan PDF)"
            }

        summary = summarize_text(text)
        category = classify(text)

        # --- zapis do pliku ---
        os.makedirs("results", exist_ok=True)

        safe_name = file.filename.replace(" ", "_")
        output_path = f"results/{safe_name}.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Plik: {file.filename}\n")
            f.write(f"Kategoria: {category}\n\n")
            f.write("Streszczenie:\n")
            f.write(summary)

        return {
            "filename": file.filename,
            "category": category,
            "summary": summary
        }

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
