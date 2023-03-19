from PIL import Image
import io


def image_to_byte_array(file_path) -> bytes:
    image = Image.open(file_path)
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format, save_all=True)
    return imgByteArr.getvalue()


def image_get_first_frame(file_content):
    imgByteArr = io.BytesIO(file_content)
    res = io.BytesIO()

    image = Image.open(imgByteArr)
    image.save(res, format=image.format)
    return res.getvalue()
