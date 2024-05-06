from PIL import Image
import io
import cv2
import imageio
import imageio.v3 as iio
import numpy as np
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


HEIGHT = 400
ALPHA = 0.4
ALL_POINTS = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

def trim_video(file_content, start, end, needed_points):
    needed_points = ALL_POINTS if needed_points is None else needed_points
    fps = iio.immeta(file_content, plugin="pyav")["fps"]

    start_time = start * fps
    end_time = end * fps

    frames = []
    frames_points = []
    pose = mp_pose.Pose()

    for frame_count, frame in enumerate(iio.imiter(file_content, extension=".mp4")):
        if (frame_count >= start_time):
            if frame_count > end_time:
                break
            h, w, _ = frame.shape

            dims = (int(HEIGHT * w / h), HEIGHT)
            frame = cv2.resize(frame, dims, interpolation=cv2.INTER_AREA)
            h, w, _ = frame.shape

            results = pose.process(frame)

            points = {}
            if results.pose_landmarks:
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    if id not in needed_points:
                        continue

                    points[str(id)] = (int(lm.x * w), int(lm.y * h))

                shapes = np.zeros_like(frame, np.uint8)

                pose_connections = frozenset(
                    {(p1, p2) for p1, p2 in mp_pose.POSE_CONNECTIONS if p1 in needed_points and p2 in needed_points}
                )

                for p1, p2 in pose_connections:
                    cv2.line(shapes, points[str(p1)], points[str(p2)],
                             (255, 255, 255), thickness=4, lineType=8)

                mask = shapes.astype(bool)
                frame[mask] = cv2.addWeighted(
                    frame, ALPHA, shapes, 1 - ALPHA, 0)[mask]

                for _, (x, y) in points.items():
                    cv2.circle(frame, (x, y), 6, (255, 0, 0), cv2.FILLED)

            frames.append(frame)
            points = {point: (x, h - y) for point, (x, y) in points.items()}
            frames_points.append(points)

    res = io.BytesIO()
    imageio.mimwrite(res, frames, format='GIF', fps=fps)

    return res.getvalue(), frames_points


def image_get_first_frame(file_content):
    imgByteArr = io.BytesIO(file_content)
    res = io.BytesIO()

    image = Image.open(imgByteArr).convert('RGB')
    image.save(res, format='JPEG', subsampling=0, quality=90)

    return res.getvalue()
