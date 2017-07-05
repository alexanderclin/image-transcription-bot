# Crops image
from io import BytesIO
from requests import get
from PIL import Image
import numpy as np
import cv2

class ImageCropper:
	"""
	Crops an image given the URL to the image.
	"""

	def __init__(self, img_url):
		self.img_url = img_url
		self.opencv_img = self.__convert_img_to_opencv(img_url)
		self.__grayscale()

	def __convert_img_to_opencv(self, img_url):
		response = get(img_url)
		opencv_img = cv2.imdecode(np.asarray(bytearray(response.content)), 1)
		cv2.imwrite('images/opencv_img.png', opencv_img)
		return opencv_img

	def __grayscale(self):
		img2grey = cv2.cvtColor(self.opencv_img, cv2.COLOR_BGR2GRAY)
		cv2.imwrite('images/grayscale.png', img2grey)

