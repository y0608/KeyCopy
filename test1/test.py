import cv2
im = cv2.imread('key_nobg.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 0, 255, 0)

cv2.imshow('res',thresh)
# cv2.imwrite('mask_result.png', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()


# from PIL import Image
# from pylab import *

# # read image to array
# im = array(Image.open('nobg.png').convert(''))

# # create a new figure
# fig = figure(frameon=True)

# # show contours with origin upper left corner
# contour(im, levels=[0], colors='black', origin='image')

# axis('equal')

# # for spine in gca().spines.values():
# #     spine.set_visible(False)


# show()


# fig.savefig('temp.png',bbox_inches="tight")
# close(fig)