# AI Intern Assessment

This repository includes **both challenges** from the PDF:

1. **The Empathy Engine** — text input, emotion detection, voice parameter modulation, and playable audio output.  
2. **The Pitch Visualizer** — narrative segmentation, prompt engineering, image generation, and storyboard display.

## Project structure

- `empathy_engine/` — Flask app for emotion-aware speech synthesis
- `storyboard_generator/` — Flask app for narrative-to-storyboard generation
- `shared/` — reusable text utilities
- `requirements.txt` — Python dependencies

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Optional API key
For the storyboard generator, set an OpenAI API key to use an image model backend:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_key"

# macOS/Linux
export OPENAI_API_KEY="your_key"
```

If no key is provided, the storyboard app falls back to a local visual renderer so the project still runs end-to-end.

## Run the Empathy Engine

```bash
python -m empathy_engine.app
```

Then open `http://127.0.0.1:5000/` in your browser.

### What it does
- Accepts text input
- Detects emotion using a lightweight rule-based classifier
- Maps emotion to:
  - speech rate
  - volume
  - pitch factor
- Generates a `.wav` file and plays it in the browser

## Run the Pitch Visualizer

In a separate terminal:

```bash
python -m storyboard_generator.app
```

Then open `http://127.0.0.1:5000/` in your browser.

### What it does
- Accepts a paragraph of text
- Splits it into at least three scenes
- Builds richer prompts from each scene
- Generates one image per scene
- Displays the storyboard as a sequence of panels

## Design choices

### Empathy Engine
- Emotion detection uses a compact lexicon-based classifier with categories:
  - **Happy**
  - **Frustrated**
  - **Concerned**
  - **Neutral**
- Voice modulation changes:
  - **rate**
  - **volume**
  - **pitch**
- `pyttsx3` creates the voice output, and `pydub` applies a pitch adjustment in post-processing.

### Pitch Visualizer
- Text is segmented using sentence boundaries first.
- If the input has fewer than 3 sentences, it is split into three balanced chunks.
- Prompt engineering adds:
  - extracted keywords
  - style keywords
  - storytelling instructions
- Image generation uses:
  - OpenAI image API when available
  - a local Pillow-based fallback otherwise

## Deliverables covered

- Text input
- Emotion / scene analysis
- Voice parameter modulation
- Prompt engineering
- Image generation
- Playable audio
- Storyboard presentation

## Notes
The two apps are intentionally separated so each challenge can be demonstrated independently.
