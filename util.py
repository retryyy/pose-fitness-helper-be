from PIL import Image
import io
import cv2
import imageio
import imageio.v3 as iio
import numpy as np
import mediapipe as mp

HEIGHT = 600
mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def trim_video(file_content, start, end):
    fps = iio.immeta(file_content, plugin="pyav")["fps"]

    start_time = start * fps
    end_time = end * fps

    frames = []
    for frame_count, frame in enumerate(iio.imread(file_content, format_hint=".mp4")):
        if (frame_count >= start_time):
            if frame_count > end_time:
                break
            h, w, _ = frame.shape

            dims = (int(HEIGHT * w / h), HEIGHT)
            frame = cv2.resize(frame, dims, interpolation=cv2.INTER_AREA)
            frames.append(frame)

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
            mp_draw.draw_landmarks(
                image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            frames.append(image_rgb)
            image.seek(image.tell() + 1)
    except EOFError:
        fps = len(frames) / duration * 1000

    res = io.BytesIO()
    imageio.mimwrite(res, frames, format='GIF', fps=fps)

    return res.getvalue()
