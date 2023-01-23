import cv2
import requests

def add_to_name(name, add):
    return name[:name.rfind('.')] + add + name[name.rfind('.'):]

def remove_background(image_name):
    response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(image_name, 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'vWr4Bn1qKT8pbA3jD6snZ72N'} # DONT SHARE API KEY
    )
    if response.status_code == requests.codes.ok:
        with open(add_to_name(image_name,'_nobg'),'wb') as out:      
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

def get_siluet(image_name):
    # remove_background(image_name)
    name = add_to_name(image_name,'_nobg')
    im = cv2.imread(name)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 0, 255, 0)

    cv2.imshow('res',thresh)
    cv2.imwrite(add_to_name(image_name,'_mask'), thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


get_siluet('key.jpg')