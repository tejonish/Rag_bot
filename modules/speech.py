from faster_whisper import WhisperModel
import tempfile

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(audio):

    if not audio:
        return ""

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as f:

        f.write(audio["bytes"])

        audio_path = f.name

    segments, _ = model.transcribe(audio_path)

    transcript = " ".join(
        segment.text
        for segment in segments
    )

    return transcript