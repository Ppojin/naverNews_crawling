from selenium import webdriver
import re
import csv
import json

# searchStr = "크롤링"
# pubStrList = "경향신문#국민일보#내일신문#한겨레".split("#")
searchStr = input("검색어 입력 : ")
pubStrList = input("출처입력 (#으로 구분) :").split("#")
boolCsv = True
strCsvfileName = "test"

strUrl = "https://search.naver.com/search.naver?where=news&query="
driver = webdriver.Chrome('./chromedriver')
driver.get(strUrl+searchStr)
driver.find_element_by_css_selector("a#_search_option_btn.bt_option").click()
for menu in driver.find_elements_by_css_selector("li.menu > a.m"):
    temp = menu.get_attribute("onclick")
    if temp == "tCR('a=fno.journallink');":
        menu.click()
        break
pubList = driver.find_element_by_css_selector("div#order_cat._group_order").find_elements_by_css_selector("ul.viewlst > li")

n = 0
for pub in pubList:
    if pub.text in pubStrList:
        pub.find_element_by_css_selector("input").click()
        n += 1
        if n == len(pubStrList) : break
driver.find_element_by_css_selector("button._submit_btn").click()


def findCsss(driver, selector):
    return driver.find_elements_by_css_selector(selector)
def findCss(driver, selector):
    return driver.find_element_by_css_selector(selector)

result = []
while 1:
    btnNext = findCsss(driver, "a.next")
    for article in findCsss(driver, "ul.type01 > li"):
        source = findCss(article, "span._sp_each_source").text
        regex = re.compile(r"네이버뉴스|보내기| |"+source)
        jsonArticle = {
            'url': findCss(article, "a._sp_each_url").get_attribute("href"),
            'title': findCss(article, "a._sp_each_title").get_attribute("title"),
            'source': source,
            'date': re.sub(regex, "", findCss(article, "dd.txt_inline").text),
            'body': findCsss(article, "dd")[1].text
        }
        result.append(jsonArticle)
        
    if len(btnNext) > 0:
        btnNext[0].click()
    else:
        print("검색 완료")
        break

if boolCsv:        
    f = csv.writer(open(strCsvfileName+".csv", "w"))

    f.writerow(["title", "source", "date", "url", "body"])

    for x in result:
        f.writerow([ x["title"], x["source"], x["date"], x["url"], x["body"] ])
    print("CSV 파일 저장 완료")

print ("작업 완료")