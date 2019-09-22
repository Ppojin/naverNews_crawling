from selenium import webdriver
import re
import csv
import json

def json2xml(json_obj, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "    " + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)

# searchStr = "크롤링"
# pubStrList = "경향신문#국민일보#내일신문#한겨레".split("#")
searchStr = input("검색어 입력 : ")
pubStrList = input("출처입력 (#으로 구분) : ").split("#")

boolCsv = True if input("CSV 파일로 저장할까요? [y/n] : ") in ['y', 'Y'] else False
if boolCsv :
    strCsvfileName = "test"

boolJson = True if input("json 파일로 저장할까요? [y/n] : ") in ['y', 'Y'] else False
if boolJson :
    strJsonfileName = "test"

boolXml = True if input("xml 파일로 저장할까요? [y/n] : ") in ['y', 'Y'] else False
if boolXml :
    strXmlfileName = "test"

print("검색중...")

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
id = 0
while 1:
    btnNext = findCsss(driver, "a.next")
    for article in findCsss(driver, "ul.type01 > li"):
        source = findCss(article, "span._sp_each_source").text
        regex = re.compile(r"네이버뉴스|보내기| |[A-Z]*[0-9]*면([0-9]단| )|"+source)
        jsonArticle = {
            'id': id,
            'url': findCss(article, "a._sp_each_url").get_attribute("href"),
            'title': findCss(article, "a._sp_each_title").get_attribute("title"),
            'source': source,
            'date': re.sub(regex, "", findCss(article, "dd.txt_inline").text),
            'body': findCsss(article, "dd")[1].text
        }
        result.append(jsonArticle)
        id += 1
        
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

if boolJson:
    with open(strJsonfileName+'.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print("json 파일 저장 완료")

if boolXml:
    f = open(strXmlfileName+'.xml', 'w')
    f.write(json2xml({'main':result}))
    print("xml 파일 저장 완료")
    
# print(boolCsv, boolJson, boolXml)

print ("작업 완료")