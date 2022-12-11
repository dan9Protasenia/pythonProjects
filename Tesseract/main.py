import cv2
import pytesseract
from PIL import Image

img = Image.open('image.png')
image = cv2.imread('image.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# text will be displayed from the image
config = r'--oem 3 --psm 6'
custom_config = r'--oem 3 --psm 13'

# print(pytesseract.image_to_string(img, config=config))

data = pytesseract.image_to_data(image, lang='eng', config=config)

# function.1 txt.file
file_name = img.filename
file_name = file_name.split('.')[0]

text = pytesseract.image_to_string(image, lang='eng', config=config)
print(text)

with open(f'{file_name}.txt', 'w') as text_file:
    text_file.write(text)

# function.2 visualization
for i, el in enumerate(data.splitlines()):
    if i == 0:
        continue

    el = el.split()
    try:
        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
        cv2.rectangle(image, (x, y), (w + x, h + y), (0, 0, 255), 1)
        cv2.putText(image, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 255, 255), 1)
    except IndexError:
        continue
# print('operation was skipped')

cv2.imshow('Result', image)
cv2.waitKey(0)


