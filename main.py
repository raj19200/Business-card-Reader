import sys
from PIL import Image
from fpt import four_point_transform
from skimage.filters import threshold_local
import numpy as np
from cv2 import cv2
import imutils
import pytesseract

image_fullpath=sys.argv[1]
image_name=sys.argv[2]


Image=cv2.imread(str(image_fullpath))

image_save_path=image_fullpath.replace(image_name,"temp.png")

# print(image_save_path)
# Image = cv2.imread(image_save_path)


width,height,_ = Image.shape
ratio = 0.25

Original = Image.copy()
image = cv2.resize(Image,(int(height*ratio),int(width*ratio)))

# image_ogratio = image.copy()
# image = imutils.resize(image, height = 500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray, (5, 5), 0)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
# cv2.imshow("Blurred",gray)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
eqhisted = clahe.apply(gray)

# cv2.imshow("eqhisted",eqhisted)
# cv2.imshow("Blurred2",gray)

edged = cv2.Canny(gray, 25, 100)
cv2.imshow("edged",edged)

kernel = np.ones((5,5),np.uint8)
edged = cv2.dilate(edged,kernel,iterations = 1)

cv2.imshow("dilate",edged)



cv2.waitKey(0)

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
else:
	print("Approx",approx)
	screenCnt = approx[:4]
	
# apply the four point transform to obtain a top-down
# view of the original image
print("Screencnt",screenCnt)
warped = four_point_transform(Image, screenCnt.reshape(4, 2) / ratio)
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# T = threshold_local(warped, 11, offset = 10, method = "gaussian")
# warped = (warped > T).astype("uint8") * 255
ret3,warped = cv2.threshold(warped,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# cv2.imshow("Original", imutils.resize(image_ogratio, height = 650))
# cv2.imshow("Resized",image)
cv2.imshow("Scanned",cv2.resize(warped,(int(height*ratio),int(width*ratio))))
cv2.waitKey(0)
# img=cv2.imread(warped)
#         height, width, _ = img.shape
#         roi = img[0: height, 0: width]
#         urlapi = "https://api.ocr.space/parse/image"
#         , compressedimage = cv2.imencode(".jpg", roi, [1, 90])
#         file_bytes = io.BytesIO(compressedimage)
#         result = requests.post(url_api,
#                     files = {"ez.jpg": file_bytes},
#                     data = {"apikey": "a2f0f7f46e88957",
#                             "language": "eng"})


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
print(pytesseract.image_to_string(warped,lang="eng"))