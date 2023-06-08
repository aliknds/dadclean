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
hocr_text = pytesseract.image_to_pdf_or_hocr(img, lang='eng+mon', config='--psm 6', extension='hocr')
# Open a file in write mode
with open('test.html', 'w', encoding='utf-8') as f:
    # Write the text into the file
    f.write(hocr_text.decode())

# Print the text
print(hocr_text)
