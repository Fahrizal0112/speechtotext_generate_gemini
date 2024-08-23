from flask import Flask, request, jsonify
import google.generativeai as genai
import speech_recognition as sr
import os

app = Flask(__name__)

genai.configure(api_key="AIzaSyAB4o8VpccbEeM_jlCOIezJGYRDoA488Ig")

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        recognizer = sr.Recognizer()
        audio_file = sr.AudioFile(file)
        
        with audio_file as source:
            audio = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio, language="id-ID")
        except sr.UnknownValueError:
            return jsonify({"error": "Speech recognition could not understand audio"}), 400
        except sr.RequestError:
            return jsonify({"error": "Could not request results from speech recognition service"}), 500
        
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Buatkan ringkasan dari teks berikut:\n\n{text}"
        
        response = model.generate_content(prompt)
        
        summary = response.text
        
        return jsonify({
            "original_text": text,
            "summary": summary
        })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
