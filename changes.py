import json
import datetime
import cv2
import imutils
import pytesseract

Entries = []
f = open("products.json", "r")
prev = json.loads(f)
Entries.update(f)
print(Entries)
def main():
    try:
        i = 1
        while (1):
            x = int(input("Enter 1 to capture, 0 to exit- "))
            if(x==1):
                pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'
                cap= cv2.VideoCapture(0)
                fourcc= cv2.VideoWriter_fourcc('X','V','I','D')
                out=cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
                while(cap.isOpened()):
                    ret, image = cap.read()
                    if ret==True:
                        out.write(image)
                        cv2.imshow('frame', image) #to show the frame
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    else:
                        break
                # image = cv2.imread('test6.jpg')
                image = imutils.resize(image, width=300)
                # cv2.imshow("original image", image)
                # cv2.waitKey(0)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # cv2.imshow("greyed image", gray_image)
                # cv2.waitKey(0)
                gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
                # cv2.imshow("smoothened image", gray_image)
                # cv2.waitKey(0)
                edged = cv2.Canny(gray_image, 30, 200)
                # cv2.imshow("edged image", edged)
                # cv2.waitKey(0)

                cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                image1 = image.copy()
                cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
                # cv2.imshow("contours", image1)
                # cv2.waitKey(0)
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
                screenCnt = None
                image2 = image.copy()
                cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
                # cv2.imshow("Top 30 contours", image2)
                # cv2.waitKey(0)

                for c in cnts:
                    perimeter = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
                    if len(approx) == 4:
                        screenCnt = approx
                        x, y, w, h = cv2.boundingRect(c)
                        new_img = image[y:y + h, x:x + w]
                        cv2.imwrite('./' + str(i) + '.png', new_img)
                        break

                cv2.drawContours(image, [screenCnt], -1, (255, 255, 0), 3)
                # cv2.imshow("image with detected license plate", image)
                # cv2.waitKey(0)
                Cropped_loc = './' + str(i) + '.png'

                cv2.imshow("cropped", cv2.imread(Cropped_loc))
                cv2.waitKey(0)
                plate = pytesseract.image_to_string(Cropped_loc, lang='eng')

                cap.release()
                out.release()
                cv2.destroyAllWindows()

                vno = plate
                date_time = datetime.datetime.now()
                dict = {"VehicleNo": str(vno),
                       "time": str(date_time),
                        "imagee": './' + str(i) + '.png'
                       }
                Entries.append(dict)
                print(dict)
                with open("products.json", "w") as file:
                    json.dump(Entries, file)

                i += 1
                continue
            else:
                return 0
    except:
        main()
main()
