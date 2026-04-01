from __future__ import annotations

from flask import Flask, render_template, request, send_file
from pathlib import Path
from datetime import datetime

from empathy_engine.emotion import analyze_emotion, emotion_to_voice
from empathy_engine.tts_engine import synthesize_audio

APP_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = APP_ROOT / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

INDEX_HTML = 'index.html'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    audio_file = None
    text = ''

    if request.method == 'POST':
        text = (request.form.get('text') or '').strip()
        if text:
            emotion = analyze_emotion(text)
            voice = emotion_to_voice(emotion)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            out_path = OUTPUT_DIR / f'empathy_{timestamp}.wav'
            synthesize_audio(
                text=text,
                output_path=str(out_path),
                rate=voice['rate'],
                volume=voice['volume'],
                pitch=voice['pitch'],
            )
            result = {
                'emotion': emotion.label,
                'confidence': emotion.confidence,
                'polarity': emotion.polarity,
                'voice': voice,
            }
            audio_file = f'/download/{out_path.name}'

    return render_template(INDEX_HTML, result=result, audio_file=audio_file, text=text)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(OUTPUT_DIR / filename, mimetype='audio/wav', as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
