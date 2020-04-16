from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import bs4
import urllib.request
import time
import datetime
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'envs' + os.sep + 'propertyNews.ini')

class NewsParser:
    def __init__(self, startUrl):
        self.startUrl = startUrl
        self.topUrlList = []
        self.cntHateList = []

    #brief: Parse top news using BeautifulSoup
    #post: append top newsUrls
    def ParseTopByBs(self):
        print("top url 접속")
        html = urllib.request.urlopen(self.startUrl)
        bsHtml = bs4.BeautifulSoup(html, "html.parser")
        topUrls = (bsHtml.findAll("div", {"class":"ranking_thumb"}))
        for i in topUrls:
            tempStr = str(i)
            tempList = tempStr.split('"')
            newsUrl = "https://news.naver.com"+tempList[5]
            newsUrl= newsUrl.replace("amp;","")
            self.topUrlList.append(newsUrl)

    #brief: Parse numer from news using Selenium
    #post: append int cntHate into list
    def ParseNumBySel(self):
        #temp
        i = 0
        options = Options()
        prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 
        'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen'
         : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 
         'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads':
          2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' 
          : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}
        options.add_experimental_option('prefs', prefs)
        options.add_argument("start-maximized") 
        options.add_argument("disable-infobars") 
        options.add_argument("--disable-extensions") 
        options.add_argument('--headless')
        driver  = wd.Chrome(executable_path = './chromedriver', options=options)
        try:
            for topUrl in self.topUrlList:
                i=i+1
                print(topUrl)
                driver.get(topUrl)
                print("뉴스 url 접속 성공")
                temp = WebDriverWait(driver, 60).until
                (
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.u_likeit_list.angry"))
                )
                #spiLayer > div._reactionModule.u_likeit > ul > li.u_likeit_list.angry > a > span.u_likeit_list_count._count
                time.sleep(2)
                cntHate = driver.find_element_by_css_selector("#spiLayer > div._reactionModule.u_likeit > ul > li.u_likeit_list.angry > a > span.u_likeit_list_count._count")
                cntHate = cntHate.text
                print(i, " 번째 완료! 결과는", cntHate)
                cntHate = cntHate.replace(',', '')
                cntHate.strip()
                if(cntHate == ''): raise Exception
                intCntHate = int(cntHate)
                self.cntHateList.append(intCntHate)
        except Exception as e:
            print(e)
        driver.close()
        
        
    #brief: Display All Record
    def DisplayRecord(self):
        print("Hate cnt")
        for i in self.cntHateList:
            print(i)

    #brief: Return list sum
    def GetListSum(self):
        return sum(self.cntHateList)

    def Run(self):
        self.ParseTopByBs()
        self.ParseNumBySel()
        self.DisplayRecord()
        return self.GetListSum()

class Timer:
    def __init__(self, startStr, endStr):
        self.startStr = startStr
        self.endStr = endStr
        self.startDate = datetime.datetime.strptime(self.startStr, "%Y%m%d")
        self.endDate = datetime.datetime.strptime(self.endStr, "%Y%m%d")
        self.strList = []


    #brief: Str to Date type 
    def StrToDate(self,myStr, myDate):
        myDate = datetime.datetime.strptime(myStr, "%Y%m%d")

    #brief: Date to Str type
    def DateToStr(self, myDate, myStr):
        myStr = str(myDate.date()).replace('-','')
        return myStr

    #brief: Date to Str type
    def AddStartDate(self):
        self.startDate = self.startDate+datetime.timedelta(days=1)
    
    #brief: append strList, loof, runner
    def TimeLoof(self):
        self.strList.append(self.startStr)

        while(True):
            if(self.startDate == self.endDate):
                return self.strList
            else:
                self.AddStartDate()
                self.startStr = self.DateToStr(self.startDate,self.startStr)
                self.strList.append(self.startStr)


if __name__ == "__main__":
    resultPath = os.path.dirname(os.path.realpath(__file__))+config['Path']['NewsResPath']
    endDay = ['31', '30', '31', '30', '31']
    for m in ['03', '04', '05', '06', '07']: #3월부터 7월까지
        resFile = open(resultPath + os.sep +"result" + m + ".txt", "w")
        resList = []
        startDate = "2019"+m+"01"
        endDate = "2019"+m+endDay[int(m)-3]
        t = Timer(startDate,endDate)
        dates = t.TimeLoof()
        print(dates)
        for date in dates:
            url = "https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=100&date="+date
            p = NewsParser(url)
            print(date+"접속...")
            todayHateNum = p.Run()
            resList.append(date + ", " +str(todayHateNum))
        for result in resList:
            resFile.write(result+'\n')
        resFile.close()
        print("조사 기간" + startDate + " ~ " + endDate)
        print(resList)
        

    
    # hateCnt 리스트를 날짜별로 받아내고 있다. 이를 이제 날짜와 함께 묶어서 리스트로 다시 만든 다음에(메인 함수에서)
    # 이를 csv로 만들어서 확인하자.