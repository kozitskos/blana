from faster_whisper import WhisperModel

model_size = "base"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, info = model.transcribe("/Users/cry/nabla/blana/test_audio.m4a", beam_size=5, language="ru", condition_on_previous_text=True)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))