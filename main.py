import tkinter as tk
from tkinter import filedialog, messagebox
import io
import requests
import pygame
import pdfplumber
import os
from dotenv import load_dotenv



load_dotenv()
api_key = os.environ.get("ELEVENLABS_API_KEY")

root = tk.Tk()
root.withdraw()




def get_pdf():
    pdf_path = filedialog.askopenfilename(
        title="Select PDF file",
        filetypes=[("PDF file", "*.pdf")],
    )
    if not pdf_path:
        return None
    return pdf_path


def extract_text(path):
    all_text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text.append(page_text)

    return" ".join(all_text)



def chunk_text(text):
    text_split = text.split(". ")
    current_chunk = []
    chunks = []
    for chunk in text_split:
        current_chunk.append(chunk)
        if len(' '.join(current_chunk)) > 5000:
            chunks.append('. '.join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append('. '.join(current_chunk))
    return chunks

def speak_chunk(chuck, api_key):
    url = "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb"
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json',
    }
    body = {
        'text': chuck,
        'model_id': 'eleven_turbo_v2_5'
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        print(f'API error: {response.status_code} - {response.text}')
        return None
    return response.content

def play_audio(mp3_bytes):
    pygame.mixer.init()
    audio = io.BytesIO(mp3_bytes)
    pygame.mixer.music.load(audio, 'mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)


def main():
    pdf_path = get_pdf()
    if not pdf_path:
        print("No file selected.")
        return
    text = extract_text(pdf_path)
    if not text:
        print("No text found in pdf.")
        return
    chunks = chunk_text(text)
    print(f'Split into {len(chunks)} chunk(s).')

    for i, chunk in enumerate(chunks):
        print(f"Speaking chunk {i + 1} of {len(chunks)}...")
        mp3_bytes = speak_chunk(chunk, api_key)
        if mp3_bytes:
            play_audio(mp3_bytes)







main()