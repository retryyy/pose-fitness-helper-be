from PIL import Image
import io
import cv2
import imageio
import imageio.v3 as iio
import numpy as np
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

HEIGHT = 400
ALPHA = 0.4
NEEDED_POINTS = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
POSE_CONNECTIONS = frozenset(
    {(p1, p2) for p1, p2 in mp_pose.POSE_CONNECTIONS if p1 in NEEDED_POINTS and p2 in NEEDED_POINTS})


def trim_video(file_content, start, end):
    fps = iio.immeta(file_content, plugin="pyav")["fps"]

    start_time = start * fps
    end_time = end * fps

    frames = []
    for frame_count, frame in enumerate(iio.imiter(file_content, extension=".mp4")):
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
    frames_points = []
    duration = 0
    try:
        while True:
            points = {}
            duration += image.info['duration']
            image_rgb = np.array(image.convert('RGB'))

            results = pose.process(image_rgb)

            if results.pose_landmarks:
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    if id not in NEEDED_POINTS:
                        continue

                    h, w, _ = image_rgb.shape
                    points[str(id)] = (int(lm.x * w), int(lm.y * h))

                shapes = np.zeros_like(image_rgb, np.uint8)

                for p1, p2 in POSE_CONNECTIONS:
                    cv2.line(shapes, points[str(p1)], points[str(p2)],
                            (255, 255, 255), thickness=4, lineType=8)

                mask = shapes.astype(bool)
                image_rgb[mask] = cv2.addWeighted(
                    image_rgb, ALPHA, shapes, 1 - ALPHA, 0)[mask]

                for _, (x, y) in points.items():
                    cv2.circle(image_rgb, (x, y), 6, (255, 0, 0), cv2.FILLED)

            frames.append(image_rgb)
            frames_points.append(points)
            image.seek(image.tell() + 1)
    except EOFError:
        fps = len(frames) / duration * 1000

    res = io.BytesIO()
    imageio.mimwrite(res, frames, format='GIF', fps=fps)

    return res.getvalue(), frames_points
