import cv2
import pytesseract

# Load the image using OpenCV
image = cv2.imread('dataset/two.png')

# Preprocess the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours of the digits
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize an empty list to store recognized digits
recognized_digits = []

# Iterate over the contours
for contour in contours:
    # Get the bounding rectangle coordinates
    (x, y, w, h) = cv2.boundingRect(contour)

    # Extract the digit ROI from the thresholded image
    roi = thresh[y:y + h, x:x + w]

    # Use Tesseract OCR to recognize the digit
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

    digit = pytesseract.image_to_string(roi, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

    # Append the recognized digit to the list
    recognized_digits.append(digit)

# Print the recognized digits
print('Recognized Digits:', recognized_digits)

