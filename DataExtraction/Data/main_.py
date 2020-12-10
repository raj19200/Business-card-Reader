from .fpt import four_point_transform
from skimage.filters import threshold_local
import pytesseract
import numpy as np
from cv2 import cv2
import imutils
import sys
from .Recognizer.contact import is_contact
from .Recognizer.email import is_email
from .Recognizer.pincode import is_pincode
from .Recognizer.website import is_website
from .Recognizer.states import find_best_guessed_state
from .Recognizer.cities import find_best_guessed_city
from .Recognizer.cities2 import is_city
from .Recognizer.company_name import is_company_name
from .Recognizer.pincode2 import is_pincode2
from .Recognizer.address import is_address
from .Recognizer.name import find_best_guessed_name
import os
from DataExtraction import settings


def downsize_image(image,max_height=620,max_width=1080):
    # max_width = 1080
    # max_height = 620
    height,width = image.shape
    scale_w = max_width/width
    scale_h = max_height/height


    if(width<=max_width):
        if(height<=max_height):
            #dont resize
            pass
        else:
            #resize height dimension
            image = cv2.resize(image,(int(width),int(height*scale_h)))
    else:
        if(height<=max_height):
            #resize width dimension
            image = cv2.resize(image,(int(width*scale_w),int(height)))
        else:
            #resize both dimension
            image = cv2.resize(image,(int(width*scale_w),int(height*scale_h)))
    
    return image,scale_h,scale_w


def preprocessor(img_path):
    image_og = cv2.imread(img_path)
    # image_og = cv2.imread(path)
   
    #downsize image for performance
    image_size = 1024
    orig_height, orig_width, _ = image_og.shape
    scale = orig_width / image_size

    image = cv2.resize(image_og, (image_size, int(orig_height / scale + 1)), None)
    # cv2.imshow("image",image)
    # print(image.shape,scale_h,scale_w)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # eqhisted = clahe.apply(gray)

    edged = cv2.Canny(gray, 25, 100)

    kernel = np.ones((5,5),np.uint8)
    edged = cv2.dilate(edged,kernel,iterations = 1)

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
        print("Couldnot find contour with four points!!!")
        print("Using first four points from approx")
        screenCnt = approx[-4:]
        
    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(image_og, screenCnt.reshape(4, 2)* scale)
    # convert the warped image to grayscale, then threshold i
    # to give it that 'black and white' paper effect
    warped= cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    ret3,th3 = cv2.threshold(warped,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #downsize and convert to 300 dpi
    th3,scale_h,scale_w = downsize_image(th3)
    # cv2.imshow("th3",th3)
    # cv2.waitKey(0)
    return th3


def tokenizer(txt):
    lines = txt.split("\n")
    tokens = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            tokens.append(line)

    return tokens
# image_fullpath=sys.argv[1]
# image_name=sys.argv[2]
# Image=cv2.imread(str(image_fullpath))
# image_save_path=image_fullpath.replace(image_name,"temp.png")
# im = preprocessor("image/1.jpg")
# cv2.imshow("im",im)
# cv2.waitKey(0)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
# txt = pytesseract.image_to_string(im, timeout=5,lang="eng") # Timeout after 5 seconds
# tokens = tokenizer(txt)
# # print(txt)
# print(tokens)
# # print(find_best_guessed_city(tokens))
# city=find_best_guessed_city(tokens)

# # print(find_best_guessed_state(tokens))
# state=find_best_guessed_state(tokens)
# # # print(find_best_guessed_name(tokens))
# name=find_best_guessed_name(tokens)
# # print(is_address(tokens))
# address=is_address(tokens)
# for token in tokens:
#     # print(token)
#     contacts = is_contact(token)
#     # print(contacts)
#     if(not len(contacts)):
#         # print(is_pincode(token))
#         pincode=is_pincode(token)
#     # print(is_email(token))
#     email=is_email(token)
#     # print(is_website(token))
#     website=is_website(token)
# # params={"name":name,"companyName":name,"email":email,"website":website,"contact1":contacts,"contact2":contacts,"city":city,"state":state,"pincode":pincode,"address":address}
def test(img_path):
    path = os.path.join(settings.MEDIA_ROOT, img_path)
    im = preprocessor(path)
    cv2.imshow("im",im)
    cv2.waitKey(0)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    txt = pytesseract.image_to_string(im, timeout=5,lang="eng") # Timeout after 5 seconds
    tokens = tokenizer(txt)
    # print(txt)
    print(tokens)
    # print(find_best_guessed_city(tokens))
    # city=find_best_guessed_city(tokens)

    # print(find_best_guessed_state(tokens))
    state=find_best_guessed_state(tokens)
    # # print(find_best_guessed_name(tokens))
    name=find_best_guessed_name(tokens)
    # print(is_address(tokens))
    city=[]
    address=is_address(tokens)
    if(len(address)):
        city=is_city(address[-1])
    contacts=[]
    pincode=[]
    email=[]
    website=[]
    companyname=[]
    p=[]
    for token in tokens:
        # print(token)
        c = is_contact(token)
        if(len(c)):
            contacts.extend(c)
        # print(contacts)
        if(not len(c)):
            # print(is_pincode(token))
            p=is_pincode(token)
          
            if(len(p)):
                pincode.extend(p)
        # print(is_email(token))
        e=is_email(token)
        if(len(e)):
            email.extend(e)
        # print(is_website(token))
        w=is_website(token)
        if(len(w)):
            website.extend(w)
        cname = is_company_name(token)
        if(cname):
            companyname.append(token)
    if((not len(p)) and len(address)):
        p=is_pincode2(address[-1])
        if(len(p)):
            pincode.extend(p)
    return contacts,pincode,email,website,city,state,address,name,path,companyname