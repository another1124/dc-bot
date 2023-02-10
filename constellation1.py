import requests
from bs4 import BeautifulSoup

list1 = ["牡羊座","金牛座","雙子座","巨蟹座",
         "獅子座","處女座","天秤座","天蠍座",
         "射手座","摩羯座","水瓶座","雙魚座"]

def destiny(astros):
    index = list1.index(astros)
    
    url = "https://astro.click108.com.tw/daily_" + str(index) + ".php?iAstro=" + str(index)
    
    data = requests.get(url)
    soup = BeautifulSoup(data.text,"html.parser")
    
    lucky_number = soup.find_all("h4")[0].text
    lucky_color = soup.find_all("h4")[1].text
    print("幸運數字：" + lucky_number)
    print("幸運顏色：" + lucky_color)
    
    div = soup.find("div",class_ = "TODAY_CONTENT")
    print(div.text)
    
#destiny("牡羊座")