import cv2
import numpy as np
import skimage.exposure
import requests    

#REMOVE BACKGROUND
# response = requests.post(
#     'https://api.remove.bg/v1.0/removebg',
#     files={'image_file': open('inputtest.jpg', 'rb')},
#     data={'size': 'auto'},
#     headers={'X-Api-Key': 'vWr4Bn1qKT8pbA3jD6snZ72N'}   
# )
# if response.status_code == requests.codes.ok:
#     with open(r'nobg.png','wb') as out:           
#         out.write(response.content)
# else:
#     print("Error:", response.status_code, response.text)


#GET SILUET
# load image
img = cv2.imread('profile_nobg.png')

# convert to gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold
thresh = cv2.threshold(gray, 11, 255, cv2.THRESH_BINARY)[1]

# apply morphology to clean small spots
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, borderType=cv2.BORDER_CONSTANT, borderValue=0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel, borderType=cv2.BORDER_CONSTANT, borderValue=0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
morph = cv2.morphologyEx(morph, cv2.MORPH_ERODE, kernel, borderType=cv2.BORDER_CONSTANT, borderValue=0)

# get external contour
contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
big_contour = max(contours, key=cv2.contourArea)

# draw white filled contour on black background as mas
contour = np.zeros_like(gray)
cv2.drawContours(contour, [big_contour], 0, 255, -1)

# blur dilate imag
blur = cv2.GaussianBlur(contour, (5,5), sigmaX=0, sigmaY=0, borderType = cv2.BORDER_DEFAULT)

# stretch so that 255 -> 255 and 127.5 -> 0
mask = skimage.exposure.rescale_intensity(blur, in_range=(127.5,255), out_range=(255,0))

# put mask into alpha channel of input
result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
result[:,:,3] = mask

# save output
cv2.imwrite('mask_result.png', mask)

cv2.imshow('input', img)
cv2.imshow('thresh', thresh)
cv2.imshow('morph', morph)
cv2.imshow('contour', contour)
cv2.imshow('mask', mask)
# cv2.imshow('result', result)


cv2.waitKey(0)
cv2.destroyAllWindows()
