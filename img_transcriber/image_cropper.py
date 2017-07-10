# Crops image
from io import BytesIO
from requests import get
from PIL import Image
import numpy as np
import cv2

from image_transcriber import ImageTranscriberWithExisting

class ImageCropper:
	"""
	Crops an image given the URL to the image.
	Inspired by https://stackoverflow.com/questions/24385714
	"""

	def __init__(self, img_url):
		self.img_url = img_url
		self.opencv_img = self.__convert_url_to_opencv(img_url)
		self.removed_grey = self.__remove_grey()
		self.simple_img = self.__simplify_img()

	def __convert_url_to_opencv(self, img_url):
		response = get(img_url)
		opencv_img = cv2.imdecode(np.asarray(bytearray(response.content)), 1)
		return opencv_img

	def __convert_opencv_to_PIL(self, cv_img):
		img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
		img_pil = Image.fromarray(img)
		return img_pil

	def __remove_grey(self):
		img2grey = cv2.cvtColor(self.opencv_img, cv2.COLOR_BGR2GRAY)
		(ret, mask) = cv2.threshold(img2grey, 180, 255, cv2.THRESH_BINARY)
		removedgrey_1 = cv2.bitwise_and(img2grey, img2grey, mask=mask)

		# If white background, invert colors
		(ret, removedgrey) = cv2.threshold(removedgrey_1, 180, 255, cv2.THRESH_BINARY)
		avg = np.average(np.average(removedgrey, axis=0), axis=0)
		if avg > 100:
			(ret, removedgrey) = cv2.threshold(removedgrey_1, 180, 255, cv2.THRESH_BINARY_INV)

		return removedgrey

	def __simplify_img(self):
		greyed = self.removed_grey
		color_image = self.opencv_img

		(height, width, _) = color_image.shape
		empty_img = np.zeros((height,width,3), np.uint8)
		empty_img[:,:] = (255, 255, 255)
		new_img = empty_img

		kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
		dilated = cv2.dilate(greyed, kernel, iterations=15)

		(img, contours, heirarchy) = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for contour in contours:
			[x, y, w, h] = cv2.boundingRect(contour)
			if w < 50 and h < 50: continue
			chunk = color_image[y : y +  h , x : x + w]

			img = self.__convert_opencv_to_PIL(chunk)
			imgc = ImageTranscriberWithExisting(img)

			# Only keep parts with text
			if imgc.text is not None and imgc.text.strip():
				new_img[y : y +  h , x : x + w] = chunk

		# Take simplified image and greyscale it
		img2grey = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
		bw = cv2.cvtColor(img2grey,cv2.COLOR_GRAY2RGB)

		img = self.__convert_opencv_to_PIL(bw)
		return img