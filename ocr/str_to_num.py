from PIL import Image
from pytesseract import *
import configparser
import os
import re

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'envs' + os.sep + 'property.ini')

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

"""
잘못된 int 값이 오는 것을 방지하기 위해
1. 10보다 작은 수가 있는지 체크합니다.
2. 앞의 두 숫자를 제외한 숫자가 0인지를 체크합니다.
경찰청에서 집계한 시위 규모는 10 이상이고 앞의 두 수를 제외하고
모두 0값이기 때문입니다.
"""
def CheckAllZero(strNum):
	if(int(strNum)<10):
		return False
	else:
		for i in strNum[2:]:
			if(i!='0'):
				return False
		return True

"""
list의 문자열을 int로 변환
"""
def StrToIntFromList(lst):
	lst = list(map(int, lst))
	return lst

def LineToNum(line):
#	subLine = re.sub('[^0-9:.)| ]','',line)
#	subLineList = subLine.split(" ")

	lineList = line.split(" ")

#	if(lineList==['']):
#		return False

	numList = []

	for i in lineList:
		i = re.sub('[ ]', '', i)

		#숫자, )|]} 외 다른 값이 포함됐다면 쓸모 없는 값이다.
		if bool(re.search('[^0-9)|\]}]', i)):
			continue

		#집회수에는 ) or | or ]이 붙어있다.
		if( not ( (')' in i) or ('|' in i) ) ):
			if(not ( (']' in i) or ('}' in i) ) ):
				continue
	
		i = re.sub('[)|\]}]','',i) 

		if(len(i)==0):
			continue

		elif(CheckAllZero(i)):
			numList.append(i)

	if(len(numList)!=0):
		return numList
	else:
		return False


def TxtToList(fullPath, fname, resList):
	f = open(fullPath, 'r',encoding = 'utf-8')
	tempList = []
	for line in f:
		numLine = LineToNum(line)
		if(numLine):
			tempList.append(numLine)
	#list를 flatten 하게 만든다.
	tempList = sum(tempList, [])
	sumListNum = sum(StrToIntFromList(tempList))
	print(tempList)
	print()
	resList.append(fname[:6] + ',' + str(sumListNum))

if __name__ == "__main__":
	resList = []
	#텍스트 전처리 메인
	outFilePath = os.path.dirname(os.path.realpath(__file__))+config['Path']['ResPath']
	for i in range(6, 12):
		for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))+os.sep+'res'+os.sep+str(i)+'m'):
			for fname in files:
				fullPath = os.path.join(root, fname)
				TxtToList(fullPath, fname,resList)
		f = open(outFilePath+os.sep+'result_'+str(i)+'m.txt', 'w')
		
		for itor in resList:
			f.write(itor+'\n')

		f.close()