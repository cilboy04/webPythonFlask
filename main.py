import os
from dotenv import load_dotenv
from groq import Groq
from flask import Flask, render_template, request
from datetime import datetime

load_dotenv()

app = Flask(__name__)

AI_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=AI_KEY)

def ai_call(year):
    try:
        chat_completion = client.chat.completions.create(
            messages= [
                {
                    "role": "user",
                    "content": f"berikan satu fakta menarik seputar teknologi pada tahun {year}, Jawab singkat.",
                }
            ], 
            model="llama-3.2-1b-preview",
            stream=False,
        )
        ai_output = chat_completion.choices[0].message.content
        return ai_output
    except Exception:
        return "Maaf Saat Ini Fitur AI saat ini tidak bisa digunakan"

@app.route("/")
def home():
    title = "Website Python Flask"
    return render_template('home.html', title= title)

@app.route("/about")
def about():
    title = "Copyright © 2025 by Acil"
    return render_template('about.html', title= title)
@app.route("/hitung_usia", methods=['GET', 'POST'])
def cek_usia():
    title = "Cek Usia Anda"
    if request.method == 'POST':
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir
        ai_output= ai_call(tahun_lahir)
        print(ai_output)
        return render_template('cek_usia.html', usia= usia, title= title, ai_output= ai_output)
    return render_template('cek_usia.html', title= title, usia= None)

if __name__=="__main__":
    app.run(host='0.0.0.0')
