from PIL import Image
import io
import cv2
import imageio

HEIGHT = 600


def trim_video_opencv(file_name, start, end):
    cap = cv2.VideoCapture(file_name)
    image_lst = []

    fps = cap.get(cv2.CAP_PROP_FPS)
    start_time = start * fps
    end_time = end * fps

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
            image_lst.append(frame)

        i += 1

    cap.release()

    res = io.BytesIO()
    imageio.mimwrite(res, image_lst, format='GIF', fps=fps)

    return res.getvalue()


def image_get_first_frame(file_content):
    imgByteArr = io.BytesIO(file_content)
    res = io.BytesIO()

    image = Image.open(imgByteArr).convert('RGB')
    image.save(res, format='JPEG', subsampling=0, quality=90)

    return res.getvalue()
