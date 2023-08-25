import cv2
from PIL import Image


def extract_middle_frame(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Set the video's position to the random frame
    video.set(cv2.CAP_PROP_POS_FRAMES, total_frames//2)

    # Read the frame
    success, frame = video.read()

    # Release the video object
    video.release()

    # Check if the frame was successfully read
    if success:
        image = Image.fromarray(frame)
        return image
    else:
        return None
