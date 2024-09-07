import base64
import pickle

# Convert audio file to base64
with open("/Users/cry/nabla/blana/test_audio.m4a", "rb") as audio_file:
    base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')
    print(base64_audio)

# Save base64 audio to a pickle file
with open("audio_base64.pkl", "wb") as pkl_file:
    pickle.dump(base64_audio, pkl_file)

print("Audio file has been converted to base64 and saved as a pickle file.")
