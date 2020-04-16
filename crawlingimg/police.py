from selenium import webdriver as wd
import time
startPage = 1
endPage = 4

for p in range(startPage, endPage+1):
    driver  = wd.Chrome(executable_path = './chromedriver')
    url = "https://www.smpa.go.kr/user/nd54882.do?page="+str(p)+"&pageLS=&pageSC=SORT_ORDER&pageSO=DESC&pageST=SUBJECT&pageSV=&itemShCd1=&itemShCd2=&itemShCd3="
    driver.get(url)
    driver.implicitly_wait(5)
    print(p, "번째 page 접속 성공")
    driver.implicitly_wait(5)

    #time.sleep(5)
    for i in range(1,11):
        postPath = "/html/body/form/div/div[2]/div[3]/table/tbody/tr[" + str(i) +"]/td[2]/a"
        driver.find_element_by_xpath(postPath).click()
        print(p,"페이지 ", i,"번 째 post 접속 성공!")
        driver.implicitly_wait(5)
        fileNames = driver.find_elements_by_class_name('doc_link')
        for j in range(0,len(fileNames)):
            if "jpg" in fileNames[j].text:    
                imgPath = "/html/body/form/div/div[2]/div[3]/table/tbody/tr[3]/td/a["+str(j+1)+ "]"
                #xpath 는 1부터 idx 시작
                driver.find_element_by_xpath(imgPath).click()
                driver.implicitly_wait(5)
        driver.back() #목록으로
        driver.back() #목록으로        
        print(p,"페이지 ",i,"번 째 post 다운로드 완료!")
    driver.close()

