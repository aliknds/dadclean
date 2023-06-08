# Importing required libraries
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

image_path = r'C:\Users\user\Desktop\Borgotsoi\py\OCR\test.jpg'
# Specify the exact path of the image
img = Image.open(image_path)

# Use pytesseract to convert the image into text
text = pytesseract.image_to_string(img, lang='eng+mon')

# Open a file in write mode
with open('test.txt', 'w', encoding='utf-8') as f:
    # Write the text into the file
    f.write(text)

# Print the text
print(text)
