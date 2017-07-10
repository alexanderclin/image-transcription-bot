# Transcribes image

from PIL import Image
from pytesseract import image_to_string
from io import BytesIO
from requests import get

class ImageTranscriber:
    """
    Used to transcribe an image to text.
    """

    def __init__(self, img_url):
        self.img_url = img_url
        self.text = self.__convert_image(img_url)

    def __convert_image(self, img_url):
        """
        Gets image from url and converts it to text
        """
        response = get(img_url)
        img_from_url = Image.open(BytesIO(response.content))
        return image_to_string(img_from_url)

class ImageTranscriberWithExisting:
    """
    Transcribe image that already exists as a PIL Image
    """

    def __init__(self, img):
        self.img = img
        self.text = self.__convert_image(img)

    def __convert_image(self, img):
        return image_to_string(img)