from PIL import Image
from pytesseract import *
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'envs' + os.sep + 'propertyOcr.ini')

def ocrToStr(fullPath, outTxtPath, fileName, lang='eng'): #default -> eng
    #이미지 경로

    img = Image.open(fullPath)
    txtName = os.path.join(outTxtPath, fileName.split('.')[0])
    
    #추출(이미지 파일, 추출언어, 옵션)
    outText = image_to_string(img, lang = lang, config = '--psm 1 -c preserve_interword_spaces=1')
    
    print('+++ OCT Extrct Result +++')
    print('Extract FileName ->>> : ', fileName, ': <<<-')
    print(outText)
    #추출 문자 텍스트 파일 쓰기
    strToTxt(txtName, outText)

#문자열 -> 텍스트 파일 개별 저장
def strToTxt(txtName, outText):
    with open(txtName + '.txt', 'w', encoding = 'utf-8') as f:
        f.write(outText)

if __name__ == "__main__":

    outTxtPath = os.path.dirname(os.path.realpath(__file__))+config['Path']['OcrTxtPath']
    
    #OCR 추출 작업 메인
    for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))+config['Path']['OriImgPath']):
        for fname in files:
            fullName = os.path.join(root, fname)
            ocrToStr(fullName, outTxtPath, fname, 'kor+eng')