from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, send_file

from storyboard_generator.story import build_story_scenes
from storyboard_generator.image_backend import generate_image

APP_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = APP_ROOT / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    storyboard = []
    text = ''
    style = 'cinematic'

    if request.method == 'POST':
        text = (request.form.get('text') or '').strip()
        style = (request.form.get('style') or 'cinematic').strip()
        if text:
            scenes = build_story_scenes(text, style=style)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            for idx, scene in enumerate(scenes, start=1):
                img_path = OUTPUT_DIR / f'story_{timestamp}_{idx}.png'
                generate_image(scene.prompt, scene.caption, str(img_path), style=style)
                storyboard.append({
                    'caption': scene.caption,
                    'prompt': scene.prompt,
                    'image_url': f'/download/{img_path.name}',
                })

    return render_template('index.html', storyboard=storyboard, text=text, style=style)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(OUTPUT_DIR / filename, mimetype='image/png', as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
