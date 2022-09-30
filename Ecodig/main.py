# import numpy as np
# import cv2 as cv
# from django.conf import settings

# def scale(image, scale_width):
#     (image_height, image_width) = image.shape[:2]
#     new_height = int(scale_width / image_width * image_height)
#     return cv.resize(image, (scale_width, new_height))


# watermark = scale(cv.imread('directory/logo.png', cv.IMREAD_UNCHANGED), 400)
# (watermark_height, watermark_width) = watermark.shape[:2]

# image = scale(cv.imread('/mediaprot/media'), 1200)
# (image_height, image_width) = image.shape[:2]
# image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)

# overlay = np.zeros((image_height, image_width, 4), dtype='uint8')
# overlay[image_height-watermark_height:image_height, image_width-watermark_width:image_width] = watermark

# cv.addWeighted(overlay, 1.0, image, 1.0, 0, image)

# while True:
#     cv.imshow("overlay", overlay)
#     cv.imshow("image", image)
#     cv.imshow("watermark", watermark)
    
#     if cv.waitKey(1) == ord('q'):
#         break



from fileinput import filename
from PIL import ImageDraw, ImageFont, Image
from tkinter import filedialog, Tk

root = Tk()
root.withdraw()
filename = filedialog.askopenfilename(initialdir="/Users/SONY/Documents/DigEcom/mediaProt/media", title='Select an image')
# print(filename)

def add_watermark(image, wm_text):
    opened_image = Image.open(image)

    image_width, image_height =opened_image.size
    draw = ImageDraw.Draw(opened_image)
    font_size = int(image_width/8)

    font = ImageFont.truetype('arial.ttf', font_size)

    x, y = int(image_width/2), int(image_height/2)


    draw.text((x, y), wm_text, font=font, fill='#FFFF', stroke_width=5, stroke_fill="#222", anchor='ms')

    opened_image.show()


add_watermark(filename, "MESHUTTER")