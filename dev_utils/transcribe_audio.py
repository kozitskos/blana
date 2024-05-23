import base64
import tempfile
import pickle
from faster_whisper import WhisperModel

# Load base64 audio from pickle file
with open("audio_base64.pkl", "rb") as pkl_file:
    base64_audio = pickle.load(pkl_file)

# Decode base64 to binary
audio_data = base64.b64decode(base64_audio)

# Save the binary data to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as temp_audio_file:
    temp_audio_file.write(audio_data)
    temp_audio_path = temp_audio_file.name

# Load the model and transcribe the temporary audio file
model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, info = model.transcribe(temp_audio_path, beam_size=5, language="ru", condition_on_previous_text=True)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

# Clean up the temporary file if needed
import os
os.remove(temp_audio_path)
