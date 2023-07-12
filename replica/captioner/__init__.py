import os
from tqdm import tqdm
from transformers import pipeline

from replica.captioner.video.utils import extract_middle_frame

captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")


def caption_image(image_path: str):
    text = captioner(image_path)[0]['generated_text']
    return text


def caption_files_in_folder(directory: str):
    captionings = {}
    cont = 0
    for filename in tqdm(os.listdir(directory)):
        if cont > 20:
            break
        if os.path.isfile(os.path.join(directory, filename)):
            if filename.endswith('jpg') or filename.endswith('jpeg') or filename.endswith('png'):
                captionings[filename] = caption_image(os.path.join(directory, filename))
            elif filename.endswith('mp4'):
                image = extract_middle_frame(filename)
                if image:
                    captionings[filename] = caption_image(image)
        cont += 1
    return captionings
