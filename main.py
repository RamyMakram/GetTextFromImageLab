from PIL import Image, ImageEnhance
import sys
import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class labObject:
    def __init__(self, fas, pla,gl):
        self.fas = fas
        self.pla = pla
        self.gl = gl

    
class lab_class:
    def __init__(self,filename):
        self.filename = filename

    def run(self):
        im = Image.open(self.filename)
        enhancer = ImageEnhance.Brightness(im)
        factor = 1.5
        im_output = enhancer.enhance(factor)
        im_output.save('brightened-image.png')

    def enhance(self):
        img = cv2.imread('brightened-image.png', 1)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        #cv2.imwrite('final.png', final)
        #img_rgb = Image.open('img\\' + filename + 'final.png')
        self.text_ = pytesseract.image_to_string(final, config='--oem 3 --psm 6')
        print(pytesseract.image_to_string(final, config='--oem 3 --psm 6'))

    def getValues(self):
        text = self.text_
        Fasting = ''
        Plasma = ''
        Glycated = ''
        text = text.lower()
        if text.find('Fasting Plasma glucose '.lower()) != -1:
            position = text.find('Fasting Plasma glucose '.lower())
            length = len('Fasting Plasma glucose ')
            for i in range(position + length, len(text)):
                if text[i].isdigit():
                    Fasting += text[i]
                else:
                    if not (text[i].isdigit()) and not (text[i].isspace()):
                        break

        if text.find('Plasma Glucose 2hrs PP '.lower()) != -1:
            position = text.find('Plasma Glucose 2hrs PP '.lower())
            length = len('Plasma Glucose 2hrs PP ')
            for i in range(position + length, len(text)):
                if text[i].isdigit():
                    Plasma += text[i]
                else:
                    if not (text[i].isdigit()) and not (text[i].isspace()):
                        break

        if text.find('Glycated Haemoglobin (HbA‘c) '.lower()) != -1:
            position = text.find('Glycated Haemoglobin (HbA‘c) '.lower())
            length = len('Glycated Haemoglobin (HbA‘c) ')
            for i in range(position + length, len(text)):
                if text[i].isdigit() or text[i]=='.':
                    Glycated += text[i]
                else:
                    if not (text[i].isdigit()) and not (text[i].isspace()):
                        break
        elif text.find('Glycated Haemoglobin (HbA1c) '.lower()) != -1:
            position = text.find('Glycated Haemoglobin (HbA1c) '.lower())
            length = len('Glycated Haemoglobin (HbA1c) ')
            for i in range(position + length, len(text)):
                if text[i].isdigit() or text[i]=='.':
                    Glycated += text[i]
                else:
                    if not (text[i].isdigit()) and not (text[i].isspace()):
                        break

        elif text.find('Glycated Haemoglobin (HbA tc) '.lower()) != -1:
            position = text.find('Glycated Haemoglobin (HbA tc) '.lower())
            length = len('Glycated Haemoglobin (HbA tc) ')
            for i in range(position + length, len(text)):
                if text[i].isdigit() or text[i]=='.':
                    Glycated += text[i]
                else:
                    if not (text[i].isdigit()) and not (text[i].isspace()):
                        break

        lengthGla = len(Glycated)
        if Glycated.find('.')==-1 and lengthGla!=0:
            Glycated = Glycated[:lengthGla - 1] + '.' + Glycated[lengthGla - 1:]
        return labObject(Fasting,Plasma,Glycated)

def main():
    path=input('Enter Path OF Photo: ')
    dd = lab_class(path)#set path here
    dd.run()
    dd.enhance()
    values = dd.getValues()
    print(values.fas)
    print(values.pla)
    print(values.gl)
    pass
    
if __name__ == "__main__":
    sys.exit(int(main() or 0))



























