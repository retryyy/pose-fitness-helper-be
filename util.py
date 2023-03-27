from PIL import Image
import io
import cv2
import imageio
import numpy as np
import mediapipe as mp

HEIGHT = 600
mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def trim_video_opencv(file_name, start, end):
    cap = cv2.VideoCapture(file_name)
    fps = cap.get(cv2.CAP_PROP_FPS)

    start_time = start * fps
    end_time = end * fps

    frames = []
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if (i >= start_time):
            if i > end_time:
                break
            h, w, _ = frame.shape
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            dims = (int(HEIGHT * w / h), HEIGHT)
            frame = cv2.resize(frame, dims, interpolation=cv2.INTER_AREA)
            frames.append(frame)

        i += 1

    cap.release()

    res = io.BytesIO()
    imageio.mimwrite(res, frames, format='GIF', fps=fps)

    return res.getvalue()


def image_get_first_frame(file_content):
    imgByteArr = io.BytesIO(file_content)
    res = io.BytesIO()

    image = Image.open(imgByteArr).convert('RGB')
    image.save(res, format='JPEG', subsampling=0, quality=90)

    return res.getvalue()


def transform_image(file_content):
    imgByteArr = io.BytesIO(file_content)

    image = Image.open(imgByteArr)
    image.seek(0)

    frames = []
    duration = 0
    try:
        while True:
            duration += image.info['duration']
            image_rgb = np.array(image.convert('RGB'))
            
            results = pose.process(image_rgb)
            mp_draw.draw_landmarks(image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            frames.append(image_rgb)
            image.seek(image.tell() + 1)
    except EOFError:
        fps = len(frames) / duration * 1000

    res = io.BytesIO()
    imageio.mimwrite(res, frames, format='GIF', fps=fps)

    return res.getvalue()
