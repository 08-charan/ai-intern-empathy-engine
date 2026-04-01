from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from pydub import AudioSegment
import pyttsx3


def _change_pitch(segment: AudioSegment, pitch_factor: float) -> AudioSegment:
    if pitch_factor <= 0:
        return segment
    new_frame_rate = int(segment.frame_rate * pitch_factor)
    pitched = segment._spawn(segment.raw_data, overrides={'frame_rate': new_frame_rate})
    return pitched.set_frame_rate(segment.frame_rate)


def synthesize_audio(text: str, output_path: str, rate: int = 175, volume: float = 0.9, pitch: float = 1.0) -> str:
    """Generate a WAV file with modulated rate, volume, and pitch."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with TemporaryDirectory() as tmp:
        raw_wav = Path(tmp) / 'raw.wav'
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', max(0.0, min(1.0, volume)))
        engine.save_to_file(text, str(raw_wav))
        engine.runAndWait()

        if not raw_wav.exists():
            raise RuntimeError('TTS engine did not produce an audio file.')

        audio = AudioSegment.from_wav(raw_wav)
        audio = _change_pitch(audio, pitch)
        audio.export(output, format='wav')

    return str(output)
