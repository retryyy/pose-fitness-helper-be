from PIL import Image
import io


def image_to_byte_array(file_path) -> bytes:
    image = Image.open(file_path)
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format, save_all=True)
    return imgByteArr.getvalue()
