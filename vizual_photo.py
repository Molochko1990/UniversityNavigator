import cv2
import pytesseract


def visual():
    Blocks = ['И-', 'Э-', 'Р-', "ГУК-", "Т-"]
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    img = cv2.imread("D:\\photo.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    StringFound = False
    res = 'Не могу распознать фото'
    for i in range(3, 14):
        if StringFound == False:
            config = r'--oem 3 --psm ' + str(i)
            result = pytesseract.image_to_string(img, config=config, lang='rus')
            for i in Blocks:
                if i in result:
                    rp = result.index('-')
                    if 'а' in result[rp + 4] or 'б' in result[rp + 4] or 'в' in result[rp + 4]:
                        res = i + result[rp + 1] + result[rp + 2] + result[rp + 3] + result[rp + 4]
                    else:
                        res = i + result[rp + 1] + result[rp + 2] + result[rp + 3]
                    StringFound = True
                    break
    return res

