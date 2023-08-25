import whisper
import os
from tqdm import tqdm

model = whisper.load_model("base")


def transcribe_audio(audio_path: str):
    result = model.transcribe(audio_path)
    return result["text"]


def transcribe_files_in_folder(directory: str):
    transcriptions = {}
    for filename in tqdm(os.listdir(directory)):
        if os.path.isfile(os.path.join(directory, filename)):
            if filename.endswith('wav') or filename.endswith('m2a') or filename.endswith('mp4') or filename.endswith('m4a'):
                transcriptions[filename] = transcribe_audio(os.path.join(directory, filename))
                print(transcriptions[filename])
            else:
                print(filename)
    return transcriptions
